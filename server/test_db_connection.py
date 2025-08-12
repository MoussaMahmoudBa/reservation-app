#!/usr/bin/env python3
"""
Test script to verify database connection with psycopg3
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_project.settings')
django.setup()

# Test database connection
from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Database connection successful!")
        print(f"PostgreSQL version: {version[0]}")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)

print("✅ All tests passed!") 