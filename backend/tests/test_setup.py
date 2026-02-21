#!/usr/bin/env python3
"""
Test script to verify the FastAPI backend setup
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test database
        from database import engine, get_db, Base
        print("✓ Database module imported successfully")
        
        # Test models
        import models
        print("✓ Models module imported successfully")
        
        # Test schemas
        import schemas
        print("✓ Schemas module imported successfully")
        
        # Test auth
        import auth
        print("✓ Auth module imported successfully")
        
        # Test FastAPI
        from fastapi import FastAPI
        print("✓ FastAPI imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_database_creation():
    """Test database table creation"""
    try:
        print("\nTesting database setup...")
        from database import engine
        import models
        
        # Create tables
        models.Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Database setup error: {e}")
        return False

def test_model_loading():
    """Test ML model loading"""
    try:
        print("\nTesting ML model loading...")
        import joblib
        
        model_files = [
            './models/best_model.pkl',
            './models/scaler.pkl',
            './models/label_encoder.pkl',
            './models/feature_names.pkl',
            './models/preprocessing_info.pkl'
        ]
        
        for model_file in model_files:
            if os.path.exists(model_file):
                joblib.load(model_file)
                print(f"✓ {model_file} loaded successfully")
            else:
                print(f"⚠ {model_file} not found")
        
        return True
        
    except Exception as e:
        print(f"✗ Model loading error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("FASTAPI BACKEND SETUP TEST")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_database_creation,
        test_model_loading
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if all(results):
        print("✓ All tests passed! Backend setup is ready.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())