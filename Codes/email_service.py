"""
Email notification service using Gmail SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

def send_email_via_gmail(to_email, to_name, subject, html_content, text_content):
    """
    Send email via Gmail SMTP
    
    Args:
        to_email: Recipient email
        to_name: Recipient name
        subject: Email subject
        html_content: HTML email content
        text_content: Plain text email content
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Check if Gmail credentials are configured
        if not Config.GMAIL_APP_PASSWORD:
            print("Warning: Gmail app password not configured. Email not sent.")
            return False
        
        # Create message
        message = MIMEMultipart('alternative')
        message['From'] = f"Disaster Management System <{Config.SENDER_EMAIL}>"
        message['To'] = f"{to_name} <{to_email}>"
        message['Subject'] = subject
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        message.attach(part1)
        message.attach(part2)
        
        # Connect to Gmail SMTP server
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(Config.SENDER_EMAIL, Config.GMAIL_APP_PASSWORD)
            server.send_message(message)
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email to {to_email}: {str(e)}")
        return False

def send_alert_email(user, alert):
    """
    Send alert email to user via Gmail SMTP
    
    Args:
        user: User object
        alert: Alert object
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create email content
        subject = f"🚨 {alert.severity} Alert: {alert.title}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: {'#dc3545' if alert.severity == 'CRITICAL' else '#ffc107' if alert.severity == 'HIGH' else '#28a745'}; 
                           color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ padding: 20px; background-color: #f8f9fa; margin: 20px 0; border-radius: 5px; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
                .severity {{ font-weight: bold; font-size: 18px; }}
                .location {{ color: #666; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Disaster Alert</h1>
                    <p class="severity">Severity: {alert.severity}</p>
                </div>
                
                <div class="content">
                    <h2>{alert.title}</h2>
                    <p class="location">📍 Location: {alert.location}</p>
                    <p>{alert.message}</p>
                    <p><strong>Issued:</strong> {alert.sent_at.strftime('%Y-%m-%d %H:%M:%S') if alert.sent_at else 'N/A'}</p>
                </div>
                
                <div class="footer">
                    <p>This is an automated alert from the Disaster Management System.</p>
                    <p>Stay safe and follow local emergency guidelines.</p>
                    <p>You are receiving this because you are registered in the affected area: {user.location}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
        DISASTER ALERT - {alert.severity}
        
        {alert.title}
        
        Location: {alert.location}
        
        {alert.message}
        
        Issued: {alert.sent_at.strftime('%Y-%m-%d %H:%M:%S') if alert.sent_at else 'N/A'}
        
        ---
        This is an automated alert from the Disaster Management System.
        Stay safe and follow local emergency guidelines.
        """
        
        return send_email_via_gmail(user.email, user.name, subject, html_content, text_content)
            
    except Exception as e:
        print(f"Error sending alert email to {user.email}: {str(e)}")
        return False

def send_otp_email(user, otp):
    """
    Send OTP email for password reset
    
    Args:
        user: User object
        otp: One-time password (6 digits)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = "🔐 Password Reset OTP - Disaster Management System"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ padding: 20px; background-color: #f8f9fa; margin: 20px 0; border-radius: 5px; }}
                .otp-box {{ background-color: #007bff; color: white; font-size: 32px; font-weight: bold; 
                           padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0; 
                           letter-spacing: 8px; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
                .warning {{ color: #dc3545; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Password Reset OTP</h1>
                </div>
                
                <div class="content">
                    <p>Hello <strong>{user.name}</strong>,</p>
                    <p>You requested to reset your password. Use the OTP below to reset it:</p>
                    
                    <div class="otp-box">{otp}</div>
                    
                    <p><strong>This OTP will expire in 10 minutes.</strong></p>
                    <p class="warning">⚠️ Do not share this OTP with anyone!</p>
                    <p>If you didn't request this, please ignore this email and your password will remain unchanged.</p>
                </div>
                
                <div class="footer">
                    <p>Disaster Management System</p>
                    <p>This is an automated message. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Password Reset OTP
        
        Hello {user.name},
        
        You requested to reset your password. Use the OTP below:
        
        OTP: {otp}
        
        This OTP will expire in 10 minutes.
        
        ⚠️ Do not share this OTP with anyone!
        
        If you didn't request this, please ignore this email.
        
        ---
        Disaster Management System
        """
        
        return send_email_via_gmail(user.email, user.name, subject, html_content, text_content)
            
    except Exception as e:
        print(f"Error sending OTP email: {str(e)}")
        return False

def send_welcome_email(user):
    """
    Send welcome email to newly registered user
    
    Args:
        user: User object
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = "Welcome to Disaster Management System"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ padding: 20px; background-color: #f8f9fa; margin: 20px 0; border-radius: 5px; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Disaster Management System</h1>
                </div>
                
                <div class="content">
                    <p>Hello <strong>{user.name}</strong>,</p>
                    <p>Thank you for registering with our Disaster Management System!</p>
                    <p>You will receive timely alerts about disasters and emergencies in your area: <strong>{user.location}</strong></p>
                    <p>Stay safe and stay informed!</p>
                </div>
                
                <div class="footer">
                    <p>Disaster Management System</p>
                    <p>Keeping communities safe, one alert at a time.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to Disaster Management System
        
        Hello {user.name},
        
        Thank you for registering with our Disaster Management System!
        
        You will receive timely alerts about disasters and emergencies 
        in your area: {user.location}
        
        Stay safe and stay informed!
        
        ---
        Disaster Management System
        """
        
        return send_email_via_gmail(user.email, user.name, subject, html_content, text_content)
            
    except Exception as e:
        print(f"Error sending welcome email: {str(e)}")
        return False


"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""


