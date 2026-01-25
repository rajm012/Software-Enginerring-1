"""
Authentication routes and logic for users and admins
"""
from flask import Blueprint, request, jsonify, session
from models import db, User, AuditLog
from config import Config
from functools import wraps
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def log_action(action, details=None, user_id=None):
    """Helper to log actions to audit log"""
    try:
        ip_address = request.remote_addr
        log = AuditLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Audit log error: {str(e)}")

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, ""

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        location = data['location'].strip()
        
        # Validate email
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password
        is_valid, msg = validate_password(password)
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(name=name, email=email, location=location)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        log_action('USER_REGISTERED', f'New user: {email}', user.id)
        
        return jsonify({
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'location': user.location
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/register-admin', methods=['POST'])
def register_admin():
    """Register a new admin with referral code"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'location', 'referral_code']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Verify referral code
        if data['referral_code'] != Config.ADMIN_REFERRAL_CODE:
            log_action('ADMIN_REGISTRATION_FAILED', f'Invalid referral code attempt for {data.get("email")}')
            return jsonify({'error': 'Invalid referral code'}), 403
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        location = data['location'].strip()
        
        # Validate email
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password
        is_valid, msg = validate_password(password)
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new admin
        user = User(name=name, email=email, location=location, is_admin=True)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        log_action('ADMIN_REGISTERED', f'New admin: {email}', user.id)
        
        return jsonify({
            'message': 'Admin registration successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'location': user.location,
                'is_admin': user.is_admin
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Admin registration failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user or admin"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            log_action('LOGIN_FAILED', f'Failed login attempt for {email}')
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create session
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin
        session.permanent = True
        
        log_action('LOGIN_SUCCESS', f'User logged in: {email}', user.id)
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'location': user.location,
                'is_admin': user.is_admin
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout current user"""
    user_id = session.get('user_id')
    log_action('LOGOUT', 'User logged out', user_id)
    
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current logged-in user info"""
    user = User.query.get(session['user_id'])
    
    if not user:
        session.clear()
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'location': user.location,
            'is_admin': user.is_admin
        }
    }), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset OTP"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        # Don't reveal if user exists for security
        if user:
            otp = user.generate_otp()
            db.session.commit()
            
            # Send OTP via email
            from email_service import send_otp_email
            email_sent = send_otp_email(user, otp)
            
            log_action('OTP_REQUESTED', f'OTP generated for {email}', user.id)
            
            if email_sent:
                return jsonify({
                    'message': 'OTP has been sent to your email',
                    'expires_in_minutes': 10
                }), 200
            else:
                return jsonify({'error': 'Failed to send OTP. Please try again.'}), 500
        
        # Always return success to prevent email enumeration
        return jsonify({'message': 'If email exists, OTP has been sent'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Request failed: {str(e)}'}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP for password reset"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        otp = data.get('otp', '').strip()
        
        if not email or not otp:
            return jsonify({'error': 'Email and OTP required'}), 400
        
        # Find user with email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 400
        
        # Verify OTP
        if not user.verify_otp(otp):
            log_action('OTP_VERIFICATION_FAILED', f'Invalid/expired OTP for {email}', user.id)
            return jsonify({'error': 'Invalid or expired OTP'}), 400
        
        log_action('OTP_VERIFIED', f'OTP verified for {email}', user.id)
        
        return jsonify({
            'message': 'OTP verified successfully',
            'email': email
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Verification failed: {str(e)}'}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with OTP"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        otp = data.get('otp', '').strip()
        new_password = data.get('new_password', '')
        
        if not email or not otp or not new_password:
            return jsonify({'error': 'Email, OTP, and new password required'}), 400
        
        # Validate password
        is_valid, msg = validate_password(new_password)
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 400
        
        # Verify OTP
        if not user.verify_otp(otp):
            return jsonify({'error': 'Invalid or expired OTP'}), 400
        
        # Update password
        user.set_password(new_password)
        user.clear_otp()
        db.session.commit()
        
        log_action('PASSWORD_RESET_SUCCESS', f'Password reset for {user.email}', user.id)
        
        return jsonify({'message': 'Password reset successful'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Password reset failed: {str(e)}'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change password for logged-in user"""
    try:
        data = request.get_json()
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new password required'}), 400
        
        user = User.query.get(session['user_id'])
        
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Validate new password
        is_valid, msg = validate_password(new_password)
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        log_action('PASSWORD_CHANGED', f'Password changed for {user.email}', user.id)
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Password change failed: {str(e)}'}), 500

@auth_bp.route('/update-location', methods=['POST'])
@login_required
def update_location():
    """Update user's location"""
    try:
        data = request.get_json()
        location = data.get('location', '').strip()
        
        if not location:
            return jsonify({'error': 'Location is required'}), 400
        
        if len(location) < 2:
            return jsonify({'error': 'Location must be at least 2 characters'}), 400
        
        user = User.query.get(session['user_id'])
        
        # Update location
        old_location = user.location
        user.location = location
        db.session.commit()
        
        log_action('LOCATION_UPDATED', f'Location changed from {old_location} to {location}', user.id)
        
        return jsonify({
            'message': 'Location updated successfully',
            'location': location
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Location update failed: {str(e)}'}), 500


"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""

