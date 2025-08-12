#!/usr/bin/env bash
# exit on error
set -o errexit

# Force Python 3.11 if available
echo "Checking Python version..."
python --version

# Install dependencies using pip
echo "Installing dependencies with pip..."
pip install --upgrade pip

# Try different psycopg2-binary versions for compatibility
echo "Installing psycopg2-binary with compatibility check..."
if pip install --no-cache-dir psycopg2-binary==2.9.9; then
    echo "✅ psycopg2-binary==2.9.9 installed successfully"
elif pip install --no-cache-dir psycopg2-binary==2.9.7; then
    echo "✅ psycopg2-binary==2.9.7 installed successfully"
elif pip install --no-cache-dir psycopg2-binary; then
    echo "✅ Latest psycopg2-binary installed successfully"
else
    echo "❌ Failed to install psycopg2-binary, trying psycopg3..."
    pip install --no-cache-dir psycopg[binary]
fi

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