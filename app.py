import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    mail = Mail(app)
    
    # Store mail instance for use in routes
    app.mail = mail
    
    # Register routes
    register_routes(app)
    
    # Initialize database
    with app.app_context():
        try:
            from database import init_database
            init_database()
        except Exception as e:
            app.logger.error(f"Database initialization failed: {str(e)}")
    
    return app

def register_routes(app):
    """Register all application routes"""
    
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
        try:
            testimonials = Testimonial.query.filter_by(is_active=True).order_by(
                Testimonial.is_featured.desc(), 
                Testimonial.created_at.desc()
            ).all()
        except Exception as e:
            app.logger.error(f"Error fetching testimonials: {str(e)}")
            testimonials = []
        return render_template('testimonials.html', testimonials=testimonials)

    @app.route('/gallery')
    def gallery():
        """Project gallery page"""
        from models import GalleryItem
        try:
            gallery_items = GalleryItem.query.filter_by(is_active=True).order_by(
                GalleryItem.is_featured.desc(),
                GalleryItem.sort_order.asc(),
                GalleryItem.created_at.desc()
            ).all()
        except Exception as e:
            app.logger.error(f"Error fetching gallery items: {str(e)}")
            gallery_items = []
        return render_template('gallery.html', gallery_items=gallery_items)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        """Contact page with form handling"""
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            service = request.form.get('service', '').strip()
            message = request.form.get('message', '').strip()
            newsletter = bool(request.form.get('newsletter'))
            
            # Validate required fields
            if not all([name, email, message]):
                flash('Please fill in all required fields.', 'error')
                return render_template('contact.html')
            
            try:
                from models import ContactSubmission
                
                # Save to database
                contact_submission = ContactSubmission(
                    name=name,
                    email=email,
                    phone=phone or None,
                    service_interest=service or None,
                    message=message,
                    newsletter_signup=newsletter,
                    ip_address=request.environ.get('REMOTE_ADDR'),
                    user_agent=request.environ.get('HTTP_USER_AGENT')
                )
                
                db.session.add(contact_submission)
                db.session.commit()
                
                # Send email notifications
                try:
                    send_contact_emails(app, name, email, phone, service, message)
                except Exception as email_error:
                    app.logger.error(f'Email sending failed: {str(email_error)}')
                    # Don't fail the form submission if email fails
                
                flash('Thank you for your message! I will contact you within 24 hours.', 'success')
                return redirect(url_for('contact'))
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'Error processing contact form: {str(e)}')
                flash('There was an error processing your message. Please try calling instead.', 'error')
        
        return render_template('contact.html')

    @app.route('/admin')
    def admin():
        """Admin dashboard for viewing contact submissions"""
        from models import ContactSubmission
        try:
            submissions = ContactSubmission.query.order_by(
                ContactSubmission.submitted_at.desc()
            ).all()
        except Exception as e:
            app.logger.error(f"Error fetching submissions: {str(e)}")
            submissions = []
        return render_template('admin.html', submissions=submissions)

    @app.route('/admin/submissions/<int:submission_id>/update', methods=['POST'])
    def update_submission_status(submission_id):
        """Update the status of a contact submission"""
        from models import ContactSubmission
        try:
            submission = ContactSubmission.query.get_or_404(submission_id)
            new_status = request.form.get('status')
            if new_status in ['new', 'contacted', 'completed']:
                submission.status = new_status
                db.session.commit()
                flash(f'Submission status updated to {new_status}', 'success')
            else:
                flash('Invalid status value', 'error')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating submission status: {str(e)}")
            flash('Error updating submission status', 'error')
        
        return redirect(url_for('admin'))

    @app.route('/api/database-info')
    def database_info():
        """API endpoint to get database information"""
        try:
            from database import get_database_info
            info = get_database_info()
            return jsonify(info)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/database-stats')
    def database_stats():
        """API endpoint to get database statistics"""
        try:
            from database import get_database_stats
            stats = get_database_stats()
            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        try:
            # Test database connection
            db.session.execute(db.text('SELECT 1'))
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': db.func.now()
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }), 500

    @app.route('/admin/reset-database', methods=['POST'])
    def reset_database():
        """Reset database with sample data (development only)"""
        if app.config.get('DEBUG'):
            try:
                from database import reset_database
                reset_database()
                flash('Database reset successfully with sample data', 'success')
            except Exception as e:
                app.logger.error(f"Error resetting database: {str(e)}")
                flash('Error resetting database', 'error')
        else:
            flash('Database reset is only available in development mode', 'error')
        
        return redirect(url_for('admin'))

def send_contact_emails(app, name, email, phone, service, message):
    """Send contact form notification emails"""
    try:
        # Send notification to business owner
        contact_email = app.config.get('CONTACT_EMAIL', 'seth@sethhowelandscaping.com')
        
        business_msg = Message(
            subject=f'New Contact Form Submission from {name}',
            recipients=[contact_email],
            body=f"""
New contact form submission received:

Name: {name}
Email: {email}
Phone: {phone or 'Not provided'}
Service Interest: {service or 'Not specified'}

Message:
{message}

---
This message was sent from the Seth Howe Landscaping website contact form.
            """.strip()
        )
        
        app.mail.send(business_msg)
        
        # Send confirmation email to client
        if email:
            confirmation_msg = Message(
                subject='Thank you for contacting Seth Howe Landscaping',
                recipients=[email],
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
Website: www.sethhowelandscaping.com

---
This is an automated confirmation email. Please do not reply to this message.
                """.strip()
            )
            
            app.mail.send(confirmation_msg)
            
    except Exception as e:
        app.logger.error(f'Error sending emails: {str(e)}')
        raise

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)