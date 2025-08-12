#!/usr/bin/env python3
"""
Test script to verify psycopg3 installation and functionality
"""
try:
    import psycopg
    print("✅ psycopg3 imported successfully")
    print(f"psycopg3 version: {psycopg.__version__}")
    
    # Test basic functionality
    from psycopg import connect
    print("✅ psycopg3.connect imported successfully")
    
except ImportError as e:
    print(f"❌ Failed to import psycopg3: {e}")
    exit(1)

try:
    import psycopg.extensions
    print("✅ psycopg3.extensions imported successfully")
except ImportError as e:
    print(f"❌ Failed to import psycopg3.extensions: {e}")
    exit(1)

print("✅ All psycopg3 tests passed!") 