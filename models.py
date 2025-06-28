from app import db
from datetime import datetime
from sqlalchemy import text

class ContactSubmission(db.Model):
    """Model for storing contact form submissions"""
    __tablename__ = 'contact_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    service_interest = db.Column(db.String(50), nullable=True)
    message = db.Column(db.Text, nullable=False)
    newsletter_signup = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='new')  # new, contacted, completed
    
    def __repr__(self):
        return f'<ContactSubmission {self.name} - {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'service_interest': self.service_interest,
            'message': self.message,
            'newsletter_signup': self.newsletter_signup,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'status': self.status
        }

class Testimonial(db.Model):
    """Model for storing client testimonials"""
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_location = db.Column(db.String(100), nullable=True)
    service_type = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Integer, default=5)  # 1-5 stars
    testimonial_text = db.Column(db.Text, nullable=False)
    project_description = db.Column(db.String(200), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Testimonial {self.client_name} - {self.rating} stars>'

class GalleryItem(db.Model):
    """Model for storing gallery project items"""
    __tablename__ = 'gallery_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # landscape, hardscape, trees
    project_location = db.Column(db.String(100), nullable=True)
    project_year = db.Column(db.Integer, nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GalleryItem {self.title} - {self.category}>'

class ServiceInquiry(db.Model):
    """Model for tracking service inquiry analytics"""
    __tablename__ = 'service_inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(50), nullable=False)
    inquiry_source = db.Column(db.String(50), nullable=True)  # contact_form, phone, email
    inquiry_date = db.Column(db.DateTime, default=datetime.utcnow)
    follow_up_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='inquiry')  # inquiry, quote_sent, scheduled, completed, declined
    estimated_value = db.Column(db.Numeric(10, 2), nullable=True)
    actual_value = db.Column(db.Numeric(10, 2), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Link to contact submission if applicable
    contact_submission_id = db.Column(db.Integer, db.ForeignKey('contact_submissions.id'), nullable=True)
    contact_submission = db.relationship('ContactSubmission', backref='service_inquiries')
    
    def __repr__(self):
        return f'<ServiceInquiry {self.service_type} - {self.status}>'