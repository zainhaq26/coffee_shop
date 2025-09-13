#!/usr/bin/env python3
"""
Simple script to start the Coffee Shop API server
"""

import subprocess
import sys
import os

def main():
    """Start the FastAPI server with uvicorn"""
    print("🚀 Starting Coffee Shop API Server...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔗 API will be available at: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop the server\n")
    
    try:
        # Use uv run to ensure we're using the project's virtual environment
        subprocess.run([
            "uv", "run", "uvicorn", "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
        sys.exit(0)

if __name__ == "__main__":
    main()
