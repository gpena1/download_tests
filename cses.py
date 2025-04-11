import requests,os
from bs4 import BeautifulSoup
import sys

if len(sys.argv) < 2:
    print("Usage: python cses.py [problem_id]")
    sys.exit(1)

problem_id = sys.argv[1]
print(f"Attempting to download tests for problem {problem_id}")

# Create a session to maintain cookies
session = requests.Session()

# First, get the login page to extract the CSRF token
login_page_url = "https://cses.fi/login"
login_response = session.get(login_page_url)
print(f"Login page status code: {login_response.status_code}")

# Parse the login page
login_soup = BeautifulSoup(login_response.text, 'html.parser')
login_csrf_input = login_soup.find('input', {'name': 'csrf_token'})

if not login_csrf_input:
    print("Could not find CSRF token on login page.")
    sys.exit(1)

login_csrf_token = login_csrf_input['value']
print(f"Found login CSRF token: {login_csrf_token[:5]}...")

# Perform login
username = os.environ['CSES_USER'] 
password = os.environ['CSES_PASSWORD']

login_data = {
    'csrf_token': login_csrf_token,
    'nick': username,
    'pass': password
}

login_result = session.post(login_page_url, data=login_data)
print(f"Login result status code: {login_result.status_code}")

# Now access the tests page
tests_url = f"https://cses.fi/problemset/tests/{problem_id}/"
tests_response = session.get(tests_url)
print(f"Tests page status code: {tests_response.status_code}")

# Parse the tests page - looking specifically for the form with 'csrf_token' input
tests_soup = BeautifulSoup(tests_response.text, 'html.parser')
download_form = tests_soup.find('form', {'method': 'post'})

if not download_form:
    print("Could not find download form on tests page.")
    sys.exit(1)

# Extract the CSRF token from the download form
tests_csrf_input = download_form.find('input', {'name': 'csrf_token'})
if not tests_csrf_input:
    print("Could not find CSRF token on tests page.")
    sys.exit(1)

tests_csrf_token = tests_csrf_input['value']
print(f"Found tests page CSRF token: {tests_csrf_token[:5]}...")

# Make the download request
download_data = {
    'csrf_token': tests_csrf_token,
    'download': 'true'
}

# Since the form action is empty, use the current URL
download_response = session.post(tests_url, data=download_data)
print(f"Download response status code: {download_response.status_code}")
print(f"Content-Type: {download_response.headers.get('Content-Type', 'None')}")

# Check if the response is a zip file
content_type = download_response.headers.get('Content-Type', '')
if 'application/zip' in content_type or 'application/octet-stream' in content_type:
    # Save the response content as a zip file
    zip_filename = f"tests.zip"
    with open(zip_filename, 'wb') as f:
        f.write(download_response.content)
    print(f"Successfully downloaded tests to {zip_filename}")

    file_size = os.path.getsize(zip_filename)
    print(f"File size: {file_size} bytes")

    if file_size < 100:  # Suspiciously small for a zip file
        print("Warning: The downloaded file is very small. It might not be a valid zip file.")
        with open(zip_filename, 'rb') as f:
            content = f.read()
        print(f"First 100 bytes: {content[:100]}")
else:
    # Save the response content to debug
    with open("download_response.html", "wb") as f:
        f.write(download_response.content)
    print("Response doesn't appear to be a zip file. Saved to download_response.html for inspection.")
