import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import argparse

def save_cookies(driver, cookies_file):
    cookies = driver.get_cookies()
    with open(cookies_file, 'w') as file:
        json.dump(cookies, file)
    print(f"Cookies saved to {cookies_file}")

def save_user_token(driver, token_file):
    try:
        user_token = driver.execute_script("return window.g_ck;")
        with open(token_file, 'w') as file:
            file.write(user_token)
        print(f"User token saved to {token_file}")
    except Exception as e:
        print(f"Failed to retrieve user token: {e}")

def perform_login(url, username, password):
    # Setup the WebDriver for Firefox
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get(url)

    # Enter username
    time.sleep(3)
    username_field = driver.find_element(By.ID, 'user_name')
    username_field.send_keys(username)

    # Enter password
    password_field = driver.find_element(By.ID, 'user_password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Wait for redirects and final page load
    time.sleep(10)

    # Save cookies and user token
    save_cookies(driver, "cookies.json")
    save_user_token(driver, "user_token.txt")

    driver.quit()

def main():
    parser = argparse.ArgumentParser(description='ServiceNow Login Script')
    parser.add_argument('url', type=str, help='ServiceNow login URL')
    parser.add_argument('username', type=str, help='ServiceNow username')
    parser.add_argument('password', type=str, help='ServiceNow password')

    args = parser.parse_args()

    perform_login(args.url, args.username, args.password)

if __name__ == "__main__":
    main()
