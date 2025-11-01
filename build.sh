#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py create_superuser

# Setup initial portfolio data
echo "Setting up portfolio data..."
python manage.py setup_portfolio_data --sample-only

# Make scripts executable
chmod +x start.sh
chmod +x test_wsgi.py

# Verify Django installation and WSGI module
echo "Verifying Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"
python -c "import portfolio.wsgi; print('WSGI module imported successfully')"

echo "Build completed successfully!"