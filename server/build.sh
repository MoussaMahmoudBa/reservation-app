#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies using pip
echo "Installing dependencies with pip..."
pip install --upgrade pip

# Install all dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!" 