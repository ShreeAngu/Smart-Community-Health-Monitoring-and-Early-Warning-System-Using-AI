#!/usr/bin/env python
"""
Quick script to verify demo users exist and have correct roles
"""
import sys
sys.path.append('.')

from database import get_db
from models import User

def verify_users():
 """Verify demo users"""
 try:
 db = next(get_db())

 print("=" * 0)
 print("VERIFYING DEMO USERS")
 print("=" * 0)

 users = db.query(User).all()

 if not users:
 print("\n NO USERS FOUND!")
 print("\nRun: python create_demo_users.py")
 return False

 print(f"\n Found {len(users)} user(s)\n")

 expected_users = {
 'admin@example.com': 'admin',
 'community@example.com': 'community',
 'test@example.com': 'community'
 }

 all_correct = True

 for user in users:
 expected_role = expected_users.get(user.email)
 actual_role = user.role.value

 if expected_role and actual_role == expected_role:
 print(f" {user.email}")
 print(f" Role: {actual_role}")
 print(f" ID: {user.id}")
 else:
 print(f" {user.email}")
 print(f" Expected role: {expected_role}")
 print(f" Actual role: {actual_role}")
 all_correct = False
 print()

 if all_correct:
 print("=" * 0)
 print(" ALL USERS VERIFIED!")
 print("=" * 0)
 print("\nYou can now login with:")
 print(" Admin: admin@example.com / admin")
 print(" Community: community@example.com / community")
 return True
 else:
 print("=" * 0)
 print(" SOME USERS HAVE INCORRECT ROLES")
 print("=" * 0)
 print("\nRun: python create_demo_users.py")
 return False

 except Exception as e:
 print(f"\n ERROR: {e}")
 print("\nThe database might not exist.")
 print("Run: python create_demo_users.py")
 return False

if __name__ == "__main__":
 success = verify_users()
 sys.exit(0 if success else )
