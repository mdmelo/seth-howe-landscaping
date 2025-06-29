#!/usr/bin/env python3
"""
Database initialization script for Seth Howe Landscaping
Run this script to manually initialize the database with tables and sample data
"""

import os
import sys
from flask import Flask

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def initialize_database():
    """Initialize the database with tables and sample data"""
    print("🔧 Initializing Seth Howe Landscaping Database...")
    
    try:
        # Import the app
        from app import create_app, db
        
        # Create Flask app
        app = create_app()
        
        with app.app_context():
            print("📋 Creating database tables...")
            
            # Drop all existing tables (if any)
            db.drop_all()
            print("   ✅ Dropped existing tables")
            
            # Create all tables
            db.create_all()
            print("   ✅ Created all tables")
            
            # Add sample data
            from database import add_sample_data
            add_sample_data()
            print("   ✅ Added sample data")
            
            # Verify tables were created
            from models import ContactSubmission, Testimonial, GalleryItem, ServiceInquiry
            
            print("\n📊 Database Statistics:")
            print(f"   • Contact Submissions: {ContactSubmission.query.count()}")
            print(f"   • Testimonials: {Testimonial.query.count()}")
            print(f"   • Gallery Items: {GalleryItem.query.count()}")
            print(f"   • Service Inquiries: {ServiceInquiry.query.count()}")
            
            print("\n🎉 Database initialization completed successfully!")
            print("   You can now run the app with: python main.py")
            
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the correct directory")
        print("2. Check that all required packages are installed")
        print("3. Verify the database file permissions")
        return False
    
    return True

if __name__ == "__main__":
    success = initialize_database()
    sys.exit(0 if success else 1)