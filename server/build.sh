#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies using pip (preferred for this project)
echo "Installing dependencies with pip..."
pip install --upgrade pip

# Install other dependencies first
echo "Installing other dependencies..."
pip install -r requirements.txt

# Try to install Pillow with different approaches
echo "Installing Pillow with specific options..."
if ! pip install --no-cache-dir --only-binary=all Pillow==10.4.0; then
    echo "Trying alternative Pillow installation..."
    if ! pip install --no-cache-dir Pillow==10.4.0; then
        echo "Trying latest Pillow version..."
        pip install --no-cache-dir Pillow
    fi
fi

# Try to install psycopg with different approaches
echo "Installing psycopg with specific options..."
if ! pip install --no-cache-dir --only-binary=all psycopg[binary]==3.1.18; then
    echo "Trying psycopg2-binary..."
    if ! pip install --no-cache-dir psycopg2-binary==2.9.9; then
        echo "Trying latest psycopg..."
        pip install --no-cache-dir psycopg[binary]
    fi
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!" 