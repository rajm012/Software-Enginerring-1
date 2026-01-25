"""
Generate dummy alerts for testing the disaster management system
"""
from app import app
from models import db, Alert, User
from indian_cities import INDIAN_CITIES
import random
from datetime import datetime, timedelta

def generate_dummy_alerts():
    """Generate 50 dummy alerts across various cities"""
    
    with app.app_context():
        # Check if alerts already exist
        existing_count = Alert.query.count()
        if existing_count > 10:
            print(f"⚠️  Found {existing_count} existing alerts. Clearing them first...")
            Alert.query.delete()
            db.session.commit()
        
        # Get admin users
        admins = User.query.filter_by(is_admin=True).all()
        if not admins:
            print("❌ No admin users found. Please run generate_users.py first.")
            return
        
        # Disaster types
        disaster_types = [
            {"title": "Heavy Rainfall Warning", "message": "Heavy to very heavy rainfall expected. Stay indoors and avoid low-lying areas.", "severity": "HIGH"},
            {"title": "Flood Alert", "message": "River water levels rising. Evacuation may be necessary. Keep emergency supplies ready.", "severity": "CRITICAL"},
            {"title": "Cyclone Warning", "message": "Severe cyclonic storm approaching. Secure loose objects and stock up on essentials.", "severity": "CRITICAL"},
            {"title": "Earthquake Alert", "message": "Seismic activity detected. Stay calm, take cover under sturdy furniture.", "severity": "HIGH"},
            {"title": "Heat Wave Warning", "message": "Extreme temperatures expected. Stay hydrated and avoid outdoor activities.", "severity": "MEDIUM"},
            {"title": "Landslide Warning", "message": "Heavy rains may trigger landslides in hilly areas. Avoid travel to hills.", "severity": "HIGH"},
            {"title": "Storm Alert", "message": "Severe thunderstorms with strong winds expected. Secure outdoor items.", "severity": "MEDIUM"},
            {"title": "Drought Advisory", "message": "Water conservation measures recommended. Avoid wastage of water.", "severity": "LOW"},
            {"title": "Air Quality Alert", "message": "Poor air quality due to pollution. Vulnerable groups should stay indoors.", "severity": "MEDIUM"},
            {"title": "Fire Warning", "message": "High fire risk due to dry conditions. Avoid open flames and smoking outdoors.", "severity": "HIGH"},
            {"title": "Tsunami Warning", "message": "Move to higher ground immediately. Tsunami waves expected.", "severity": "CRITICAL"},
            {"title": "Smog Alert", "message": "Dense smog reducing visibility. Drive carefully and use headlights.", "severity": "MEDIUM"},
            {"title": "Cold Wave Warning", "message": "Severe cold wave conditions. Protect vulnerable groups and livestock.", "severity": "MEDIUM"},
            {"title": "Lightning Alert", "message": "Thunderstorm with lightning activity. Stay indoors and avoid open areas.", "severity": "HIGH"},
            {"title": "Hailstorm Warning", "message": "Hailstorm expected. Protect vehicles and stay indoors.", "severity": "MEDIUM"},
        ]
        
        # Status distribution
        statuses = ['SENT', 'SENT', 'SENT', 'VERIFIED', 'PENDING']
        
        alerts_created = 0
        
        # Generate 50 alerts
        for i in range(50):
            disaster = random.choice(disaster_types)
            city = random.choice(INDIAN_CITIES)
            admin = random.choice(admins)
            status = random.choice(statuses)
            
            # Random dates
            days_ago = random.randint(0, 30)
            created_date = datetime.now() - timedelta(days=days_ago)
            
            # Scheduled date (for future alerts)
            scheduled_date = None
            if random.random() > 0.6:  # 40% have scheduled dates
                days_ahead = random.randint(1, 7)
                scheduled_date = datetime.now() + timedelta(days=days_ahead, hours=random.randint(0, 23))
            
            alert = Alert(
                title=disaster['title'],
                message=disaster['message'],
                severity=disaster['severity'],
                location=city,
                status=status,
                created_by=admin.id,
                created_at=created_date,
                scheduled_date=scheduled_date
            )
            
            # Set verified_at and sent_at based on status
            if status == 'VERIFIED' or status == 'SENT':
                alert.verified_at = created_date + timedelta(hours=random.randint(1, 6))
            
            if status == 'SENT':
                alert.sent_at = alert.verified_at + timedelta(hours=random.randint(1, 3))
            
            try:
                db.session.add(alert)
                alerts_created += 1
            except Exception as e:
                print(f"❌ Error creating alert: {str(e)}")
                db.session.rollback()
                continue
        
        # Commit all alerts
        try:
            db.session.commit()
            print("\n" + "="*60)
            print("✅ DUMMY ALERTS CREATED SUCCESSFULLY!")
            print("="*60)
            print(f"\n📊 Summary:")
            print(f"   🚨 Total Alerts: {alerts_created}")
            
            # Count by severity
            critical = Alert.query.filter_by(severity='CRITICAL').count()
            high = Alert.query.filter_by(severity='HIGH').count()
            medium = Alert.query.filter_by(severity='MEDIUM').count()
            low = Alert.query.filter_by(severity='LOW').count()
            
            print(f"\n📈 By Severity:")
            print(f"   🔴 Critical: {critical}")
            print(f"   🟠 High: {high}")
            print(f"   🟡 Medium: {medium}")
            print(f"   🟢 Low: {low}")
            
            # Count by status
            pending = Alert.query.filter_by(status='PENDING').count()
            verified = Alert.query.filter_by(status='VERIFIED').count()
            sent = Alert.query.filter_by(status='SENT').count()
            
            print(f"\n📋 By Status:")
            print(f"   ⏳ Pending: {pending}")
            print(f"   ✅ Verified: {verified}")
            print(f"   📧 Sent: {sent}")
            
            # Count with scheduled dates
            scheduled = Alert.query.filter(Alert.scheduled_date.isnot(None)).count()
            print(f"\n⏰ Scheduled Alerts: {scheduled}")
            
            print(f"\n📍 Cities with Alerts:")
            cities = db.session.query(Alert.location).distinct().all()
            print(f"   {len(cities)} cities covered")
            
            print("\n" + "="*60)
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error committing to database: {str(e)}")

if __name__ == "__main__":
    print("\n🚀 Generating Dummy Alerts for Testing...")
    generate_dummy_alerts()


"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""


