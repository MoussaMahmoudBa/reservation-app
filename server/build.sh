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

# Try to run database migrations (continue even if it fails)
echo "Running database migrations..."
if python manage.py migrate; then
    echo "✅ Database migrations completed successfully"
else
    echo "⚠️ Database migrations failed, but continuing with build..."
    echo "⚠️ Please check your database configuration on Render.com"
fi

echo "Build completed successfully!" 