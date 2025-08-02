#!/usr/bin/env python3
"""
Personal Blog Website - Startup Script
A simple script to run the Flask application with proper configuration.
"""

import os
import sys
from app import app, db, User

def main():
    """Main function to run the Flask application."""
    print("=" * 60)
    print("🚀 Personal Blog Website - Starting Application")
    print("=" * 60)

    # Check if required directories exist
    required_dirs = ['static/uploads', 'templates']
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"⚠️  Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)

    # Set environment variables if not already set
    if not os.environ.get('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'your-secret-key-change-in-production'

    if not os.environ.get('FLASK_ENV'):
        os.environ['FLASK_ENV'] = 'development'

    print("✅ Environment configured")
    print("✅ Directories verified")
    
    # Initialize database
    print("🗄️  Initializing database...")
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@blog.com',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created: username='admin', password='admin123'")
        else:
            print("✅ Admin user already exists")
    
    print("✅ Database initialized successfully")
    print()
    print("🌐 Starting Flask development server...")
    print("📱 Application will be available at: http://localhost:5000")
    print("👤 Default admin credentials: admin / admin123")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

    try:
        # Run the Flask application
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 