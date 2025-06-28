// Seth Howe Landscaping - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initNavigation();
    initScrollEffects();
    initFormHandling();
    initGallery();
    initAnimations();
    initContactForm();
});

// Navigation functionality
function initNavigation() {
    // Active nav link highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.parentElement.classList.add('active');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Scroll effects
function initScrollEffects() {
    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Fade in animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.service-card, .testimonial-card, .gallery-item, .process-step').forEach(el => {
        observer.observe(el);
    });
}

// Form handling
function initFormHandling() {
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
            }
        });
    });
    
    // Form validation enhancement
    const inputs = document.querySelectorAll('input[required], textarea[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') && this.value.trim() !== '') {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    });
}

// Gallery functionality
function initGallery() {
    // Filter functionality for gallery tabs
    const galleryTabs = document.querySelectorAll('#galleryTabs button');
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    if (galleryTabs.length > 0) {
        galleryTabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const filter = this.getAttribute('data-bs-target').replace('#', '');
                filterGalleryItems(filter);
            });
        });
    }
    
    // Image modal functionality
    const galleryImages = document.querySelectorAll('.gallery-image');
    const modal = document.getElementById('imageModal');
    
    if (modal) {
        const modalImg = modal.querySelector('#modalImage');
        const modalTitle = modal.querySelector('#imageModalLabel');
        
        galleryImages.forEach(img => {
            img.addEventListener('click', function() {
                const src = this.getAttribute('src');
                const alt = this.getAttribute('alt');
                const overlay = this.parentElement.querySelector('.gallery-overlay');
                const title = overlay ? overlay.querySelector('h5').textContent : alt;
                
                modalImg.src = src;
                modalImg.alt = alt;
                modalTitle.textContent = title;
            });
        });
    }
    
    // Lazy loading for gallery images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Filter gallery items (for future category filtering)
function filterGalleryItems(category) {
    const items = document.querySelectorAll('.gallery-item');
    
    items.forEach(item => {
        if (category === 'all' || item.classList.contains(category)) {
            item.style.display = 'block';
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'scale(1)';
            }, 100);
        } else {
            item.style.opacity = '0';
            item.style.transform = 'scale(0.8)';
            setTimeout(() => {
                item.style.display = 'none';
            }, 300);
        }
    });
}

// Animation initialization
function initAnimations() {
    // Counter animation for statistics
    const counters = document.querySelectorAll('.stat-number');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
    
    // Stagger animation for service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// Counter animation
function animateCounter(element) {
    const target = parseInt(element.textContent.replace(/\D/g, ''));
    const duration = 2000;
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        let displayValue = Math.floor(current);
        if (element.textContent.includes('%')) {
            displayValue += '%';
        } else if (displayValue >= 100) {
            displayValue += '+';
        }
        
        element.textContent = displayValue;
    }, 16);
}

// Contact form enhancements
function initContactForm() {
    const contactForm = document.querySelector('#contact form, .contact-form form');
    
    if (contactForm) {
        // Phone number formatting
        const phoneInput = contactForm.querySelector('input[type="tel"]');
        if (phoneInput) {
            phoneInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length >= 6) {
                    value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
                } else if (value.length >= 3) {
                    value = value.replace(/(\d{3})(\d{0,3})/, '($1) $2');
                }
                e.target.value = value;
            });
        }
        
        // Service selection enhancement
        const serviceSelect = contactForm.querySelector('select[name="service"]');
        const messageTextarea = contactForm.querySelector('textarea[name="message"]');
        
        if (serviceSelect && messageTextarea) {
            serviceSelect.addEventListener('change', function() {
                const service = this.value;
                let placeholder = 'Please describe your project, property size, specific challenges, and any questions you have...';
                
                switch(service) {
                    case 'landscape-design':
                        placeholder = 'Please describe your landscape design vision, property size, current challenges, style preferences, and budget range...';
                        break;
                    case 'hardscape-design':
                        placeholder = 'Please describe your hardscape project goals, desired features (patio, walkways, retaining walls), materials preferences, and budget...';
                        break;
                    case 'arborist-services':
                        placeholder = 'Please describe your tree concerns, tree species if known, specific problems observed, and location on your property...';
                        break;
                    case 'problem-diagnosis':
                        placeholder = 'Please describe the specific problems you\'re experiencing with your lawn, garden, or trees, including symptoms and affected areas...';
                        break;
                }
                
                messageTextarea.setAttribute('placeholder', placeholder);
            });
        }
        
        // Form submission enhancement
        contactForm.addEventListener('submit', function(e) {
            // Add any additional client-side validation here
            const requiredFields = contactForm.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
                return false;
            }
        });
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    // Could implement error reporting here
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData.loadEventEnd - perfData.loadEventStart > 3000) {
                console.warn('Page load time is slow:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }
        }, 0);
    });
}
