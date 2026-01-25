"""
Generate dummy users for testing the disaster management system
"""
from app import app
from models import db, User
from indian_cities import INDIAN_CITIES
import random

def generate_dummy_users():
    """Generate 60 dummy users with different locations"""
    
    with app.app_context():
        # Check if dummy users already exist
        existing = User.query.filter(User.email.like('user%@test.com')).count()
        if existing > 0:
            print(f"⚠️  Found {existing} existing test users. Clearing them first...")
            User.query.filter(User.email.like('user%@test.com')).delete()
            User.query.filter(User.email.like('admin%@test.com')).delete()
            db.session.commit()
        
        # Names for variety
        first_names = [
            "Raj", "Priya", "Amit", "Sneha", "Rahul", "Anjali", "Vikram", "Pooja",
            "Arjun", "Kavya", "Sanjay", "Divya", "Karan", "Neha", "Rohit", "Shreya",
            "Aditya", "Riya", "Varun", "Isha", "Akash", "Meera", "Nikhil", "Sakshi",
            "Pranav", "Ananya", "Harsh", "Tanvi", "Siddharth", "Nidhi"
        ]
        
        last_names = [
            "Sharma", "Kumar", "Singh", "Patel", "Gupta", "Reddy", "Verma", "Joshi",
            "Nair", "Rao", "Mehta", "Shah", "Khan", "Desai", "Kapoor", "Malhotra",
            "Chopra", "Bansal", "Agarwal", "Jain", "Saxena", "Pillai", "Iyer", "Menon",
            "Pandey", "Tiwari", "Mishra", "Chauhan", "Sinha", "Bhat"
        ]
        
        users_created = 0
        admins_created = 0
        
        # Create 60 regular users
        for i in range(1, 61):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            email = f"user{i}@test.com"
            location = random.choice(INDIAN_CITIES)
            password = "hiddenforsafety"
            
            user = User(
                name=name,
                email=email,
                location=location,
                is_admin=False
            )
            user.set_password(password)
            
            try:
                db.session.add(user)
                users_created += 1
            except Exception as e:
                print(f"❌ Error creating {email}: {str(e)}")
                db.session.rollback()
                continue
        
        # Create 5 admin users from different cities
        admin_cities = random.sample(INDIAN_CITIES, 5)
        for i, city in enumerate(admin_cities, 1):
            name = f"Admin {random.choice(first_names)}"
            email = f"admin{i}@test.com"
            password = "hiddenforsafety"
            
            admin = User(
                name=name,
                email=email,
                location=city,
                is_admin=True
            )
            admin.set_password(password)
            
            try:
                db.session.add(admin)
                admins_created += 1
            except Exception as e:
                print(f"❌ Error creating {email}: {str(e)}")
                db.session.rollback()
                continue
        
        # Commit all users
        try:
            db.session.commit()
            print("\n" + "="*60)
            print("✅ DUMMY USERS CREATED SUCCESSFULLY!")
            print("="*60)
            print(f"\n📊 Summary:")
            print(f"   👥 Regular Users: {users_created}")
            print(f"   🛡️  Admin Users: {admins_created}")
            print(f"   📍 Cities covered: {len(set([u.location for u in User.query.all()]))}")
            
            print(f"\n📋 Sample Users:")
            print(f"   Regular: ")
            print(f"   Regular: ")
            print(f"   Admin: admin1@test.com")
            
            print(f"\n📍 User Distribution by City:")
            city_counts = {}
            for user in User.query.filter_by(is_admin=False).all():
                city_counts[user.location] = city_counts.get(user.location, 0) + 1
            
            # Show top 10 cities
            sorted_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for city, count in sorted_cities:
                print(f"   {city}: {count} users")
            
            print("\n" + "="*60)
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error committing to database: {str(e)}")

if __name__ == "__main__":
    print("\n🚀 Generating Dummy Users for Testing...")
    generate_dummy_users()

"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""



