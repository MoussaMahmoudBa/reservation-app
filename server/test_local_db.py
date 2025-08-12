#!/usr/bin/env python3
"""
Simple test to verify psycopg2-binary installation
"""
try:
    import psycopg2
    print("✅ psycopg2 imported successfully")
    
    # Test basic functionality
    print(f"psycopg2 version: {psycopg2.__version__}")
    
except ImportError as e:
    print(f"❌ Failed to import psycopg2: {e}")
    exit(1)

try:
    import psycopg2.extensions
    print("✅ psycopg2.extensions imported successfully")
except ImportError as e:
    print(f"❌ Failed to import psycopg2.extensions: {e}")
    exit(1)

print("✅ All psycopg2 tests passed!") 