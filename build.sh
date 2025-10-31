#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py create_superuser

# Setup initial portfolio data
python manage.py setup_portfolio_data --sample-only

echo "Build completed successfully!"