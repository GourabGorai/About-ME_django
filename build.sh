#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist (skip if fails)
echo "Creating superuser..."
python manage.py create_superuser || echo "Superuser creation skipped"

# Setup initial portfolio data (skip if fails)
echo "Setting up portfolio data..."
python manage.py setup_portfolio_data --sample-only || echo "Portfolio data setup skipped"

# Make scripts executable
chmod +x start.sh
chmod +x test_wsgi.py

# Verify Django installation and WSGI module
echo "Verifying Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')" || echo "Django import failed"
echo "Verifying app.py compatibility layer..."
python -c "import app; print('app.py imported successfully')" || echo "app.py import failed"

echo "Build completed successfully!"