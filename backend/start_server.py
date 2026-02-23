#!/usr/bin/env python
"""
Startup script for the Water-Borne Disease Prediction API
"""
import uvicorn

if __name__ == "__main__":
 print("Starting Water-Borne Disease Prediction API...")
 print("API Documentation will be available at: http://localhost:000/docs")
 print("Health check endpoint: http://localhost:000/health")
 print("Press CTRL+C to stop the server")

 uvicorn.run(
 "main:app",
 host="0.0.0.0",
 port=000,
 reload=True, # Enable auto-reload for development
 log_level="info"
 )