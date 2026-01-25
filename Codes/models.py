"""
Database models for the Disaster Management System
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

db = SQLAlchemy()

class User(db.Model):
    """User model for regular users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    otp = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    alert_logs = db.relationship('AlertLog', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_token(self):
        """Generate password reset token"""
        self.reset_token = secrets.token_urlsafe(32)
        from datetime import timedelta
        self.reset_token_expiry = datetime.now() + timedelta(hours=1)
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verify reset token is valid and not expired"""
        if self.reset_token != token:
            return False
        if self.reset_token_expiry and datetime.now() > self.reset_token_expiry:
            return False
        return True
    
    def clear_reset_token(self):
        """Clear reset token after use"""
        self.reset_token = None
        self.reset_token_expiry = None
    
    def generate_otp(self):
        """Generate OTP for password reset"""
        import random
        from config import Config
        from datetime import timedelta
        
        self.otp = ''.join([str(random.randint(0, 9)) for _ in range(Config.OTP_LENGTH)])
        self.otp_expiry = datetime.now() + timedelta(minutes=Config.OTP_EXPIRY_MINUTES)
        return self.otp
    
    def verify_otp(self, otp):
        """Verify OTP is valid and not expired"""
        if not self.otp or self.otp != otp:
            return False
        if self.otp_expiry and datetime.now() > self.otp_expiry:
            return False
        return True
    
    def clear_otp(self):
        """Clear OTP after use"""
        self.otp = None
        self.otp_expiry = None
    
    def __repr__(self):
        return f'<User {self.email}>'


class Alert(db.Model):
    """Alert model for disaster alerts"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='PENDING')  # PENDING, VERIFIED, SENT
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    verified_at = db.Column(db.DateTime, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    scheduled_date = db.Column(db.DateTime, nullable=True)  # When disaster is expected to hit
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by])
    logs = db.relationship('AlertLog', backref='alert', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Alert {self.id}: {self.title} - {self.status}>'


class AlertLog(db.Model):
    """Log for tracking alert delivery to users"""
    __tablename__ = 'alert_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey('alerts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email_sent = db.Column(db.Boolean, default=False)
    email_status = db.Column(db.String(50), nullable=True)  # success, failed, pending
    sent_at = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<AlertLog Alert:{self.alert_id} User:{self.user_id} Status:{self.email_status}>'


class AuditLog(db.Model):
    """Audit log for tracking all system actions"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<AuditLog {self.action} at {self.timestamp}>'

"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""

