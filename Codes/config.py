"""
Configuration settings for the Disaster Management System
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///disaster_management.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Gmail SMTP Email
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
    GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    
    # OTP Settings
    OTP_EXPIRY_MINUTES = 10
    OTP_LENGTH = 6
    
    # Admin
    ADMIN_REFERRAL_CODE = 'hidden'
    
    # Alert Settings
    ALERT_STATUSES = ['PENDING', 'VERIFIED', 'SENT']
    ALERT_SEVERITIES = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    # Pagination
    ALERTS_PER_PAGE = 20


"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""


