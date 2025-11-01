#!/usr/bin/env bash

echo "Starting Django application..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=portfolio.settings

# Verify the WSGI application can be imported
echo "Testing WSGI application import..."
python test_wsgi.py

if [ $? -eq 0 ]; then
    echo "WSGI test passed, starting Gunicorn..."
    exec gunicorn -c gunicorn.conf.py portfolio.wsgi:application
else
    echo "WSGI test failed, exiting..."
    exit 1
fi