# 🛡️ SafeAlert - Disaster Management System

A comprehensive, real-time disaster alert and management system built with Flask. SafeAlert enables location-based disaster notifications, role-based access control, scheduled disaster alerts, and OTP-based secure authentication. Designed to keep citizens informed and safe during natural disasters across India.

---

## ✨ Features

### For End Users
- **📍 Location-Based Alerts**: Receive disaster alerts specific to your registered location
- **🔔 Real-Time Notifications**: Get instant email notifications when disasters are dispatched
- **🌍 50 Indian Cities Coverage**: Comprehensive coverage of major Indian cities with manual entry option
- **🔍 Better Filtering**: Filter alerts by severity (Critical, High, Medium, Low) and status
- **📱 Responsive Design**: Seamless experience across desktop, tablet, and mobile devices
- **🔐 Secure Auths**: Email-based registration with encrypted password storage
- **🔑 OTP Password Reset**: 6-digit OTP-based password recovery via email (10-minute validity)
- **📊 Alert History**: View complete history of all disaster alerts in your location

### For Administrators
- **⚡ Quick Alert Creation**: Create disaster alerts with type, location, severity, and description
- **⏰ Scheduled Disasters**: Set future date/time for expected disasters (cyclones, storms, etc.)
- **✅ Two-Stage Verification**: Verify alerts before dispatching to ensure accuracy
- **📧 Bulk Email Dispatch**: Send alerts to all affected users in specific locations
- **👥 User Management Panel**: View user distribution across cities and locations
- **📈 Real-Time Statistics**: Track pending, verified, and sent alerts with live dashboard
- **🔍 User Search**: Search users by name, email, or location
- **📱 Contact Access**: View user contact information for emergency coordination

### System Features
- **🗄️ SQLite Database**: Lightweight, serverless database with complete ACID compliance
- **🔒 Role-Based Access**: Separate user and admin roles with protected routes
- **📨 Gmail SMTP Integration**: Reliable email delivery using Gmail's SMTP server
- **🎨 Basic UI**: Bootstrap 5 with gradient cards and intuitive navigation
- **🌐 RESTful API**: Clean API architecture for future mobile app integration
- **📝 Comprehensive Logging**: Track all system activities and user actions
- **🧪 Test Data Generators**: Scripts to populate database with realistic test data

---

## 🛠️ Technology Stack

### Backend
- **Flask 2.3.3** - Lightweight Python web framework
- **SQLAlchemy** - Python SQL toolkit and Object-Relational Mapping (ORM)
- **SQLite** - Serverless, self-contained database engine
- **Werkzeug Security** - Password hashing and security utilities
- **Python-dotenv** - Environment variable management
- **SMTP (Gmail)** - Email delivery service

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with modern features
- **Bootstrap 5.3.0** - Responsive UI framework
- **JavaScript ES6** - Modern JavaScript with modules
- **Font Awesome** - Icon library

### Security
- **Password Hashing** - Werkzeug's pbkdf2:sha256
- **Session Management** - Flask secure sessions
- **OTP Verification** - Time-limited one-time passwords
- **CSRF Protection** - Built-in Flask security
- **Environment Variables** - Secure credential storage

---

## 📥 Installation & Setup

### Prerequisites

Ensure you have the following installed:
- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package installer - comes with Python)
- **Gmail account** with App Password enabled
- **Git** (optional, for cloning)

### Step 1: Get the Project

**Option A: Clone Repository**
```bash
git clone Software-Enginerring-1
cd Software-Enginerring-1
```

**Option B: Download ZIP**
1. Download the project ZIP file
2. Extract to your desired location
3. Navigate to the project directory

### Step 2: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```
---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root directory:

```env
SECRET_KEY=
SENDER_EMAIL=
GMAIL_APP_PASSWORD=
FLASK_ENV=
MONGO_URI=
JWT_SECRET=
ADMIN_REFERRAL_CODE=

# A .env.example is given for your refrence
```

### Setting Up Gmail App Password

To enable email functionality, you need a Gmail App Password:

1. **Enable 2-Factor Authentication**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable **2-Step Verification**

2. **Generate App Password**
   - Go to **App Passwords** section
   - Select **Mail** as the app
   - Select **Other (Custom name)** as the device
   - Name it "SafeAlert" or "Disaster System"
   - Click **Generate**

3. **Copy Password**
   - Copy the 16-character password (without spaces)
   - Paste it in `.env` file as `GMAIL_APP_PASSWORD`

