#!/usr/bin/env python
"""
Test script to verify deployment readiness
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
 """Check if a file exists and print status"""
 if os.path.exists(filepath):
 print(f" {description}: {filepath}")
 return True
 else:
 print(f" {description}: {filepath} (MISSING)")
 return False

def check_directory_exists(dirpath, description):
 """Check if a directory exists and print status"""
 if os.path.isdir(dirpath):
 print(f" {description}: {dirpath}")
 return True
 else:
 print(f" {description}: {dirpath} (MISSING)")
 return False

def main():
 print(" Vercel Deployment Readiness Check")
 print("=" * 0)

 all_good = True

 # Check essential files
 print("\n Essential Files:")
 all_good &= check_file_exists("api/main.py", "FastAPI Entry Point")
 all_good &= check_file_exists("vercel.json", "Vercel Configuration")
 all_good &= check_file_exists("requirements.txt", "Python Dependencies")
 all_good &= check_file_exists("package.json", "Root Package.json")
 all_good &= check_file_exists("frontend/package.json", "Frontend Package.json")

 # Check directories
 print("\n Essential Directories:")
 all_good &= check_directory_exists("backend", "Backend Directory")
 all_good &= check_directory_exists("frontend/src", "Frontend Source")
 all_good &= check_directory_exists("api", "API Directory")

 # Check backend files
 print("\n Backend Files:")
 all_good &= check_file_exists("backend/main.py", "Backend Main")
 all_good &= check_file_exists("backend/models.py", "Database Models")
 all_good &= check_file_exists("backend/schemas.py", "API Schemas")
 all_good &= check_file_exists("backend/auth.py", "Authentication")
 all_good &= check_file_exists("backend/database.py", "Database Config")

 # Check ML models (optional)
 print("\n ML Models (Optional):")
 check_file_exists("backend/models/best_model.pkl", "Trained Model")
 check_file_exists("backend/models/scaler.pkl", "Feature Scaler")
 check_file_exists("backend/models/label_encoder.pkl", "Label Encoder")

 # Test imports
 print("\n Import Tests:")
 try:
 sys.path.insert(0, "backend")
 import main
 print(" Backend main.py imports successfully")
 except Exception as e:
 print(f" Backend import failed: {e}")
 all_good = False

 # Check frontend build
 print("\n Frontend Build Test:")
 if os.path.exists("frontend/node_modules"):
 print(" Frontend dependencies installed")
 else:
 print(" Frontend dependencies not installed (run: cd frontend && npm install)")

 # Final status
 print("\n" + "=" * 0)
 if all_good:
 print(" DEPLOYMENT READY!")
 print(" All essential files are present")
 print(" Backend imports work correctly")
 print("\n Next steps:")
 print(". Commit and push to GitHub")
 print(". Deploy to Vercel using the dashboard or CLI")
 print(". Add environment variables in Vercel dashboard")
 else:
 print(" DEPLOYMENT NOT READY")
 print(" Please fix the missing files/issues above")
 print("\n Common fixes:")
 print("- Run: python train_model.py (to generate ML models)")
 print("- Run: cd frontend && npm install (to install frontend deps)")
 print("- Check file paths and ensure all files exist")

 return all_good

if __name__ == "__main__":
 success = main()
 sys.exit(0 if success else )