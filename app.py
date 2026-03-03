from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///pulsepoint.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Initialize Database
# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# ===== MODELS =====
class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Service(db.Model):
    """Service model for storing service information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon
        }


class Enquiry(db.Model):
    """Enquiry model for storing customer enquiries"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, contacted, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'service': self.service,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class ServiceArea(db.Model):
    """Service Area model"""
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False, unique=True)
    state = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'state': self.state,
            'description': self.description,
            'is_active': self.is_active
        }


# ===== ROUTES =====

@app.route('/')
def index():
    """Home page - render main website"""
    services = Service.query.all()
    service_areas = ServiceArea.query.filter_by(is_active=True).all()
    return render_template('index.html', services=services, service_areas=service_areas)


@app.route('/api/services', methods=['GET'])
def get_services():
    """API endpoint to get all services"""
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services])


@app.route('/api/enquiries', methods=['POST'])
def submit_enquiry():
    """API endpoint to submit enquiry"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'email', 'service', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create new enquiry
        enquiry = Enquiry(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            service=data['service'],
            message=data['message']
        )
        
        db.session.add(enquiry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Your enquiry has been submitted successfully',
            'enquiry_id': enquiry.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/enquiries/<int:enquiry_id>', methods=['GET'])
@login_required
def get_enquiry(enquiry_id):
    """Get single enquiry by ID"""
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    return jsonify(enquiry.to_dict())


@app.route('/api/enquiries/<int:enquiry_id>', methods=['PUT'])
@login_required
def update_enquiry(enquiry_id):
    """Update enquiry status"""
    try:
        enquiry = Enquiry.query.get_or_404(enquiry_id)
        data = request.get_json()
        
        if 'status' in data:
            enquiry.status = data['status']
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Enquiry updated successfully',
            'enquiry': enquiry.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/enquiries/<int:enquiry_id>', methods=['DELETE'])
@login_required
def delete_enquiry(enquiry_id):
    """Delete enquiry"""
    try:
        enquiry = Enquiry.query.get_or_404(enquiry_id)
        db.session.delete(enquiry)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Enquiry deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/enquiries', methods=['GET'])
@login_required
def get_all_enquiries():
    """Get all enquiries (for admin dashboard)"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', None)
    
    query = Enquiry.query
    if status:
        query = query.filter_by(status=status)
    
    enquiries = query.order_by(Enquiry.created_at.desc()).paginate(page=page, per_page=20)
    
    return jsonify({
        'enquiries': [e.to_dict() for e in enquiries.items],
        'total': enquiries.total,
        'pages': enquiries.pages,
        'current_page': page
    })


@app.route('/api/service-areas', methods=['GET'])
def get_service_areas():
    """Get all active service areas"""
    areas = ServiceArea.query.filter_by(is_active=True).all()
    return jsonify([area.to_dict() for area in areas])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        
        flash('Invalid username or password')
        
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin/enquiries')
@login_required
def admin_dashboard():
    """Admin dashboard for viewing enquiries"""
    return render_template('admin_dashboard.html')


# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ===== CONTEXT PROCESSOR =====

@app.context_processor
def inject_config():
    """Inject configuration into templates"""
    return {
        'app_name': 'PulsePoint Homecare',
        'current_year': datetime.now().year
    }


# ===== INITIALIZATION =====

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if services already exist
        if Service.query.first() is None:
            services = [
                Service(
                    name='Weight Check',
                    description='Regular weight monitoring at home with professional assessment and personalized health recommendations.',
                    icon='⚖️'
                ),
                Service(
                    name='Blood Pressure Check',
                    description='Accurate BP monitoring and tracking with expert guidance for hypertension management and prevention.',
                    icon='💓'
                ),
                Service(
                    name='Injection Service',
                    description='Safe and sterile injection administration at home by trained healthcare professionals.',
                    icon='💉'
                ),
                Service(
                    name='First Aid Service',
                    description='Emergency first aid support available for sudden illnesses and injuries with quick response time.',
                    icon='🚑'
                )
            ]
            
            for service in services:
                db.session.add(service)
            
            db.session.commit()
        
        # Check if service areas exist
        if ServiceArea.query.first() is None:
            areas = [
                ServiceArea(
                    city='Kolkata',
                    state='West Bengal',
                    description='Serving entire Kolkata and surrounding areas'
                )
            ]
            
            for area in areas:
                db.session.add(area)
            
            db.session.commit()
        
        # Check if admin user exists
        if User.query.first() is None:
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created (admin/admin123)")
        
        print("Database initialized successfully!")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
