#!/usr/bin/env python3
"""
Simple test to debug registration issue
"""
import sys
sys.path.append('.')

from auth import get_password_hash, verify_password

def test_password_hashing():
    """Test password hashing directly"""
    try:
        password = "testpassword123"
        print(f"Testing password: {password}")
        
        # Test hashing
        hashed = get_password_hash(password)
        print(f"Hashed password: {hashed}")
        
        # Test verification
        is_valid = verify_password(password, hashed)
        print(f"Password verification: {is_valid}")
        
        return is_valid
        
    except Exception as e:
        print(f"Password hashing error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from database import get_db, engine
        from sqlalchemy.orm import Session
        
        # Test database connection
        db = next(get_db())
        print("Database connection: OK")
        db.close()
        return True
        
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

def test_user_creation():
    """Test user creation directly"""
    try:
        from database import get_db
        import models
        
        db = next(get_db())
        
        # Check if user exists
        existing_user = db.query(models.User).filter(models.User.email == "test@example.com").first()
        if existing_user:
            print("User already exists, deleting...")
            db.delete(existing_user)
            db.commit()
        
        # Create new user
        hashed_password = get_password_hash("testpassword123")
        new_user = models.User(
            email="test@example.com",
            password_hash=hashed_password,
            role=models.UserRole.community
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"User created: ID={new_user.id}, Email={new_user.email}")
        db.close()
        return True
        
    except Exception as e:
        print(f"User creation error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("DEBUGGING REGISTRATION ISSUE")
    print("=" * 50)
    
    print("\n1. Testing password hashing...")
    hash_ok = test_password_hashing()
    
    print("\n2. Testing database connection...")
    db_ok = test_database_connection()
    
    print("\n3. Testing user creation...")
    user_ok = test_user_creation()
    
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"Password hashing: {'✓' if hash_ok else '✗'}")
    print(f"Database connection: {'✓' if db_ok else '✗'}")
    print(f"User creation: {'✓' if user_ok else '✗'}")