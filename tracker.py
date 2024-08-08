# ! /usr/bin/env python3

# 2024-08-08
# Author: adil.yergaliyev@gmail.com

import difflib
import hashlib
import sys
from bs4 import BeautifulSoup
import requests

URL = "https://www.stadt-koeln.de/service/produkte/00547/index.html"
DEBUG_URL = "http://localhost:8000"

WEBSITE_HASH = "tmp/website_hash.md5"
WEBSITE_CONTENT = "tmp/website_content.txt"

def get_website_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract text content
    text_content = soup.get_text()
    return text_content

def hash_content(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def print_diff(old_content, new_content):
    diff = difflib.unified_diff(
        old_content.splitlines(), 
        new_content.splitlines(), 
        lineterm=''
    )
    
    removed_lines = []
    added_lines = []

    for line in diff:
        if line.startswith('-'):
            line_content = line[1:].strip()
            if line_content:  # Add non-empty lines
                removed_lines.append(f"\033[91m{line_content}\033[0m")  # Red for removed lines
        elif line.startswith('+'):
            line_content = line[1:].strip()
            if line_content:  # Add non-empty lines
                added_lines.append(f"\033[92m{line_content}\033[0m")  # Green for added lines

    if removed_lines or added_lines:
        print("Changes detected:\n")
        if removed_lines:
            print("Removed Content:")
            print("\n".join(removed_lines))
        if added_lines:
            print("\nAdded Content:")
            print("\n".join(added_lines))
    else:
        print("No significant changes detected.")

if __name__ == "__main__":
    try:
        print(f"Monitoring {URL} for changes...")
        current_content = get_website_content(URL) # Use DEBUG_URL for debugging
        current_hash = hash_content(current_content)

        try:
            with open(WEBSITE_HASH, 'r') as file:
                old_hash = file.read().strip()
        except FileNotFoundError:
            old_hash = ''
        
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
            
            # Print only the differences with color coding
            print_diff(old_content, current_content)
                            
            with open(WEBSITE_HASH, 'w') as file:
                file.write(current_hash)
            
            with open(WEBSITE_CONTENT, 'w') as file:
                file.write(current_content)
            
            sys.exit(1)
        else:
            sys.exit(0)
    except Exception as e:
        print(f"Error checking website: {e}")
        sys.exit(1)