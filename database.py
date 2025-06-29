"""Database utilities and initialization"""
import os
from flask import current_app
from app import db
from models import ContactSubmission, Testimonial, GalleryItem, ServiceInquiry

def init_database():
    """Initialize the database with tables and sample data"""
    try:
        # Create all tables
        db.create_all()
        current_app.logger.info("Database tables created successfully")
        
        # Add sample data if tables are empty
        add_sample_data()
        
    except Exception as e:
        current_app.logger.error(f"Error initializing database: {str(e)}")
        raise

def add_sample_data():
    """Add sample testimonials and gallery items if they don't exist"""
    try:
        # Check if we already have data
        if Testimonial.query.first() is None:
            sample_testimonials = [
                Testimonial(
                    client_name="Sarah & Mike Johnson",
                    client_location="Westfield",
                    service_type="Complete Landscape Design",
                    rating=5,
                    testimonial_text="Seth transformed our backyard into a beautiful oasis. His expertise and attention to detail exceeded our expectations. The design perfectly balances our need for low maintenance with stunning visual appeal.",
                    project_description="Backyard Transformation",
                    is_featured=True,
                    is_active=True
                ),
                Testimonial(
                    client_name="David Chen",
                    client_location="Downtown",
                    service_type="Property Value Enhancement",
                    rating=5,
                    testimonial_text="Professional, knowledgeable, and reliable. Seth's landscape design increased our property value significantly while creating an outdoor space we absolutely love.",
                    project_description="Front Yard Redesign",
                    is_featured=True,
                    is_active=True
                ),
                Testimonial(
                    client_name="Maria Rodriguez",
                    client_location="Oakwood",
                    service_type="Tree Care & Landscape Restoration",
                    rating=5,
                    testimonial_text="Outstanding tree care services. Seth saved our century-old oak tree and restored our entire landscape. His arborist expertise is unmatched in the area.",
                    project_description="Heritage Tree Restoration",
                    is_featured=True,
                    is_active=True
                ),
                Testimonial(
                    client_name="Jennifer & Tom Wilson",
                    client_location="Riverside",
                    service_type="Drainage Solutions & Native Plant Garden",
                    rating=5,
                    testimonial_text="We had serious drainage issues that were killing our plants. Seth's solution was both creative and effective - he designed a beautiful rain garden that solved our problems and became the focal point of our landscape.",
                    project_description="Problem-Solving Excellence",
                    is_featured=False,
                    is_active=True
                ),
                Testimonial(
                    client_name="Robert & Lisa Chang",
                    client_location="Hillcrest",
                    service_type="Sustainable Landscape Design",
                    rating=5,
                    testimonial_text="Seth created a completely sustainable landscape that requires 70% less water than our previous design. His selection of drought-tolerant native plants supports local wildlife while looking stunning.",
                    project_description="Sustainable Design Specialist",
                    is_featured=False,
                    is_active=True
                )
            ]
            
            for testimonial in sample_testimonials:
                db.session.add(testimonial)
        
        # Add sample gallery items if they don't exist
        if GalleryItem.query.first() is None:
            sample_gallery_items = [
                GalleryItem(
                    title="Complete Landscape Installation",
                    description="Residential property transformation with native plantings and sustainable design principles",
                    image_url="https://images.pexels.com/photos/1105019/pexels-photo-1105019.jpeg",
                    category="landscape",
                    project_location="Westfield",
                    project_year=2023,
                    is_featured=True,
                    is_active=True,
                    sort_order=1
                ),
                GalleryItem(
                    title="Natural Stone Patio",
                    description="Custom hardscape design with integrated planters and outdoor living space",
                    image_url="https://images.pexels.com/photos/1105019/pexels-photo-1105019.jpeg",
                    category="hardscape",
                    project_location="Downtown",
                    project_year=2023,
                    is_featured=True,
                    is_active=True,
                    sort_order=2
                ),
                GalleryItem(
                    title="Professional Tree Pruning",
                    description="Expert pruning services for tree health, safety, and aesthetic enhancement",
                    image_url="https://images.pexels.com/photos/1105019/pexels-photo-1105019.jpeg",
                    category="trees",
                    project_location="Oakwood",
                    project_year=2023,
                    is_featured=True,
                    is_active=True,
                    sort_order=3
                ),
                GalleryItem(
                    title="Sustainable Garden Design",
                    description="Water-wise landscaping with native plants and year-round interest",
                    image_url="https://images.pexels.com/photos/1105019/pexels-photo-1105019.jpeg",
                    category="landscape",
                    project_location="Hillcrest",
                    project_year=2023,
                    is_featured=False,
                    is_active=True,
                    sort_order=4
                ),
                GalleryItem(
                    title="Garden Pathway Design",
                    description="Curved walkway with natural stone and integrated lighting",
                    image_url="https://images.pexels.com/photos/1105019/pexels-photo-1105019.jpeg",
                    category="hardscape",
                    project_location="Riverside",
                    project_year=2022,
                    is_featured=False,
                    is_active=True,
                    sort_order=5
                ),
                GalleryItem(
                    title="Tree Health Assessment",
                    description="Comprehensive evaluation and treatment plan for mature trees",
                    image_url="https://images.pexels.com/photos/1105019/pexels-photo-1105019.jpeg",
                    category="trees",
                    project_location="Valley View",
                    project_year=2022,
                    is_featured=False,
                    is_active=True,
                    sort_order=6
                )
            ]
            
            for gallery_item in sample_gallery_items:
                db.session.add(gallery_item)
        
        # Commit all changes
        db.session.commit()
        current_app.logger.info("Sample data added successfully")
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding sample data: {str(e)}")
        raise

