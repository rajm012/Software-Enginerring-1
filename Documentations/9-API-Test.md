# API Testing Quick Reference Guide

Complete guide for testing all API endpoints using curl commands.

## Prerequisites

1. **Start the Flask server:**
   ```powershell
   python Codes/app.py
   ```

2. **Server should be running on:** `http://localhost:5000`

3. **Have curl installed** (comes with Windows 10+, Mac, Linux)

---

## Table of Contents

1. [Health & Info Endpoints](#health--info-endpoints)
2. [Authentication Endpoints](#authentication-endpoints)
3. [User Management](#user-management)
4. [Alert Management (User)](#alert-management-user)
5. [Alert Management (Admin)](#alert-management-admin)
6. [Testing Scripts](#testing-scripts)

---

## Health & Info Endpoints

### 1. Health Check
```bash
curl -X GET http://localhost:5000/health
```

### 2. Get Cities List
```bash
curl -X GET http://localhost:5000/api/cities
```

---

## Authentication Endpoints

### 3. User Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "testuser@example.com",
    "password": "password123",
    "location": "Mumbai"
  }'
```

### 4. Admin Registration
```bash
curl -X POST http://localhost:5000/api/auth/register-admin \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "adminpass123",
    "location": "Mumbai",
    "referral_code": "ADMIN2024SECURE"
  }'
```

**Note:** Replace `ADMIN2024SECURE` with your actual referral code from `config.py`

### 5. Login (User or Admin)
```bash
# Save cookies for authenticated requests
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "testuser@example.com",
    "password": "password123"
  }'
```

### 6. Get Current User Info
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

### 7. Logout
```bash
curl -X POST http://localhost:5000/api/auth/logout \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

### 8. Forgot Password - Request OTP
```bash
curl -X POST http://localhost:5000/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com"
  }'
```

### 9. Verify OTP
```bash
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "otp": "123456"
  }'
```

### 10. Reset Password with OTP
```bash
curl -X POST http://localhost:5000/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "otp": "123456",
    "new_password": "newpassword123"
  }'
```

### 11. Change Password (Logged In)
```bash
curl -X POST http://localhost:5000/api/auth/change-password \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "current_password": "password123",
    "new_password": "newpass123"
  }'
```

---

## User Management

### 12. Update Location
```bash
curl -X POST http://localhost:5000/api/auth/update-location \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "location": "Pune"
  }'
```

### 13. Get All Users (Admin Only)
```bash
curl -X GET http://localhost:5000/api/users/all \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt
```

---

## Alert Management (User)

### 14. Get My Alerts (User's Location)
```bash
curl -X GET http://localhost:5000/api/alerts/my-alerts \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

### 15. Get Alert Details
```bash
curl -X GET http://localhost:5000/api/alerts/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

## Alert Management (Admin)

### 16. Create Alert (Admin Only)
```bash
curl -X POST http://localhost:5000/api/alerts/create \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "title": "Flood Warning",
    "message": "Heavy rainfall expected. Stay indoors.",
    "severity": "HIGH",
    "location": "Mumbai"
  }'
```

**Severity levels:** `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`

### 17. Create Scheduled Alert
```bash
curl -X POST http://localhost:5000/api/alerts/create \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "title": "Cyclone Alert",
    "message": "Cyclone expected tomorrow.",
    "severity": "CRITICAL",
    "location": "Chennai",
    "scheduled_date": "2026-01-26T10:00:00"
  }'
```

### 18. Get All Alerts (Admin Only)
```bash
# All alerts
curl -X GET http://localhost:5000/api/alerts/all \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt

# Filter by status
curl -X GET "http://localhost:5000/api/alerts/all?status=PENDING" \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt

# With pagination
curl -X GET "http://localhost:5000/api/alerts/all?page=1" \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt
```

### 19. Verify Alert (Admin Only)
```bash
curl -X POST http://localhost:5000/api/alerts/verify/1 \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt
```

### 20. Dispatch Alert (Admin Only)
```bash
curl -X POST http://localhost:5000/api/alerts/dispatch/1 \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt
```

**Note:** Alert must be VERIFIED before dispatch

### 21. Get Alert Statistics (Admin Only)
```bash
curl -X GET http://localhost:5000/api/alerts/stats \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt
```

### 22. Delete Alert (Admin Only)
```bash
curl -X DELETE http://localhost:5000/api/alerts/1 \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt
```

**Note:** Only PENDING alerts can be deleted

---

## Testing Scripts

### PowerShell (Windows)
```powershell
# Run all tests
.\Codes\test_api.ps1
```

### Bash (Linux/Mac/Git Bash)
```bash
# Make executable
chmod +x Codes/test_api.sh

# Run all tests
./Codes/test_api.sh
```

---

## Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful GET/POST/DELETE |
| 201 | Created | User/Alert created |
| 400 | Bad Request | Missing required fields |
| 401 | Unauthorized | Not logged in |
| 403 | Forbidden | Not admin when admin required |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate alert/email |
| 500 | Server Error | Internal server error |

---

## Tips

1. **Save cookies for session:**
   - Use `-c cookies.txt` to save cookies
   - Use `-b cookies.txt` to send cookies

2. **Pretty print JSON responses:**
   ```bash
   curl ... | python -m json.tool
   ```
   Or install `jq`:
   ```bash
   curl ... | jq
   ```

3. **Debug requests:**
   Add `-v` flag for verbose output:
   ```bash
   curl -v -X GET http://localhost:5000/health
   ```

4. **Test workflow:**
   1. Register user → Login → Get current user
   2. Register admin → Login → Create alert → Verify → Dispatch
   3. Login as user → Get my alerts

5. **Replace placeholders:**
   - Alert IDs: Replace `1` with actual alert ID from database
   - OTP: Get from email or server logs
   - Referral code: Check `config.py`

---

## Testing Checklist

- [ ] Health check returns OK
- [ ] User registration successful
- [ ] Admin registration with valid referral code
- [ ] User login and session created
- [ ] Admin login successful
- [ ] Get current user info
- [ ] Update user location
- [ ] Change password works
- [ ] Forgot password OTP sent
- [ ] Verify OTP successful
- [ ] Reset password with OTP
- [ ] Create alert (admin)
- [ ] Verify alert (admin)
- [ ] Dispatch alert (admin)
- [ ] Get my alerts (user)
- [ ] Get all alerts (admin)
- [ ] Alert statistics (admin)
- [ ] Get all users (admin)
- [ ] Delete alert (admin)
- [ ] Logout clears session
- [ ] Unauthorized access blocked
- [ ] Invalid login rejected
- [ ] Duplicate registration blocked

---

## Alert Workflow

```
PENDING → VERIFIED → SENT
   ↓         ↓         ↓
Create   Verify   Dispatch
(admin)  (admin)   (admin)
```

1. Admin creates alert (status: PENDING)
2. Admin verifies alert (status: VERIFIED)
3. Admin dispatches alert (status: SENT)
4. Users in location receive email
5. Users can view alert in dashboard

---

## Need Help?

- Check `Codes/app.py` for route definitions
- Check `Codes/auth.py` for authentication endpoints
- Check `Codes/alerts.py` for alert endpoints
- Check `Codes/config.py` for configuration values
- Review server logs for detailed error messages


"""
Credits:
    Harshit, Aditya, Anuj: Idea, Code, Working
    AI tools: Formatting and Refinement
"""

