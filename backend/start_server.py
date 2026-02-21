#!/usr/bin/env python3
"""
Startup script for the Water-Borne Disease Prediction API
"""
import uvicorn

if __name__ == "__main__":
    print("Starting Water-Borne Disease Prediction API...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("Health check endpoint: http://localhost:8000/health")
    print("Press CTRL+C to stop the server")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )