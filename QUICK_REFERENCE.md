# PulsePoint Homecare - Quick Reference Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Setup
```bash
# Windows
setup.bat

# macOS/Linux
chmod +x setup.sh
./setup.sh
```

### Step 2: Run
```bash
python app.py
```

### Step 3: Access
- 🌐 Website: http://localhost:5000
- 📊 Admin: http://localhost:5000/admin/enquiries

---

## 📁 File Guide

| File | Purpose |
|------|---------|
| `app.py` | Flask application with all routes and database models |
| `templates/index.html` | Main website frontend with Lenis scroll |
| `templates/admin_dashboard.html` | Admin dashboard for enquiry management |
| `requirements.txt` | Python dependencies (install with `pip install -r`) |
| `.env` | Configuration file (API keys, database URL, etc.) |
| `setup.sh` / `setup.bat` | Automated setup scripts |
| `README.md` | Full project documentation |
| `SETUP_GUIDE.md` | Detailed setup and deployment guide |

---

## 🔧 Common Commands

```bash
# Activate virtual environment
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Run application
python app.py

# Install new package
pip install package-name
pip freeze > requirements.txt   # Update requirements.txt

# Create database
python
>>> from app import app, init_db
>>> init_db()
>>> exit()

# Deactivate virtual environment
deactivate
```

---

## 🌐 Website Sections

### Frontend (index.html)
- **Header**: Logo, navigation, CTA button
- **Hero**: Introduction with call-to-action buttons
- **Services**: Dynamic cards loaded from database
- **Why Us**: Trust-building features
- **Location**: Service area information
- **Contact Form**: Enquiry submission
- **Footer**: Links and copyright

### Admin Dashboard (admin_dashboard.html)
- **Statistics**: Total, pending, contacted, completed enquiries
- **Table**: List all enquiries with actions
- **Filters**: Filter by status
- **Details Modal**: View full enquiry information
- **Update Modal**: Change enquiry status
- **Pagination**: Navigate between pages

---

## 💾 Database Schema

### Service Table
```python
id (Integer)
name (String) - e.g., "Weight Check"
description (Text)
icon (String) - e.g., "⚖️"
created_at (DateTime)
updated_at (DateTime)
```

### Enquiry Table
```python
id (Integer)
name (String)
phone (String)
email (String)
service (String)
message (Text)
status (String) - pending, contacted, completed
created_at (DateTime)
updated_at (DateTime)
```

### ServiceArea Table
```python
id (Integer)
city (String) - e.g., "Kolkata"
state (String) - e.g., "West Bengal"
description (Text)
is_active (Boolean)
created_at (DateTime)
```

---

## 🔌 API Endpoints Quick Reference

### Services
```
GET /api/services
→ Returns all services as JSON array
```

### Enquiries
```
POST /api/enquiries
Body: {name, phone, email, service, message}
→ Submit new enquiry

GET /api/enquiries?page=1&status=pending
→ List enquiries (pagination, optional status filter)

GET /api/enquiries/1
→ Get single enquiry by ID

PUT /api/enquiries/1
Body: {status: "contacted"}
→ Update enquiry status
```

### Pages
```
GET /
→ Main website

GET /admin/enquiries
→ Admin dashboard
```

---

## 🎨 Customization Checklist

- [ ] Update company name in header/footer
- [ ] Change logo/colors (teal #1e7a8a, orange #ffa500)
- [ ] Modify service descriptions
- [ ] Update "Why Us" section
- [ ] Change contact form fields
- [ ] Update service areas
- [ ] Set SECRET_KEY in .env
- [ ] Configure database URL
- [ ] Change footer links

---

## 🚀 Deployment Checklist

### Before Deploying
- [ ] Set `FLASK_ENV=production`
- [ ] Generate new SECRET_KEY
- [ ] Configure production database
- [ ] Enable HTTPS/SSL
- [ ] Setup error logging
- [ ] Configure backups
- [ ] Test all forms
- [ ] Run security checks

### Deploy Command
```bash
# Heroku
git push heroku main

# AWS
ssh user@server
cd /var/www/pulsepoint
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
systemctl restart pulsepoint
```

---

## 🆘 Common Issues & Fixes

### Issue: ModuleNotFoundError
**Fix:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Fix:** Kill existing process
```bash
lsof -ti:5000 | xargs kill -9     # macOS/Linux
netstat -ano | findstr :5000      # Windows
```

### Issue: Database not found
**Fix:** Initialize database
```bash
python
>>> from app import app, init_db
>>> init_db()
>>> exit()
```

### Issue: Static files not loading
**Fix:** Ensure `templates/` folder exists with correct path

### Issue: Forms not submitting
**Fix:** Check browser console for CORS errors, verify API endpoints

---

## 📞 Support Resources

- 📖 Full docs: See `README.md` and `SETUP_GUIDE.md`
- 🐛 Debug mode: `FLASK_ENV=development` in `.env`
- 📊 Check database: Use SQLite Browser for `instance/pulsepoint.db`
- 🔍 API testing: Use Postman or curl commands

---

## 🔐 Security Quick Tips

```python
# Change this in .env
SECRET_KEY=your-new-secure-key-here

# Use strong database passwords
DATABASE_URL=postgresql://strong_user:strong_pass@host/db

# Enable HTTPS in production
# Use SSL certificates from Let's Encrypt
```

---

## 📊 Performance Tips

1. **Database**: Use PostgreSQL for production (not SQLite)
2. **Caching**: Add Flask-Caching for repeated queries
3. **Compression**: Enable gzip in Nginx/Apache
4. **CDN**: Serve static files via CDN
5. **Monitoring**: Use tools like New Relic or DataDog

---

## 🎓 Learning Resources

- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Lenis: https://github.com/darkroomengineering/lenis
- Heroku Deployment: https://devcenter.heroku.com/
- AWS Deployment: https://aws.amazon.com/

---

**Version:** 1.0.0  
**Last Updated:** February 2024  
**Project:** PulsePoint Homecare Flask Application
