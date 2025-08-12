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

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!" 