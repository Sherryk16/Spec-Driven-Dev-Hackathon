import requests
import os

# Ensure the backend is running on this URL
BASE_URL = "http://127.0.0.1:8000"
INGEST_ENDPOINT = f"{BASE_URL}/ingest"

# Path to your book file (make sure this file exists in the backend directory)
# Check for either the original PDF or the new text file with meaningful content
if os.path.exists("sample_robotics_book.txt"):
    file_path = "sample_robotics_book.txt"
    file_type = "text/plain"
elif os.path.exists("sample_book.pdf"):
    file_path = "sample_book.pdf"
    file_type = "application/pdf"
else:
    print("Error: No sample book file found. Please ensure either 'sample_book.pdf' or 'sample_robotics_book.txt' exists in the backend directory.")
    exit(1)

title = "Robotics and AI Handbook"
author = "AI Assistant"

def ingest_book():
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}. Please create the file or update the file_path variable.")
        return

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, file_type)}
        data = {"title": title, "author": author}

        try:
            response = requests.post(INGEST_ENDPOINT, files=files, data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            print("Book ingestion successful!")
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error during book ingestion: {e}")
            if response is not None:
                print(f"Response content: {response.text}")

if __name__ == "__main__":
    ingest_book()

