"""
Alert management routes and logic
"""
from flask import Blueprint, request, jsonify, session
from models import db, Alert, User, AlertLog, AuditLog
from auth import admin_required, login_required, log_action
from config import Config
from datetime import datetime

alerts_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

@alerts_bp.route('/create', methods=['POST'])
@admin_required
def create_alert():
    """Create a new alert (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'message', 'severity', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        title = data['title'].strip()
        message = data['message'].strip()
        severity = data['severity'].upper()
        location = data['location'].strip()
        scheduled_date = data.get('scheduled_date')  # Optional: ISO format date-time
        
        # Validate severity
        if severity not in Config.ALERT_SEVERITIES:
            return jsonify({'error': f'Invalid severity. Must be one of: {Config.ALERT_SEVERITIES}'}), 400
        
        # Parse scheduled_date if provided
        scheduled_datetime = None
        if scheduled_date:
            try:
                scheduled_datetime = datetime.fromisoformat(scheduled_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO format'}), 400
        
        # Create alert with PENDING status
        alert = Alert(
            title=title,
            message=message,
            severity=severity,
            location=location,
            status='PENDING',
            created_by=session['user_id'],
            scheduled_date=scheduled_datetime
        )
        
        db.session.add(alert)
        db.session.commit()
        
        log_action(
            'ALERT_CREATED', 
            f'Alert created: {title} for {location} (Severity: {severity})',
            session['user_id']
        )
        
        return jsonify({
            'message': 'Alert created successfully with PENDING status',
            'alert': {
                'id': alert.id,
                'title': alert.title,
                'message': alert.message,
                'severity': alert.severity,
                'location': alert.location,
                'status': alert.status,
                'created_at': alert.created_at.isoformat(),
                'scheduled_date': alert.scheduled_date.isoformat() if alert.scheduled_date else None
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Alert creation failed: {str(e)}'}), 500

@alerts_bp.route('/verify/<int:alert_id>', methods=['POST'])
@admin_required
def verify_alert(alert_id):
    """Verify an alert (admin only)"""
    try:
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        if alert.status != 'PENDING':
            return jsonify({'error': f'Alert is already {alert.status}'}), 400
        
        # Check for duplicates in same location
        duplicate = Alert.query.filter(
            Alert.location == alert.location,
            Alert.title == alert.title,
            Alert.status.in_(['VERIFIED', 'SENT']),
            Alert.id != alert_id
        ).first()
        
        if duplicate:
            log_action(
                'ALERT_VERIFICATION_BLOCKED',
                f'Duplicate alert detected for alert {alert_id}',
                session['user_id']
            )
            return jsonify({
                'warning': 'Similar alert already exists for this location',
                'duplicate_alert_id': duplicate.id
            }), 409
        
        # Verify alert
        alert.status = 'VERIFIED'
        alert.verified_at = datetime.utcnow()
        db.session.commit()
        
        log_action(
            'ALERT_VERIFIED',
            f'Alert {alert_id} verified: {alert.title}',
            session['user_id']
        )
        
        return jsonify({
            'message': 'Alert verified successfully',
            'alert': {
                'id': alert.id,
                'title': alert.title,
                'status': alert.status,
                'verified_at': alert.verified_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Verification failed: {str(e)}'}), 500

@alerts_bp.route('/dispatch/<int:alert_id>', methods=['POST'])
@admin_required
def dispatch_alert(alert_id):
    """Dispatch verified alert to users (admin only)"""
    try:
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        if alert.status != 'VERIFIED':
            return jsonify({'error': 'Alert must be VERIFIED before dispatch'}), 400
        
        # Get users in affected location
        users = User.query.filter(
            User.location.ilike(f'%{alert.location}%'),
            User.is_admin == False
        ).all()
        
        if not users:
            return jsonify({'warning': 'No users found in affected location'}), 404
        
        # Import email service
        from email_service import send_alert_email
        
        success_count = 0
        failed_count = 0
        
        # Send emails and create logs
        for user in users:
            try:
                # Send email
                email_sent = send_alert_email(user, alert)
                
                # Create alert log
                alert_log = AlertLog(
                    alert_id=alert.id,
                    user_id=user.id,
                    email_sent=email_sent,
                    email_status='success' if email_sent else 'failed',
                    sent_at=datetime.utcnow() if email_sent else None
                )
                
                if email_sent:
                    success_count += 1
                else:
                    failed_count += 1
                    alert_log.error_message = 'Email sending failed'
                
                db.session.add(alert_log)
                
            except Exception as e:
                failed_count += 1
                alert_log = AlertLog(
                    alert_id=alert.id,
                    user_id=user.id,
                    email_sent=False,
                    email_status='failed',
                    error_message=str(e)
                )
                db.session.add(alert_log)
        
        # Update alert status
        alert.status = 'SENT'
        alert.sent_at = datetime.utcnow()
        db.session.commit()
        
        log_action(
            'ALERT_DISPATCHED',
            f'Alert {alert_id} dispatched to {len(users)} users (Success: {success_count}, Failed: {failed_count})',
            session['user_id']
        )
        
        return jsonify({
            'message': 'Alert dispatched successfully',
            'stats': {
                'total_users': len(users),
                'success': success_count,
                'failed': failed_count
            },
            'alert': {
                'id': alert.id,
                'status': alert.status,
                'sent_at': alert.sent_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Dispatch failed: {str(e)}'}), 500

@alerts_bp.route('/my-alerts', methods=['GET'])
@login_required
def get_user_alerts():
    """Get alerts for current user's location"""
    try:
        user = User.query.get(session['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get alerts for user's location
        alerts = Alert.query.filter(
            Alert.location.ilike(f'%{user.location}%'),
            Alert.status == 'SENT'
        ).order_by(Alert.sent_at.desc()).all()
        
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                'id': alert.id,
                'title': alert.title,
                'message': alert.message,
                'severity': alert.severity,
                'location': alert.location,
                'sent_at': alert.sent_at.isoformat() if alert.sent_at else None
            })
        
        return jsonify({
            'alerts': alerts_data,
            'count': len(alerts_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch alerts: {str(e)}'}), 500

@alerts_bp.route('/all', methods=['GET'])
@admin_required
def get_all_alerts():
    """Get all alerts (admin only)"""
    try:
        status_filter = request.args.get('status', '').upper()
        page = request.args.get('page', 1, type=int)
        per_page = Config.ALERTS_PER_PAGE
        
        query = Alert.query
        
        # Filter by status if provided
        if status_filter and status_filter in Config.ALERT_STATUSES:
            query = query.filter_by(status=status_filter)
        
        # Paginate
        pagination = query.order_by(Alert.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        alerts_data = []
        for alert in pagination.items:
            creator = User.query.get(alert.created_by)
            alerts_data.append({
                'id': alert.id,
                'title': alert.title,
                'message': alert.message,
                'severity': alert.severity,
                'location': alert.location,
                'status': alert.status,
                'created_by': creator.name if creator else 'Unknown',
                'created_at': alert.created_at.isoformat(),
                'verified_at': alert.verified_at.isoformat() if alert.verified_at else None,
                'sent_at': alert.sent_at.isoformat() if alert.sent_at else None,
                'scheduled_date': alert.scheduled_date.isoformat() if alert.scheduled_date else None
            })
        
        return jsonify({
            'alerts': alerts_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch alerts: {str(e)}'}), 500

@alerts_bp.route('/<int:alert_id>', methods=['GET'])
@login_required
def get_alert_details(alert_id):
    """Get detailed information about a specific alert"""
    try:
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        user = User.query.get(session['user_id'])
        
        # Non-admin can only see SENT alerts for their location
        if not user.is_admin:
            if alert.status != 'SENT' or user.location not in alert.location:
                return jsonify({'error': 'Access denied'}), 403
        
        creator = User.query.get(alert.created_by)
        
        alert_data = {
            'id': alert.id,
            'title': alert.title,
            'message': alert.message,
            'severity': alert.severity,
            'location': alert.location,
            'status': alert.status,
            'created_by': creator.name if creator else 'Unknown',
            'created_at': alert.created_at.isoformat(),
            'verified_at': alert.verified_at.isoformat() if alert.verified_at else None,
            'sent_at': alert.sent_at.isoformat() if alert.sent_at else None,
            'scheduled_date': alert.scheduled_date.isoformat() if alert.scheduled_date else None
        }
        
        # Add delivery stats for admin
        if user.is_admin:
            logs = AlertLog.query.filter_by(alert_id=alert_id).all()
            alert_data['delivery_stats'] = {
                'total': len(logs),
                'success': sum(1 for log in logs if log.email_status == 'success'),
                'failed': sum(1 for log in logs if log.email_status == 'failed')
            }
        
        return jsonify({'alert': alert_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch alert: {str(e)}'}), 500

@alerts_bp.route('/<int:alert_id>', methods=['DELETE'])
@admin_required
def delete_alert(alert_id):
    """Delete an alert (admin only)"""
    try:
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        # Only allow deletion of PENDING alerts
        if alert.status != 'PENDING':
            return jsonify({'error': 'Only PENDING alerts can be deleted'}), 400
        
        alert_title = alert.title
        db.session.delete(alert)
        db.session.commit()
        
        log_action(
            'ALERT_DELETED',
            f'Alert {alert_id} deleted: {alert_title}',
            session['user_id']
        )
        
        return jsonify({'message': 'Alert deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500

@alerts_bp.route('/stats', methods=['GET'])
@admin_required
def get_alert_stats():
    """Get alert statistics (admin only)"""
    try:
        total_alerts = Alert.query.count()
        pending = Alert.query.filter_by(status='PENDING').count()
        verified = Alert.query.filter_by(status='VERIFIED').count()
        sent = Alert.query.filter_by(status='SENT').count()
        
        severity_stats = {}
        for severity in Config.ALERT_SEVERITIES:
            severity_stats[severity] = Alert.query.filter_by(severity=severity).count()
        
        return jsonify({
            'total_alerts': total_alerts,
            'by_status': {
                'pending': pending,
                'verified': verified,
                'sent': sent
            },
            'by_severity': severity_stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch stats: {str(e)}'}), 500


"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""



