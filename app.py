"""
Render deployment compatibility layer
This file allows Render's auto-detection to work with our Django application
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

# Import Django WSGI application
from portfolio.wsgi import application

# Export as 'app' for Render's auto-detection
app = application