### Configuration Details

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Flask session encryption key | N/A | ✅ Yes |
| `FLASK_ENV` | Environment mode | development | ✅ Yes |
| `SENDER_EMAIL` | Gmail address for sending emails | N/A | ✅ Yes |
| `GMAIL_APP_PASSWORD` | Gmail App Password | N/A | ✅ Yes |
| `ADMIN_REFERRAL_CODE` | Code required for admin registration | AllIsGood | ✅ Yes |

---

## 🗄️ Database Setup

### Initialize Database

Create the SQLite database and all required tables:

```bash
python init_db.py
```

**Expected Output:**
```
✅ Database initialized successfully!
📊 Tables created: users, alerts
```

### Database Schema

**Users Table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    location VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    otp_code VARCHAR(6),
    otp_expiry DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Alerts Table:**
```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disaster_type VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    scheduled_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Seed Test Data (Optional)

Populate the database with realistic test data:

**Generate 65 Test Users:**
```bash
python generate_users.py
```
- Creates **60 regular users** + **5 admins**
- Distributed across **43 Indian cities**
- Includes names, emails, and locations

**Generate 50 Test Alerts:**
```bash
python generate_alerts.py
```
- Creates **50 disaster alerts**
- Covers **15 disaster types** (floods, cyclones, earthquakes, etc.)
- Random severity distribution
- **19 alerts** with scheduled future dates

**Test Credentials Created:**
- **Users:** user1@test.com through user60@test.com (password: password1 - password60)
- **Admins:** admin1@test.com through admin5@test.com (password: admin1123 - admin5123)

---

## 🚀 Running the Application

### Start the Flask Server

```bash
python app.py
```

**Expected Output:**
```
Starting SafeAlert System
Server running at: http://localhost:5000
```

### Access the Application

Open your web browser and navigate to:

- **🏠 Home Page:** http://localhost:5000/
- **👤 User Registration:** http://localhost:5000/register
- **🔧 Admin Registration:** http://localhost:5000/register-admin
- **🔑 Login:** http://localhost:5000/login
- **🔒 Forgot Password:** http://localhost:5000/forgot-password

### Server Configuration

By default, the application runs on:
- **Host:** 127.0.0.1 (localhost)
- **Port:** 5000
- **Debug Mode:** Enabled in development

---

## 👤 User Guide

### Registration

1. Navigate to **Register** page
2. Fill in the registration form:
   - **Full Name:** Your name
   - **Email:** Valid email address
   - **Password:** Strong password (min 6 characters)
   - **Location:** Choose from 50 Indian cities or enter manually
3. Click **Register**
4. Login with your credentials

### Viewing Alerts

1. **Login** to your account
2. **Dashboard** shows all alerts for your location
3. **Filter alerts** by:
   - **Severity:** Critical, High, Medium, Low
   - **Status:** Pending, Verified, Sent

### Updating Location

1. Go to **Dashboard**
2. Find the **Your Location** card
3. Select new city from dropdown (or enter manually)
4. Click **Update Location**
5. You'll now receive alerts for the new location

### Password Recovery

1. Click **Forgot Password** on login page
2. Enter your registered email
3. Check email for **6-digit OTP**
4. Enter OTP within **10 minutes**
5. Set your new password
6. Login with new credentials

---

## 🔧 Admin Guide

### Admin Registration

1. Navigate to **Admin Registration** page
2. Fill in the form:
   - **Full Name**
   - **Email**
   - **Password**
   - **Location**
   - **Referral Code:** `AllIsGood` (required)
3. Click **Register as Admin**

### Creating Disaster Alerts

1. **Login** as admin
2. Go to **Admin Dashboard**
3. Fill in the **Create Alert** form:
   - **Disaster Type:** Select from dropdown (Flood, Cyclone, Earthquake, etc.)
   - **City:** Choose from 50 Indian cities
   - **Severity:** Critical, High, Medium, or Low
   - **Description:** Detailed information (min 10 characters)
   - **Scheduled Date/Time:** (Optional) When disaster is expected
4. Click **Create Alert**
5. Alert status: **PENDING**

### Verifying Alerts

1. Find alert with status **PENDING**
2. Review alert details
3. Click **Verify** button
4. Alert status changes to **VERIFIED**

### Dispatching Alerts

1. Find alert with status **VERIFIED**
2. Click **Dispatch** button
3. System sends emails to all users in that location
4. Alert status changes to **SENT**

### Scheduled Alerts

- Alerts with **scheduled dates** show a **⚠️ warning icon**
- Use datetime picker to set precise time
- Useful for predicted disasters (cyclones, storms)
- Format: `YYYY-MM-DD HH:MM`

### Managing Users

1. Navigate to **Users Panel** (admin only)
2. View **user distribution** across cities
3. **Search users** by name, email, or location
4. Click user card to view **contact information**
5. See statistics on user locations

---

## 📡 API Documentation
Open the Documentations folder and see the RestApiDocs.html for all API related stuffs.

---

## 📁 Project Structure

```
Assignment-1/
│
├── app.py                      # Main Flask application
├── models.py                   # SQLAlchemy database models
├── auth.py                     # Authentication routes (login, register, OTP)
├── alerts.py                   # Alert management routes (CRUD operations)
├── email_service.py            # Email/OTP service using Gmail SMTP
├── indian_cities.py            # List of 50 Indian cities
├── init_db.py                  # Database initialization script
├── generate_users.py           # Test user data generator (65 users)
├── generate_alerts.py          # Test alert data generator (50 alerts)
│
├── .env                        # Environment variables (create this)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── TESTING.txt                 # Testing checklist (65 test cases)
├── DEPLOYMENT.md               # Deployment guide
│
├── templates/                  # HTML templates
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── register.html          # User registration
│   ├── register-admin.html    # Admin registration
│   ├── forgot-password.html   # Password recovery
│   ├── user-dashboard.html    # User dashboard
│   ├── admin-dashboard.html   # Admin dashboard
│   └── users-panel.html       # User management panel (admin)
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       ├── config.js          # API endpoints configuration
│       ├── api.js             # API service layer
│       └── utils.js           # Utility functions
│
└── instance/                   # Instance folder (auto-created)
    └── disaster_management.db  # SQLite database
