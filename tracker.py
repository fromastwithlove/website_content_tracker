# ! /usr/bin/env python3

# 2024-08-08
# Author: adil.yergaliyev@gmail.com

import hashlib
import sys
from bs4 import BeautifulSoup
import requests
import os

URL = "https://www.stadt-koeln.de/service/produkte/00547/index.html"
DEBUG_URL = "http://localhost:8000"

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

WEBSITE_HASH = os.path.join(SCRIPT_DIR, 'tmp', 'website_hash.md5')
WEBSITE_CONTENT = os.path.join(SCRIPT_DIR, 'tmp', 'website_content.txt')

# Ensure the 'tmp' directory exists
os.makedirs('tmp', exist_ok=True)

def get_website_content(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract text content
    text_content = soup.get_text()
    return text_content

def hash_content(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def prepare_email_content(old_content, new_content):
    old_lines = set(old_content.splitlines())
    new_lines = set(new_content.splitlines())
    added_lines = new_lines - old_lines

    if added_lines:
        email_body = "New content detected on the monitored website:\n\n"
        email_body += "\n".join(line.strip() for line in added_lines if line.strip())
        return email_body
    else:
        return "No new content added."

if __name__ == "__main__":
    try:
        print(f"Monitoring {URL} for changes...")
        current_content = get_website_content(URL) # Use DEBUG_URL for debugging
        current_hash = hash_content(current_content)

        try:
            with open(WEBSITE_HASH, 'r') as file:
                old_hash = file.read().strip()
        except FileNotFoundError:
            old_hash = None
        
        if old_hash is None:
            # First run, save the content and hash without triggering a change
            print("First run. Storing the initial content.")
            with open(WEBSITE_HASH, 'w') as file:
                file.write(current_hash)
            with open(WEBSITE_CONTENT, 'w') as file:
                file.write(current_content)
            sys.exit(0)
        
        if current_hash != old_hash:
            print("Website content has changed :)")

            with open(WEBSITE_CONTENT, 'r') as file:
                old_content = file.read().strip()
            
            # Prepare email-friendly content
            email_body = prepare_email_content(old_content, current_content)
            print(email_body)

            # Save the new hash and content
            with open(WEBSITE_HASH, 'w') as file:
                file.write(current_hash)
            
            with open(WEBSITE_CONTENT, 'w') as file:
                file.write(current_content)
            
            sys.exit(1)
        else:
            print("No changes detected.")
            sys.exit(0)
    except Exception as e:
        print(f"Error checking website: {e}")
        sys.exit(1)