def reset_database():
    """Reset the database (drop and recreate all tables)"""
    try:
        db.drop_all()
        db.create_all()
        add_sample_data()
        current_app.logger.info("Database reset successfully")
    except Exception as e:
        current_app.logger.error(f"Error resetting database: {str(e)}")
        raise

def get_database_info():
    """Get information about the current database"""
    try:
        engine = db.engine
        
        # Get table names safely
        try:
            with engine.connect() as connection:
                if engine.dialect.name == 'sqlite':
                    result = connection.execute(db.text("SELECT name FROM sqlite_master WHERE type='table';"))
                    tables = [row[0] for row in result]
                elif engine.dialect.name == 'postgresql':
                    result = connection.execute(db.text("SELECT tablename FROM pg_tables WHERE schemaname='public';"))
                    tables = [row[0] for row in result]
                else:
                    tables = []
        except Exception:
            tables = []
        
        return {
            'url': str(engine.url).replace(str(engine.url.password), '***') if engine.url.password else str(engine.url),
            'dialect': engine.dialect.name,
            'driver': engine.dialect.driver,
            'tables': tables
        }
    except Exception as e:
        current_app.logger.error(f"Error getting database info: {str(e)}")
        return {'error': str(e)}

def get_database_stats():
    """Get database statistics"""
    try:
        stats = {}
        
        # Count records in each table
        stats['contact_submissions'] = ContactSubmission.query.count()
        stats['testimonials'] = Testimonial.query.count()
        stats['gallery_items'] = GalleryItem.query.count()
        stats['service_inquiries'] = ServiceInquiry.query.count()
        
        # Get recent activity
        recent_submissions = ContactSubmission.query.order_by(
            ContactSubmission.submitted_at.desc()
        ).limit(5).all()
        
        stats['recent_submissions'] = [
            {
                'name': sub.name,
                'email': sub.email,
                'submitted_at': sub.submitted_at.isoformat() if sub.submitted_at else None,
                'status': sub.status
            }
            for sub in recent_submissions
        ]
        
        return stats
    except Exception as e:
        current_app.logger.error(f"Error getting database stats: {str(e)}")
        return {'error': str(e)}