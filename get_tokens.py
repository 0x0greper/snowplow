import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import argparse

def perform_login(start_url, username, password):
    # Setup the WebDriver for Firefox
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get(start_url)

    # Step 1: Navigate to the initial URL and handle redirects
    time.sleep(5)  # wait for redirection to complete

    # Step 2: Check if we are on the login page
    if 'login.do' in driver.current_url:
        print("On login page")
        
        # Enter username
        username_field = driver.find_element(By.ID, 'user_name')
        username_field.send_keys(username)
        
        # Enter password
        password_field = driver.find_element(By.ID, 'user_password')
        password_field.send_keys(password)
        
        # Submit the form
        login_button = driver.find_element(By.ID, 'sysverb_login')
        login_button.click()

        time.sleep(10)  # wait for login and redirections

        # Save cookies to a file
        cookies = driver.get_cookies()
        with open("cookies.json", "w") as file:
            json.dump(cookies, file)
        
        print("Cookies saved to cookies.json")
        
        # Attempt to extract the X-Usertoken from the page
        try:
            user_token = driver.execute_script("return window.g_ck;")
            if user_token:
                with open("user_token.txt", "w") as file:
                    file.write(user_token)
                print("User token saved to user_token.txt")
            else:
                print("Failed to retrieve user token: token is None")
        except Exception as e:
            print(f"Failed to retrieve user token: {e}")

    else:
        print("Failed to reach the login page.")

    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ServiceNow login automation script')
    parser.add_argument('url', type=str, help='ServiceNow instance login URL')
    parser.add_argument('username', type=str, help='ServiceNow username')
    parser.add_argument('password', type=str, help='ServiceNow password')
    
    args = parser.parse_args()

    perform_login(args.url, args.username, args.password)

