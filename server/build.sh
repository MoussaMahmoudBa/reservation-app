#!/usr/bin/env bash
# exit on error
set -o errexit

# Check Python version
echo "Checking Python version..."
python --version

# Install dependencies using pip
echo "Installing dependencies with pip..."
pip install --upgrade pip

# Install psycopg3 for Python 3.13 compatibility
echo "Installing psycopg3 for Python 3.13 compatibility..."
pip install --no-cache-dir psycopg[binary]

# Install all other dependencies from requirements.txt
echo "Installing other dependencies from requirements.txt..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!" 