# Seth Howe Landscaping Website

## Overview

This is a professional landscaping business website for Seth Howe Landscaping, built as a Flask web application. The site serves as a digital presence for a landscape consulting business with 20+ years of experience, featuring service information, client testimonials, project gallery, and contact functionality.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default templating system)
- **CSS Framework**: Bootstrap 5.3.0 for responsive design and UI components
- **Icons**: Font Awesome 6.0.0 for consistent iconography
- **JavaScript**: Vanilla JavaScript for interactive functionality
- **Layout**: Template inheritance using a base template with block content

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM for data persistence
- **Application Structure**: Flask application with models (`models.py`) and route handlers (`app.py`)
- **Email Service**: Flask-Mail integration for contact form functionality
- **Admin Interface**: Custom admin dashboard for managing contact submissions
- **Configuration**: Environment variable-based configuration for deployment flexibility

## Key Components

### Core Application Files
- `app.py`: Main Flask application with route definitions and email configuration
- `main.py`: Application entry point for development server
- `templates/`: HTML templates using Jinja2 templating
- `static/`: Static assets (CSS, JavaScript, images)

### Page Structure
- **Homepage** (`/`): Hero section with service overview and call-to-action
- **Biography** (`/bio`): Professional background and expertise showcase
- **Services** (`/services`): Detailed service offerings and specializations
- **Testimonials** (`/testimonials`): Client reviews and success stories
- **Gallery** (`/gallery`): Project portfolio with categorized filtering
- **Contact** (`/contact`): Contact information and inquiry form

### Email Integration
- Flask-Mail configured for SMTP email sending
- Contact form processing (implementation incomplete in current codebase)
- Environment-based email configuration for security

## Data Flow

1. **User Navigation**: Users browse static pages rendered from Jinja2 templates
2. **Contact Interaction**: Contact form submissions processed through Flask route
3. **Email Processing**: Form data converted to email messages via Flask-Mail
4. **Static Content**: Images and assets served directly from static directory

## External Dependencies

### Python Packages
- `Flask`: Web framework for Python
- `Flask-Mail`: Email sending functionality

### Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework (CDN)
- **Font Awesome 6.0.0**: Icon library (CDN)

### Email Service
- SMTP server configuration (default: Gmail SMTP)
- Requires email credentials via environment variables

## Deployment Strategy

### Environment Configuration
- `SESSION_SECRET`: Flask session security key
- `MAIL_SERVER`: SMTP server address
- `MAIL_PORT`: SMTP server port
- `MAIL_USERNAME`: Email account username
- `MAIL_PASSWORD`: Email account password
- `MAIL_DEFAULT_SENDER`: Default sender email address

### Development Setup
- Development server runs on `0.0.0.0:5000` with debug mode enabled
- Static files served directly by Flask development server

### Production Considerations
- Environment variables required for email functionality
- SSL/TLS certificate needed for secure email transmission
- Consider using application server (Gunicorn, uWSGI) for production deployment

## Changelog

```
Changelog:
- June 28, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```

## Notes for Development

### Incomplete Features
- Contact form POST handler is incomplete in `app.py`
- Form validation and error handling needs implementation
- Email template creation for contact inquiries

### Potential Enhancements
- Database integration for storing contact inquiries
- Content management system for gallery and testimonials
- SEO optimization with meta tags and structured data
- Performance optimization for image loading
- Mobile-first responsive improvements

### Security Considerations
- Input validation for contact forms
- CSRF protection implementation
- Rate limiting for form submissions
- Secure email credential storage