#!/usr/bin/env python3
"""
Fuel Express - Startup Script
Run this script to start the Fuel Express application
"""

import os
import sys
from app import app, db

def create_tables():
    """Create database tables if they don't exist"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified successfully")

def main():
    """Main function to start the application"""
    print("🚀 Starting Fuel Express...")
    print("=" * 50)
    
    # Create database tables
    create_tables()
    
    # Get configuration
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print(f"🔧 Debug mode: {'ON' if debug_mode else 'OFF'}")
    print("=" * 50)
    print("📋 Default Admin Account:")
    print("   Email: admin@fuel-express.com")
    print("   Password: admin123")
    print("=" * 50)
    print("⛽ Fuel Express is ready!")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug_mode)
    except KeyboardInterrupt:
        print("\n👋 Fuel Express stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting Fuel Express: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()



