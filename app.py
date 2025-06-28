import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@sethhowelandscaping.com')

mail = Mail(app)

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
    return render_template('testimonials.html')

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
            # Send email notification
            msg = Message(
                subject=f'New Contact Form Submission from {name}',
                recipients=[os.environ.get('CONTACT_EMAIL', 'seth@sethhowelandscaping.com')],
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
                """
            )
            mail.send(confirmation_msg)
            
            flash('Thank you for your message! I will contact you within 24 hours.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            app.logger.error(f'Error sending email: {str(e)}')
            flash('There was an error sending your message. Please try calling instead.', 'error')
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
