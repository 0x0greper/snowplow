#!/usr/bin/env python3

import json
import requests
import argparse

def load_cookies(cookie_file):
    with open(cookie_file, 'r') as file:
        cookies = json.load(file)
    return cookies

def load_user_token(token_file):
    with open(token_file, 'r') as file:
        token = file.read().strip()
    return token

def make_api_request(url, api_endpoint, cookies, user_token):
    session = requests.Session()

    # Load cookies into the session
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    headers = {
        'X-UserToken': user_token
    }

    # Make an API request
    response = session.get(f"{url}{api_endpoint}", headers=headers)
    return response

def main():
    parser = argparse.ArgumentParser(description='ServiceNow API interaction script')
    parser.add_argument('url', type=str, help='ServiceNow instance URL')
    parser.add_argument('cookie_file', type=str, help='Path to the JSON file containing cookies')
    parser.add_argument('token_file', type=str, help='Path to the file containing the user token')
    parser.add_argument('api_endpoint', type=str, help='API endpoint to query')

    args = parser.parse_args()

    cookies = load_cookies(args.cookie_file)
    user_token = load_user_token(args.token_file)
    response = make_api_request(args.url, args.api_endpoint, cookies, user_token)

    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except json.JSONDecodeError:
        print("Failed to parse JSON response.")

if __name__ == "__main__":
    main()
