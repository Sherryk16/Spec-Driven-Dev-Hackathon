#!/usr/bin/env python3
"""
Startup script for the Integrated RAG Chatbot.
This script will start the backend server with fallback to mock services if needed.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    print("Starting Integrated RAG Chatbot with fallback services...")
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    print("Attempting to start the backend server...")
    print("The server will automatically fall back to mock services if real services fail.")
    
    # Start the uvicorn server
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "src.api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"  # Enable auto-reload for development
    ]
    
    try:
        # Run the server
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting the server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()