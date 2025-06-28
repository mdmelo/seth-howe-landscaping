import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure database
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
else:
    # Fallback for development without database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///landscaping.db"

# Initialize the app with the extension
db.init_app(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@sethhowelandscaping.com')

mail = Mail(app)

# Create database tables
with app.app_context():
    # Import models to ensure tables are created
    from models import ContactSubmission, Testimonial, GalleryItem, ServiceInquiry
    db.create_all()

@app.route('/')
def index():
    """Homepage with hero section and service overview"""
    return render_template('index.html')

@app.route('/bio')
def bio():
    """Seth Howe's professional biography page"""
    return render_template('bio.html')

@app.route('/services')
def services():
    """Detailed services page"""
    return render_template('services.html')

@app.route('/testimonials')
def testimonials():
    """Client testimonials page"""
    from models import Testimonial
    testimonials = Testimonial.query.filter_by(is_active=True).order_by(Testimonial.is_featured.desc(), Testimonial.created_at.desc()).all()
    return render_template('testimonials.html', testimonials=testimonials)

@app.route('/gallery')
def gallery():
    """Project gallery page"""
    return render_template('gallery.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')
        
        if not all([name, email, message]):
            flash('Please fill in all required fields.', 'error')
            return render_template('contact.html')
        
        try:
            # Import models here to avoid circular imports
            from models import ContactSubmission
            
            # Save to database
            contact_submission = ContactSubmission()
            contact_submission.name = name
            contact_submission.email = email
            contact_submission.phone = phone
            contact_submission.service_interest = service
            contact_submission.message = message
            contact_submission.newsletter_signup = bool(request.form.get('newsletter'))
            contact_submission.ip_address = request.environ.get('REMOTE_ADDR')
            contact_submission.user_agent = request.environ.get('HTTP_USER_AGENT')
            db.session.add(contact_submission)
            db.session.commit()
            
            # Send email notification
            contact_email = os.environ.get('CONTACT_EMAIL', 'seth@sethhowelandscaping.com')
            msg = Message(
                subject=f'New Contact Form Submission from {name}',
                recipients=[contact_email],
                body=f"""
New contact form submission:

Name: {name}
Email: {email}
Phone: {phone or 'Not provided'}
Service Interest: {service or 'Not specified'}

Message:
{message}
                """
            )
            mail.send(msg)
            
            # Send confirmation email to client
            confirmation_msg = Message(
                subject='Thank you for contacting Seth Howe Landscaping',
                recipients=[email] if email else [],
                body=f"""
Dear {name},

Thank you for contacting Seth Howe Landscaping. I have received your message and will get back to you within 24 hours.

Your message:
{message}

Best regards,
Seth Howe
Professional Landscape Consultant
20+ Years of Experience

Phone: (555) 123-4567
Email: seth@sethhowelandscaping.com
                """
            )
            mail.send(confirmation_msg)
            
            flash('Thank you for your message! I will contact you within 24 hours.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            app.logger.error(f'Error sending email: {str(e)}')
            flash('There was an error sending your message. Please try calling instead.', 'error')
    
    return render_template('contact.html')

@app.route('/admin')
def admin():
    """Admin dashboard for viewing contact submissions"""
    from models import ContactSubmission
    submissions = ContactSubmission.query.order_by(ContactSubmission.submitted_at.desc()).all()
    return render_template('admin.html', submissions=submissions)

@app.route('/admin/submissions/<int:submission_id>/update', methods=['POST'])
def update_submission_status(submission_id):
    """Update the status of a contact submission"""
    from models import ContactSubmission
    submission = ContactSubmission.query.get_or_404(submission_id)
    new_status = request.form.get('status')
    if new_status in ['new', 'contacted', 'completed']:
        submission.status = new_status
        db.session.commit()
        flash(f'Submission status updated to {new_status}', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
