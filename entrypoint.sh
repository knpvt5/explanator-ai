#!/bin/bash
# Exit on error
set -o errexit

# Activate the virtual environment
source /usr/src/app/venv/bin/activate

# Wait for the database to be ready (if needed)
# ./wait-for-it.sh db:5432 -- echo "Database is ready!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --no-input

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Start the Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn explanator_ai.wsgi:application --bind 0.0.0.0:8000
