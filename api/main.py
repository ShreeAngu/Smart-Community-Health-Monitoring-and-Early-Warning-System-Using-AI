"""
FastAPI application entry point for Vercel deployment
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set working directory to backend for relative imports
original_cwd = os.getcwd()
os.chdir(backend_dir)

try:
 # Import the FastAPI app from backend
 from main import app
except ImportError as e:
 print(f"Import error: {e}")
 # Fallback import
 import main
 app = main.app
finally:
 # Restore original working directory
 os.chdir(original_cwd)

# Export the app for Vercel
__all__ = ["app"]