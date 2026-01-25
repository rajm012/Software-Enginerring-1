"""
Test script to verify all endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health endpoint"""
    print("\n🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_user_registration():
    """Test user registration"""
    print("\n🔍 Testing user registration...")
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123",
        "location": "Test City"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code in [200, 201, 400]  # 400 if already exists

def test_user_login():
    """Test user login"""
    print("\n🔍 Testing user login...")
    data = {
        "email": "test@example.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.cookies
    return None

def test_admin_registration():
    """Test admin registration"""
    print("\n🔍 Testing admin registration...")
    data = {
        "name": "Test Admin",
        "email": "testadmin@example.com",
        "password": "admin123",
        "location": "Admin City",
        "referral_code": "Enter yours or contact us"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register-admin", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code in [200, 201, 400]

def test_admin_login():
    """Test admin login"""
    print("\n🔍 Testing admin login...")
    data = {
        "email": "testadmin@example.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.cookies
    return None

def test_create_alert(cookies):
    """Test alert creation (admin only)"""
    print("\n🔍 Testing alert creation...")
    data = {
        "title": "Test Emergency Alert",
        "message": "This is a test alert message",
        "severity": "HIGH",
        "location": "Test City"
    }
    response = requests.post(f"{BASE_URL}/api/alerts/create", json=data, cookies=cookies)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        return response.json().get('alert', {}).get('id')
    return None

def test_verify_alert(alert_id, cookies):
    """Test alert verification"""
    print(f"\n🔍 Testing alert verification for alert {alert_id}...")
    response = requests.post(f"{BASE_URL}/api/alerts/verify/{alert_id}", cookies=cookies)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_get_my_alerts(cookies):
    """Test getting user alerts"""
    print("\n🔍 Testing get my alerts...")
    response = requests.get(f"{BASE_URL}/api/alerts/my-alerts", cookies=cookies)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_get_all_alerts(cookies):
    """Test getting all alerts (admin)"""
    print("\n🔍 Testing get all alerts...")
    response = requests.get(f"{BASE_URL}/api/alerts/all", cookies=cookies)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("  DISASTER MANAGEMENT SYSTEM - API TESTS")
    print("=" * 60)
    
    results = []
    
    # Test health check
    results.append(("Health Check", test_health_check()))
    
    # Test user flow
    results.append(("User Registration", test_user_registration()))
    user_cookies = test_user_login()
    results.append(("User Login", user_cookies is not None))
    
    # Test admin flow
    results.append(("Admin Registration", test_admin_registration()))
    admin_cookies = test_admin_login()
    results.append(("Admin Login", admin_cookies is not None))
    
    if admin_cookies:
        # Test alert creation
        alert_id = test_create_alert(admin_cookies)
        results.append(("Alert Creation", alert_id is not None))
        
        if alert_id:
            # Test alert verification
            results.append(("Alert Verification", test_verify_alert(alert_id, admin_cookies)))
        
        # Test get all alerts
        results.append(("Get All Alerts", test_get_all_alerts(admin_cookies)))
    
    if user_cookies:
        # Test get my alerts
        results.append(("Get My Alerts", test_get_my_alerts(user_cookies)))
    
    # Print results
    print("\n" + "=" * 60)
    print("  TEST RESULTS")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print("\n" + "=" * 60)
    print(f"  Total: {passed}/{total} tests passed")
    print("=" * 60)

if __name__ == '__main__':
    print("\n⚠️  Make sure the Flask server is running on http://localhost:5000")
    input("Press Enter to start tests...")
    
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server!")
        print("   Make sure Flask server is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


"""
Credits:
    Aditya & harshit: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""

