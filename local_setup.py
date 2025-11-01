#!/usr/bin/env python
"""
Setup script for Django Portfolio Application
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}:")
        print(f"  Command: {command}")
        print(f"  Error: {e.stderr}")
        return False

def main():
    print("Django Portfolio Application Setup")
    print("=" * 40)
    
    # Check if virtual environment is recommended
    if sys.prefix == sys.base_prefix:
        print("⚠️  Warning: You're not in a virtual environment.")
        print("   It's recommended to create and activate a virtual environment first:")
        print("   python -m venv portfolio_env")
        print("   portfolio_env\\Scripts\\activate  # On Windows")
        print("   source portfolio_env/bin/activate  # On Linux/Mac")
        print()
        
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        return
    
    # Create .env file if it doesn't exist
    if not Path('.env').exists():
        print("\nCreating .env file...")
        with open('.env', 'w') as f:
            f.write("SECRET_KEY=django-insecure-change-me-in-production\n")
            f.write("DEBUG=True\n")
            f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")
        print("✓ .env file created")
    
    # Run Django migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        return
    
    if not run_command("python manage.py migrate", "Applying database migrations"):
        return
    
    # Create superuser
    print("\nCreating Django superuser...")
    print("You'll need this to access the admin panel at /admin/")
    if not run_command("python manage.py createsuperuser", "Creating superuser"):
        print("Note: You can create a superuser later with: python manage.py createsuperuser")
    
    # Populate initial data
    if not run_command("python manage.py populate_data", "Populating initial data"):
        print("Note: You can populate data later with: python manage.py populate_data")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("Note: Static files collection failed, but the app should still work in DEBUG mode")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the development server: python manage.py runserver")
    print("2. Open your browser to: http://127.0.0.1:8000")
    print("3. Access admin panel at: http://127.0.0.1:8000/admin")
    print("4. Add your content through the admin panel")
    print("\nTo add categories and content:")
    print("- Go to /admin/ and log in with your superuser account")
    print("- Add categories (Projects, Skills, etc.)")
    print("- Add content items to each category")
    print("- Update your personal information")

if __name__ == "__main__":
    main()