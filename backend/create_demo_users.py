#!/usr/bin/env python3
"""
Create demo users for testing both Community and Admin dashboards
"""
import sys
sys.path.append('.')

from database import get_db
import models
from auth import get_password_hash

def create_demo_users():
    """Create demo users for both roles"""
    try:
        db = next(get_db())
        
        print("=" * 60)
        print("CREATING DEMO USERS")
        print("=" * 60)
        
        # Check and delete existing users
        existing_users = db.query(models.User).all()
        if existing_users:
            print(f"\nFound {len(existing_users)} existing user(s). Deleting...")
            for user in existing_users:
                db.delete(user)
            db.commit()
            print("✓ Existing users deleted")
        
        # Create Admin User
        print("\nCreating admin user...")
        admin_user = models.User(
            email="admin@example.com", 
            password_hash=get_password_hash("admin123"),
            role=models.UserRole.admin
        )
        db.add(admin_user)
        
        # Create Community User
        print("Creating community user...")
        community_user = models.User(
            email="community@example.com",
            password_hash=get_password_hash("community123"),
            role=models.UserRole.community
        )
        db.add(community_user)
        
        # Keep the original test user as community
        print("Creating test user...")
        test_user = models.User(
            email="test@example.com",
            password_hash=get_password_hash("testpassword123"),
            role=models.UserRole.community
        )
        db.add(test_user)
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("✓ DEMO USERS CREATED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\n📋 DEMO USER CREDENTIALS")
        print("-" * 60)
        
        print("\n👑 ADMIN USER:")
        print("   Email:    admin@example.com")
        print("   Password: admin123")
        print("   Role:     Admin")
        print("   Access:   Full system access, analytics, alerts")
        
        print("\n🏠 COMMUNITY USER:")
        print("   Email:    community@example.com")
        print("   Password: community123")
        print("   Role:     Community")
        print("   Access:   Health reporting, risk checking")
        
        print("\n🧪 TEST USER:")
        print("   Email:    test@example.com")
        print("   Password: testpassword123")
        print("   Role:     Community")
        print("   Access:   Health reporting, risk checking")
        
        print("\n" + "=" * 60)
        print("USAGE INSTRUCTIONS")
        print("=" * 60)
        print("\n1. Start the backend server:")
        print("   python main.py")
        print("\n2. Start the frontend server:")
        print("   cd ../frontend && npm run dev")
        print("\n3. Open browser:")
        print("   http://localhost:5173")
        print("\n4. Login with any credentials above")
        print("\n" + "=" * 60)
        
        db.close()
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: Failed to create demo users")
        print(f"   Details: {e}")
        return False

def verify_users():
    """Verify created users"""
    try:
        from auth import authenticate_user
        db = next(get_db())
        
        print("\n" + "=" * 60)
        print("VERIFYING USERS")
        print("=" * 60)
        
        users_to_test = [
            ("admin@example.com", "admin123", "admin"),
            ("community@example.com", "community123", "community"),
            ("test@example.com", "testpassword123", "community")
        ]
        
        all_verified = True
        for email, password, expected_role in users_to_test:
            user = authenticate_user(email, password, db)
            if user and user.role.value == expected_role:
                print(f"✓ {email} - Role: {user.role.value}")
            else:
                print(f"✗ {email} - Verification failed")
                all_verified = False
        
        db.close()
        
        if all_verified:
            print("\n✓ All users verified successfully!")
        else:
            print("\n✗ Some users failed verification")
        
        return all_verified
        
    except Exception as e:
        print(f"\n✗ Verification error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DEMO USER SETUP SCRIPT")
    print("=" * 60)
    
    # Create users
    if create_demo_users():
        # Verify users
        if verify_users():
            print("\n" + "=" * 60)
            print("✅ SETUP COMPLETE - READY TO USE!")
            print("=" * 60)
            sys.exit(0)
        else:
            print("\n❌ VERIFICATION FAILED")
            sys.exit(1)
    else:
        print("\n❌ SETUP FAILED")
        sys.exit(1)