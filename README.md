# Seth Howe Landscaping Website

A professional landscaping consulting website built with Flask, showcasing 20+ years of expertise in landscape design, hardscape installation, and arborist services.

## 🌿 Live Demo

The website is deployed and accessible at: [Your Replit URL will be here]

## 📋 Features

### Core Pages
- **Homepage**: Hero section with service overview and call-to-action
- **About Seth**: Professional biography highlighting 20+ years of experience
- **Services**: Detailed descriptions of landscape design, hardscape, and arborist services
- **Testimonials**: Authentic client reviews and satisfaction statistics
- **Gallery**: Professional project portfolio with categorized filtering
- **Contact**: Contact form with business information and service areas

### Technical Features
- Responsive Bootstrap 5 design optimized for all devices
- Professional earth-tone color scheme
- Working contact form with email integration
- Interactive gallery with modal image viewing
- Smooth animations and scroll effects
- SEO-friendly structure with proper meta tags

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **Flask-Mail** - Email functionality for contact forms
- **Gunicorn** - WSGI HTTP Server for production deployment

### Frontend
- **Bootstrap 5.3.0** - Responsive CSS framework
- **Font Awesome 6.0.0** - Professional iconography
- **Vanilla JavaScript** - Interactive functionality
- **Custom CSS** - Earth-tone styling and animations

### Deployment
- **Replit Deployments** - Hosting and domain management
- **Environment Variables** - Secure configuration management

## 📁 Project Structure

```
seth-howe-landscaping/
├── app.py                 # Main Flask application with routes
├── main.py               # Application entry point
├── templates/            # Jinja2 HTML templates
│   ├── base.html        # Base template with navigation/footer
│   ├── index.html       # Homepage
│   ├── bio.html         # About Seth page
│   ├── services.html    # Services page
│   ├── testimonials.html # Client testimonials
│   ├── gallery.html     # Project gallery
│   └── contact.html     # Contact page
├── static/              # Static assets
│   ├── css/
│   │   └── style.css   # Custom styling
│   └── js/
│       └── main.js     # Interactive functionality
├── pyproject.toml       # Python dependencies
└── replit.md           # Project documentation
```

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- pip or uv package manager

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mdmelo/seth-howe-landscaping.git
   cd seth-howe-landscaping
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export SESSION_SECRET="your-secret-key"
   export MAIL_USERNAME="your-email@gmail.com"
   export MAIL_PASSWORD="your-app-password"
   export CONTACT_EMAIL="seth@sethhowelandscaping.com"
   ```

4. Run the application:
   ```bash
   python main.py
   ```

5. Visit `http://localhost:5000` in your browser

## 📧 Email Configuration

The contact form requires SMTP configuration for email functionality:

```python
# Required environment variables
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=seth@sethhowelandscaping.com
CONTACT_EMAIL=seth@sethhowelandscaping.com
```

## 🎨 Design Philosophy

The website employs a professional earth-tone color palette that reflects the natural landscape industry:

- **Primary Green**: #2d5016 (Forest green for trust and expertise)
- **Secondary Green**: #4a7c59 (Sage green for natural appeal)
- **Accent Brown**: #8b4513 (Earth brown for stability)
- **Light Accents**: Natural beige and tan for readability

## 📱 Responsive Design

The website is fully responsive and optimized for:
- Desktop computers (1200px+)
- Tablets (768px - 1199px)
- Mobile phones (320px - 767px)

## 🔧 Key Features Implementation

### Contact Form
- Client-side validation with real-time feedback
- Service-specific message templates
- Phone number formatting
- Email confirmation system

### Gallery System
- Category-based filtering
- Modal image viewing
- Lazy loading for performance
- Mobile-optimized grid layout

### Professional Content
- Detailed service descriptions
- Authentic client testimonials
- Professional certifications and awards
- Service area coverage maps

## 🌟 Business Value

This website serves as a comprehensive digital presence for Seth Howe Landscaping:

- **Lead Generation**: Contact form and clear calls-to-action
- **Credibility**: Professional design and detailed testimonials
- **Service Education**: Comprehensive service descriptions
- **Portfolio Showcase**: Visual project gallery
- **Trust Building**: Certifications, awards, and experience highlights

## 📈 Performance Optimizations

- Optimized images with proper sizing
- Minified CSS and JavaScript
- Efficient Bootstrap component usage
- Semantic HTML structure for SEO
- Fast loading times with CDN resources

## 🔒 Security Features

- Environment variable configuration
- CSRF protection ready
- Input validation on forms
- Secure email handling
- Production-ready deployment setup

## 📞 Contact Information

For questions about this website or Seth's landscaping services:

- **Phone**: (555) 123-4567
- **Email**: seth@sethhowelandscaping.com
- **Service Area**: Greater Metro Area (50+ mile radius)

## 📄 License

This project is proprietary software developed for Seth Howe Landscaping.

## 🤝 Development Credits

Website developed using modern web technologies with focus on:
- Professional presentation
- Mobile responsiveness  
- User experience optimization
- Search engine optimization
- Performance and reliability

---

**Built with ❤️ for professional landscaping excellence**