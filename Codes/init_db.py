"""
Database initialization and seed data script
Run this to set up the database and create sample data
"""
from app import create_app, db
from models import User, Alert, AuditLog
from datetime import datetime

def init_database():
    """Initialize database and create tables"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate (WARNING: This deletes all data!)
        print("🗑️  Dropping existing tables...")
        db.drop_all()
        
        print("📦 Creating new tables...")
        db.create_all()
        
        print("✅ Database initialized successfully!")
        
        # Optionally create sample admin
        create_sample_data = input("\nCreate sample admin account? (y/n): ")
        
        if create_sample_data.lower() == 'y':
            create_sample_admin()

def create_sample_admin():
    """Create a sample admin user"""
    app = create_app()
    
    with app.app_context():
        # Check if admin exists
        existing_admin = User.query.filter_by(email='admin@example.com').first()
        
        if existing_admin:
            print("⚠️  Sample admin already exists!")
            return
        
        # Create admin
        admin = User(
            name='System Admin',
            email='admin@example.com',
            location='System',
            is_admin=True
        )
        admin.set_password('hidden')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Sample admin created!")
        print("   Email: admin@example.com")
        print("   Password: admin123")
        print("   ⚠️  Change password after first login!")

def create_sample_users():
    """Create sample regular users"""
    app = create_app()
    
    with app.app_context():
        users_data = [
            {'name': 'John Doe', 'email': 'john@example.com', 'location': 'New York', 'password': 'user123'},
            {'name': 'Jane Smith', 'email': 'jane@example.com', 'location': 'Los Angeles', 'password': 'user123'},
            {'name': 'Bob Johnson', 'email': 'bob@example.com', 'location': 'New York', 'password': 'user123'},
        ]
        
        for user_data in users_data:
            existing = User.query.filter_by(email=user_data['email']).first()
            if not existing:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    location=user_data['location']
                )
                user.set_password(user_data['hidden'])
                db.session.add(user)
        
        db.session.commit()
        print(f"✅ Created {len(users_data)} sample users!")

def create_sample_alerts():
    """Create sample alerts"""
    app = create_app()
    
    with app.app_context():
        admin = User.query.filter_by(is_admin=True).first()
        
        if not admin:
            print("⚠️  No admin found. Create admin first!")
            return
        
        alerts_data = [
            {
                'title': 'Earthquake Warning',
                'message': 'A magnitude 5.5 earthquake has been detected. Please move to safe areas.',
                'severity': 'HIGH',
                'location': 'New York',
                'status': 'PENDING'
            },
            {
                'title': 'Flood Alert',
                'message': 'Heavy rainfall may cause flooding in low-lying areas. Stay alert.',
                'severity': 'MEDIUM',
                'location': 'Los Angeles',
                'status': 'VERIFIED'
            },
            {
                'title': 'Hurricane Watch',
                'message': 'Hurricane approaching coastal areas. Evacuate if instructed.',
                'severity': 'CRITICAL',
                'location': 'Miami',
                'status': 'SENT',
                'sent_at': datetime.now()
            }
        ]
        
        for alert_data in alerts_data:
            alert = Alert(
                title=alert_data['title'],
                message=alert_data['message'],
                severity=alert_data['severity'],
                location=alert_data['location'],
                status=alert_data['status'],
                created_by=admin.id
            )
            
            if alert_data.get('sent_at'):
                alert.sent_at = alert_data['sent_at']
            
            db.session.add(alert)
        
        db.session.commit()
        print(f"✅ Created {len(alerts_data)} sample alerts!")

if __name__ == '__main__':
    print("=" * 50)
    print("  Disaster Management System - Database Setup")
    print("=" * 50)
    
    init_database()
    
    # Ask if user wants sample data
    print("\n" + "=" * 50)
    create_users = input("Create sample users? (y/n): ")
    if create_users.lower() == 'y':
        create_sample_users()
    
    create_alerts = input("Create sample alerts? (y/n): ")
    if create_alerts.lower() == 'y':
        create_sample_alerts()
    
    print("\n✅ Setup complete!")
    print("🚀 Run 'python app.py' to start the server")


"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""


