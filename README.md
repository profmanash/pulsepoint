# PulsePoint Homecare - Healthcare Website with Flask Backend

A modern, professional healthcare service website built with Flask, featuring a smooth Lenis scroll experience, database-driven enquiry management, and an admin dashboard.

## 🎯 Features

### Frontend
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Smooth Scrolling**: Integrated Lenis library for premium scroll experience
- **Modern UI**: Beautiful gradients, animations, and interactive elements
- **Service Cards**: Dynamic service listing with database integration
- **Contact Form**: Real-time form submission with validation
- **Toast Notifications**: Elegant success/error messages
- **Accessibility**: Semantic HTML and ARIA labels

### Backend
- **Flask REST API**: Clean, RESTful API for all operations
- **SQLAlchemy ORM**: Robust database management
- **Multiple Database Support**: SQLite, PostgreSQL, MySQL
- **Enquiry Management**: Complete CRUD operations
- **Database Migrations**: Flask-Migrate for schema management
- **Environment Configuration**: Secure configuration management

### Admin Dashboard
- **Enquiry Management**: View and manage all customer enquiries
- **Status Tracking**: pending → contacted → completed
- **Filtering & Search**: Filter by status and date
- **Statistics**: Real-time stats on enquiries
- **Pagination**: Handle large datasets efficiently
- **Modal Details**: View full enquiry details inline
- **Data Export Ready**: Easy integration with export tools

## 🚀 Quick Start

### Windows Users
```bash
setup.bat
```

### macOS/Linux Users
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

**Access the application:**
- 🌐 Website: http://localhost:5000
- 📊 Admin Dashboard: http://localhost:5000/admin/enquiries

## 📁 Project Structure

```
pulsepoint/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Configuration file
├── setup.sh                    # Linux/Mac setup script
├── setup.bat                   # Windows setup script
├── SETUP_GUIDE.md             # Detailed setup documentation
├── README.md                   # This file
├── templates/
│   ├── index.html             # Main website frontend
│   └── admin_dashboard.html   # Admin dashboard
└── instance/
    └── pulsepoint.db          # SQLite database (auto-created)
```

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Flask Settings
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here

# Database (choose one)
DATABASE_URL=sqlite:///pulsepoint.db
# DATABASE_URL=postgresql://user:pass@localhost/pulsepoint
# DATABASE_URL=mysql+pymysql://user:pass@localhost/pulsepoint
```

## 📋 API Endpoints

### Public Endpoints
```
GET  /                    → Main website
GET  /api/services        → List all services
POST /api/enquiries       → Submit new enquiry
GET  /api/service-areas   → List service areas
```

### Admin Endpoints
```
GET  /admin/enquiries              → Admin dashboard
GET  /api/enquiries                → List all enquiries (paginated)
GET  /api/enquiries/<id>           → Get enquiry details
PUT  /api/enquiries/<id>           → Update enquiry status
```

## 🗄️ Database Models

### Service
- `id`: Primary key
- `name`: Service name
- `description`: Detailed description
- `icon`: Emoji icon
- `created_at`, `updated_at`: Timestamps

### Enquiry
- `id`: Primary key
- `name`: Customer name
- `phone`: Phone number
- `email`: Email address
- `service`: Requested service
- `message`: Customer message
- `status`: pending | contacted | completed
- `created_at`, `updated_at`: Timestamps

### ServiceArea
- `id`: Primary key
- `city`: City name
- `state`: State/Province
- `description`: Area description
- `is_active`: Active status

## 🎨 Customization

### Change Services
Add/edit services in the database:
```python
from app import app, db, Service

with app.app_context():
    service = Service(
        name='New Service',
        description='Service description',
        icon='💉'
    )
    db.session.add(service)
    db.session.commit()
```

### Modify Styling
Edit the `<style>` section in `templates/index.html`:
- Color scheme: Search for `#1e7a8a` (teal)
- Fonts: Update `font-family` declarations
- Spacing: Adjust `padding` and `margin` values

### Add New Sections
Create new HTML sections in `templates/index.html` and add routes in `app.py`

## 🔒 Security Features

- **Environment Variables**: Sensitive data in `.env`
- **CSRF Protection Ready**: Can add Flask-WTF
- **Input Validation**: Server-side validation on all endpoints
- **SQL Injection Prevention**: SQLAlchemy parameterized queries
- **HTTPS Ready**: Works with reverse proxies (Nginx, Apache)

### Production Security Checklist
- [ ] Change SECRET_KEY in .env
- [ ] Set FLASK_ENV=production
- [ ] Use PostgreSQL/MySQL instead of SQLite
- [ ] Enable HTTPS with SSL certificates
- [ ] Add CORS protection if needed
- [ ] Setup database backups
- [ ] Enable logging and monitoring
- [ ] Use environment-specific .env files

## 📦 Dependencies

- **Flask 2.3.3**: Web framework
- **Flask-SQLAlchemy 3.0.5**: ORM for databases
- **Flask-Migrate 4.0.4**: Database migrations
- **SQLAlchemy 2.0.21**: SQL toolkit
- **python-dotenv 1.0.0**: Environment variables
- **Lenis**: Client-side smooth scroll library (CDN)

## 🚀 Deployment

### Heroku
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Install gunicorn
pip install gunicorn
pip freeze > requirements.txt

# Deploy
heroku create app-name
git push heroku main
```

### AWS EC2
See SETUP_GUIDE.md for detailed AWS deployment instructions

### Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

Run:
```bash
docker build -t pulsepoint .
docker run -p 8000:8000 pulsepoint
```

## 📊 Admin Dashboard Features

### Enquiry Management
- View all customer enquiries in a table
- Filter by status (pending, contacted, completed)
- View detailed enquiry information
- Update enquiry status
- Pagination for large datasets
- Real-time statistics

### Statistics
- Total enquiries count
- Pending enquiries
- Contacted enquiries
- Completed enquiries

## 🐛 Troubleshooting

### Port 5000 already in use
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database not creating
```python
python
>>> from app import app, init_db
>>> init_db()
```

### Virtual environment issues
Delete `venv` folder and reinstall:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📞 Support & Contact

For issues or questions:
- Email: support@pulsepointhocare.com
- Website: www.pulsepointhocare.com
- Admin Dashboard: /admin/enquiries

## 📄 License

This project is proprietary. All rights reserved.

---

**Built with ❤️ for PulsePoint Homecare**

**Last Updated:** February 2024
**Version:** 1.0.0
