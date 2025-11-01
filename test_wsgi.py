#!/usr/bin/env python
"""
Test script to verify WSGI application can be imported correctly
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

try:
    # Test importing Django
    import django
    print(f"✓ Django imported successfully (version: {django.get_version()})")
    
    # Test importing WSGI application
    from portfolio.wsgi import application
    print("✓ WSGI application imported successfully")
    
    # Test Django setup
    django.setup()
    print("✓ Django setup completed successfully")
    
    print("\n🎉 All tests passed! WSGI application should work correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)