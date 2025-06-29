from app import create_app
import os

if __name__ == '__main__':
    # Force development mode
    os.environ['FLASK_ENV'] = 'development'
    
    # Create app in development mode
    app = create_app('development')
    
    # Run with debug enabled
    app.run(host='0.0.0.0', port=5000, debug=True)