```

---

## 🧪 Testing

### Manual Testing

Use the comprehensive **TESTING.txt** file which includes:

- ✅ **65 Test Cases** across 10 categories
- 🔐 Authentication tests (registration, login, OTP)
- 👤 User dashboard tests (location, filters, alerts)
- 🔧 Admin dashboard tests (create, verify, dispatch)
- 👥 User management tests
- 📧 Email functionality tests
- 🎨 UI/UX tests (responsive, colors, accessibility)
- 🔌 API endpoint tests
- 🔒 Security tests
- ⚠️ Error handling tests

**Test Credentials:**
- User: `user1@test.com` / `password1`
- Admin: `admin1@test.com` / `admin1123`

### Running Test Data Scripts

**Test Users:**
```bash
python generate_users.py
```

**Test Alerts:**
```bash
python generate_alerts.py
```

### API Testing with cURL

**Test Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user1@test.com","password":"password1"}'
```
---

## 🌐 Deployment

### PythonAnywhere (Recommended for Students)

Detailed deployment instructions are available in **Documentations/DEPLOYMENT.md**.

**Quick Steps:**

1. **Upload files** to PythonAnywhere
2. **Install dependencies:** `pip3 install --user -r requirements.txt`
3. **Create .env file** with production credentials
4. **Initialize database:** `python3 init_db.py`
5. **Seed data:** 
   ```bash
   python3 generate_users.py
   python3 generate_alerts.py
   ```
6. **Configure WSGI** file
7. **Add static files mapping**
8. **Reload web app**

Your app will be live at: `https://rajm012.pythonanywhere.com`

### Production Considerations

- ✅ Change `SECRET_KEY` to a strong random value
- ✅ Set `FLASK_ENV=production`
- ✅ Use PostgreSQL/MySQL instead of SQLite for better performance
- ✅ Enable HTTPS/SSL
- ✅ Set up proper logging
- ✅ Configure CORS if needed
- ✅ Implement rate limiting
- ✅ Set up backup strategy for database

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions

---

## 📄 License

This project is licensed under the **MIT License** - free to use for educational purposes.

---

## 👨‍💻 Author

**By Group 1**
**Created for Software Engineering Assignment**  

---

## 📞 Support

For issues and questions:
2. Review **TESTING.txt** for testing guidance
1. Consult **DEPLOYMENT.md** for deployment help

---

## 🎯 Future Enhancements

Potential features for future versions:
- 📱 Mobile app (React Native/Flutter)
- 🗺️ Interactive disaster map with Google Maps
- 📊 Analytics dashboard with charts
- 🔔 SMS notifications integration
- 🌐 Multi-language support (Hindi, regional languages)
- 🤖 AI-powered disaster prediction
- 📡 Real-time weather API integration
- 🚨 Emergency contact management
- 📱 Push notifications (web push)
- 🗃️ PostgreSQL database migration

---

<div align="center">

### ⚡ Stay Safe with SafeAlert ⚡

**Built with ❤️ for disaster preparedness and public safety**

</div>
