"""
Recreate database with proper schema including new alert columns
"""

import os
from database import Base, engine
from models import User, Report, Prediction, Alert
from sqlalchemy.orm import Session

def recreate_database():
    """Drop and recreate all tables with current schema"""
    
    print("🔄 Recreating database with updated schema...")
    
    # Drop all tables
    print("  ⚠️  Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("  ✅ Tables dropped")
    
    # Create all tables with current schema
    print("  ➕ Creating tables with new schema...")
    Base.metadata.create_all(bind=engine)
    print("  ✅ Tables created")
    
    print("\n✅ Database recreated successfully!")
    print("\n📝 Note: All existing data has been cleared.")
    print("   Run 'python create_demo_users.py' to create test users.")

if __name__ == "__main__":
    recreate_database()
