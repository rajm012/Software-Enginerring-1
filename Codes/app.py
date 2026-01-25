"""
Main Flask application entry point
"""
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from models import db, User
from config import Config
import os

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, supports_credentials=True)
    
    # Register blueprints
    from auth import auth_bp
    from alerts import alerts_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(alerts_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    # Root route - Landing page
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        try:
            # Check database connection
            db.session.execute('SELECT 1')
            db_status = 'healthy'
        except Exception as e:
            db_status = f'unhealthy: {str(e)}'
        
        return jsonify({
            'status': 'ok',
            'database': db_status
        }), 200
    
    # Cities endpoint
    @app.route('/api/cities')
    def get_cities():
        """Get list of Indian cities"""
        from indian_cities import get_cities
        return jsonify({'cities': get_cities()}), 200
    
    # Users endpoint (admin only)
    @app.route('/api/users/all')
    def get_all_users():
        """Get all users with location distribution (admin only)"""
        from auth import admin_required
        from flask import session
        
        # Check if admin
        if not session.get('user_id'):
            return jsonify({'error': 'Unauthorized'}), 401
        
        current_user = User.query.get(session['user_id'])
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get all users
        users = User.query.all()
        
        # Group by location
        location_stats = {}
        user_list = []
        
        for user in users:
            # Location statistics
            if user.location not in location_stats:
                location_stats[user.location] = {'count': 0, 'users': []}
            location_stats[user.location]['count'] += 1
            location_stats[user.location]['users'].append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'is_admin': user.is_admin
            })
            
            # User list
            user_list.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'location': user.location,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        return jsonify({
            'total_users': len(users),
            'location_stats': location_stats,
            'users': user_list
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Authentication pages
    @app.route('/login.html')
    def login_page():
        return render_template('login.html')
    
    @app.route('/register.html')
    def register_page():
        return render_template('register.html')
    
    @app.route('/register-admin.html')
    def register_admin_page():
        return render_template('register-admin.html')
    
    @app.route('/forgot-password.html')
    def forgot_password_page():
        return render_template('forgot-password.html')
    
    # Dashboard pages
    @app.route('/admin-dashboard.html')
    def admin_dashboard():
        return render_template('admin-dashboard.html')
    
    @app.route('/user-dashboard.html')
    def user_dashboard():
        return render_template('user-dashboard.html')
    
    @app.route('/users-panel.html')
    def users_panel():
        return render_template('users-panel.html')
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    print("Starting Disaster Management System")
    print("Server running at: http://localhost:5000")
    print("API Documentation: http://localhost:5000")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )


"""
Credits:
    Raj & Om: Logic, Code and Idea
    AI Chatbots: Optimization, Formatting
"""


