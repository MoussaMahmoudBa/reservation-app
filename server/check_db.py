#!/usr/bin/env python3
"""
Script to check database connection and configuration
"""
import os
from decouple import config

def check_database_config():
    print("🔍 Checking database configuration...")
    
    # Check if DATABASE_URL is set
    database_url = config('DATABASE_URL', default=None)
    if database_url:
        print(f"✅ DATABASE_URL is set")
        # Mask password for security
        masked_url = database_url.replace('://', '://***:***@')
        print(f"📝 DATABASE_URL: {masked_url}")
    else:
        print("❌ DATABASE_URL is not set")
        return False
    
    # Try to connect to database
    try:
        import psycopg
        from psycopg import connect
        
        print("🔌 Attempting to connect to database...")
        with connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
                print(f"✅ Database connection successful!")
                print(f"📊 PostgreSQL version: {version[0]}")
                return True
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    check_database_config() 