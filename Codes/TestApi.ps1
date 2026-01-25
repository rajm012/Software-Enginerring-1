# ========================================
# API Testing Script - PowerShell
# ========================================
# This script tests all API endpoints using Invoke-RestMethod
# Make sure the Flask app is running on http://localhost:5000
# ========================================

$BASE_URL = "http://localhost:5000"
$cookies = @{}
$admin_cookies = @{}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "API Testing Script - Disaster Management System" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# ========================================
# 1. HEALTH CHECK
# ========================================
Write-Host "`n[1] Testing Health Check Endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/health" `
        -Method GET `
        -ContentType "application/json"
    Write-Host "Health Check Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 2. GET CITIES
# ========================================
Write-Host "`n[2] Testing Get Cities Endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/cities" `
        -Method GET `
        -ContentType "application/json"
    Write-Host "Cities Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 3. USER REGISTRATION
# ========================================
Write-Host "`n[3] Testing User Registration..." -ForegroundColor Yellow
try {
    $body = @{
        name = "om test"
        email = "om@test.com"
        password = "password123"
        location = "Mumbai"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "User Registration Response:" -ForegroundColor Green
    $response
    
    # Register second user
    $body2 = @{
        name = "om test 2"
        email = "om2@test.com"
        password = "password123"
        location = "Mumbai"
    } | ConvertTo-Json
    
    $response2 = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body2
    
    Write-Host "Second User Registration Response:" -ForegroundColor Green
    $response2
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 4. ADMIN REGISTRATION
# ========================================
Write-Host "`n[4] Testing Admin Registration..." -ForegroundColor Yellow
try {
    $body = @{
        name = "om admin"
        email = "om@admin.com"
        password = "adminpass123"
        location = "Mumbai"
        referral_code = "hidden"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/register-admin" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "Admin Registration Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 5. USER LOGIN
# ========================================
Write-Host "`n[5] Testing User Login..." -ForegroundColor Yellow
try {
    $body = @{
        email = "om@test.com"
        password = "password123"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -SessionVariable 'userSession'
    
    $cookies = $userSession
    Write-Host "User Login Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 6. ADMIN LOGIN
# ========================================
Write-Host "`n[6] Testing Admin Login..." -ForegroundColor Yellow
try {
    $body = @{
        email = "om@admin.com"
        password = "adminpass123"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -SessionVariable 'adminSession'
    
    $admin_cookies = $adminSession
    Write-Host "Admin Login Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 7. GET CURRENT USER
# ========================================
Write-Host "`n[7] Testing Get Current User..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/me" `
        -Method GET `
        -ContentType "application/json" `
        -WebSession $cookies
    
    Write-Host "Current User Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 8. UPDATE USER LOCATION
# ========================================
Write-Host "`n[8] Testing Update User Location..." -ForegroundColor Yellow
try {
    $body = @{
        location = "Pune"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/update-location" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -WebSession $cookies
    
    Write-Host "Update Location Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 9. CHANGE PASSWORD
# ========================================
Write-Host "`n[9] Testing Change Password..." -ForegroundColor Yellow
try {
    $body = @{
        current_password = "password123"
        new_password = "newpass123"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/change-password" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -WebSession $cookies
    
    Write-Host "Change Password Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 10. FORGOT PASSWORD - REQUEST OTP
# ========================================
Write-Host "`n[10] Testing Forgot Password - Request OTP..." -ForegroundColor Yellow
try {
    $body = @{
        email = "om@test.com"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/forgot-password" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "Forgot Password Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 11. VERIFY OTP
# ========================================
Write-Host "`n[11] Testing Verify OTP..." -ForegroundColor Yellow
Write-Host "Note: Replace '123456' with actual OTP from email" -ForegroundColor Gray
try {
    $body = @{
        email = "om@test.com"
        otp = "123456"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/verify-otp" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "Verify OTP Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 12. RESET PASSWORD WITH OTP
# ========================================
Write-Host "`n[12] Testing Reset Password with OTP..." -ForegroundColor Yellow
Write-Host "Note: Replace '123456' with actual OTP" -ForegroundColor Gray
try {
    $body = @{
        email = "om@test.com"
        otp = "123456"
        new_password = "resetpass123"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/reset-password" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "Reset Password Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 13. CREATE ALERT (Admin only)
# ========================================
Write-Host "`n[13] Testing Create Alert (admin only)..." -ForegroundColor Yellow
try {
    $body = @{
        title = "Flood Warning"
        message = "Heavy rainfall expected. Stay indoors and avoid low-lying areas."
        severity = "HIGH"
        location = "Mumbai"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/create" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -WebSession $admin_cookies
    
    Write-Host "Create Alert Response:" -ForegroundColor Green
    $response
    
    # Create another alert
    $body2 = @{
        title = "Earthquake Alert"
        message = "Minor tremors detected. Stay calm and follow safety procedures."
        severity = "MEDIUM"
        location = "Delhi"
    } | ConvertTo-Json
    
    $response2 = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/create" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body2 `
        -WebSession $admin_cookies
    
    Write-Host "Second Alert Response:" -ForegroundColor Green
    $response2
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 14. GET ALL ALERTS (Admin only)
# ========================================
Write-Host "`n[14] Testing Get All Alerts (admin only)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/all" `
        -Method GET `
        -ContentType "application/json" `
        -WebSession $admin_cookies
    
    Write-Host "All Alerts Response:" -ForegroundColor Green
    $response
    
    # With status filter
    $response2 = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/all?status=PENDING" `
        -Method GET `
        -ContentType "application/json" `
        -WebSession $admin_cookies
    
    Write-Host "Alerts with PENDING status:" -ForegroundColor Green
    $response2
    
    # With pagination
    $response3 = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/all?page=1" `
        -Method GET `
        -ContentType "application/json" `
        -WebSession $admin_cookies
    
    Write-Host "Alerts page 1:" -ForegroundColor Green
    $response3
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 15. VERIFY ALERT (Admin only)
# ========================================
Write-Host "`n[15] Testing Verify Alert (admin only)..." -ForegroundColor Yellow
Write-Host "Note: Replace '1' with actual alert ID" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/verify/1" `
        -Method POST `
        -ContentType "application/json" `
        -WebSession $admin_cookies
    
    Write-Host "Verify Alert Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 16. DISPATCH ALERT (Admin only)
# ========================================
Write-Host "`n[16] Testing Dispatch Alert (admin only)..." -ForegroundColor Yellow
Write-Host "Note: Replace '1' with actual verified alert ID" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/dispatch/1" `
        -Method POST `
        -ContentType "application/json" `
        -WebSession $admin_cookies
    
    Write-Host "Dispatch Alert Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 17. GET MY ALERTS (User)
# ========================================
Write-Host "`n[17] Testing Get My Alerts (user)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/my-alerts" `
        -Method GET `
        -ContentType "application/json" `
        -WebSession $cookies
    
    Write-Host "My Alerts Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 18. GET ALERT DETAILS
# ========================================
Write-Host "`n[18] Testing Get Alert Details..." -ForegroundColor Yellow
Write-Host "Note: Replace '1' with actual alert ID" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/1" `
        -Method GET `
        -ContentType "application/json" `
        -WebSession $cookies
    
    Write-Host "Alert Details Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 19. GET ALERT STATS (Admin only)
# ========================================
Write-Host "`n[19] Testing Get Alert Statistics (admin only)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/stats" `
        -Method GET `
        -ContentType "application/json" `
        -WebSession $admin_cookies
    
    Write-Host "Alert Stats Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 20. DELETE ALERT (Admin only)
# ========================================
Write-Host "`n[20] Testing Delete Alert (admin only - PENDING alerts only)..." -ForegroundColor Yellow
Write-Host "Note: Replace '1' with actual PENDING alert ID" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/1" `
        -Method DELETE `
        -ContentType "application/json" `
        -WebSession $admin_cookies
    
    Write-Host "Delete Alert Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 21. GET ALL USERS (Admin only)
# ========================================
Write-Host "`n[21] Testing Get All Users with location stats (admin only)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/users/all" `
        -Method GET `
        -ContentType "application/json" `
        -WebSession $admin_cookies
    
    Write-Host "All Users Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 22. LOGOUT
# ========================================
Write-Host "`n[22] Testing User Logout..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/logout" `
        -Method POST `
        -ContentType "application/json" `
        -WebSession $cookies
    
    Write-Host "User Logout Response:" -ForegroundColor Green
    $response
    
    # Admin logout
    $response2 = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/logout" `
        -Method POST `
        -ContentType "application/json" `
        -WebSession $admin_cookies
    
    Write-Host "Admin Logout Response:" -ForegroundColor Green
    $response2
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# ========================================
# 23. ERROR HANDLING TESTS
# ========================================
Write-Host "`n[23] Testing Error Handling..." -ForegroundColor Yellow

# Invalid Login
Write-Host "`n[23a] Invalid Login Test..." -ForegroundColor Gray
try {
    $body = @{
        email = "wrong@example.com"
        password = "wrongpass"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "Invalid Login Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Expected Error: $_" -ForegroundColor Yellow
}

# Duplicate Registration
Write-Host "`n[23b] Duplicate Registration Test..." -ForegroundColor Gray
try {
    $body = @{
        name = "Test User"
        email = "om@test.com"
        password = "password123"
        location = "Mumbai"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "Duplicate Registration Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Expected Error: $_" -ForegroundColor Yellow
}

# Unauthorized Access
Write-Host "`n[23c] Unauthorized Access Test..." -ForegroundColor Gray
try {
    $body = @{
        title = "Test Alert"
        message = "This should fail"
        severity = "LOW"
        location = "Mumbai"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/alerts/create" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "Unauthorized Access Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Expected Error: $_" -ForegroundColor Yellow
}

# 404 Not Found
Write-Host "`n[23d] 404 Not Found Test..." -ForegroundColor Gray
try {
    $response = Invoke-RestMethod `
        -Uri "$BASE_URL/api/nonexistent" `
        -Method GET `
        -ContentType "application/json"
    
    Write-Host "404 Test Response:" -ForegroundColor Green
    $response
} catch {
    Write-Host "Expected Error: $_" -ForegroundColor Yellow
}

# ========================================
# CLEANUP
# ========================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Testing Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
Write-Host "Note: Some tests may fail if data doesn't exist (e.g., alert IDs)" -ForegroundColor Yellow
Write-Host "Adjust IDs and data as needed based on your database state.`n" -ForegroundColor Yellow


# Credits: 
#   Raj, Om: Code, Login, Ideas
#   AI models: Refine, Formatting, Debugging