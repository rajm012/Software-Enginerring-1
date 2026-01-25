## Production Deployment

### PythonAnywhere (Recommended for Students)

#### Step 1: Upload Files
1. Create account on [PythonAnywhere](https://www.pythonanywhere.com)
2. Go to **Files** → Upload files or use Git
3. Upload all project files to: `/home/yourusername/disaster-app/`

#### Step 2: Install Dependencies
Open **Bash console**:
```bash
cd disaster-app
pip3 install --user -r requirements.txt
```

#### Step 3: Set Environment Variables
Create `.env` file:
```bash
nano .env
```
Add your configuration:
```env
SECRET_KEY=
SENDER_EMAIL=
GMAIL_APP_PASSWORD=
FLASK_ENV=
MONGO_URI=
JWT_SECRET=
ADMIN_REFERRAL_CODE=
```
Press `Ctrl+X`, then `Y`, then `Enter` to save.

#### Step 4: Initialize Database
```bash
python3 init_db.py
```

#### Step 5: Configure Web App
1. Go to **Web** tab → **Add a new web app**
2. Choose **Manual configuration** → Python 3.10
3. Set **Source code** to: `/home/yourusername/disaster-app`
4. Click **WSGI configuration file** link

Edit WSGI file:
```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/disaster-app'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from app import app as application
```

#### Step 6: Configure Static Files
In **Web** tab, add static files mapping:
- URL: `/static/`
- Directory: `/home/yourusername/disaster-app/static/`

#### Step 7: Reload Web App
Click **Reload** button at top of Web tab.

Your app will be live at: `https://yourusername.pythonanywhere.com`


Credits ❤️: 
    Raj: For Idea
    Om: For Deploying 
    Gemini: For Formatting 
