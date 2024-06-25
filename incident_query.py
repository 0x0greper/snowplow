#!/usr/bin/env python3

import requests
import http
from pysnc import ServiceNowClient

# requests Authentication class for ServiceNow Rest API token authentication
# https://docs.python-requests.org/en/latest/user/authentication/#new-forms-of-authentication
# https://developer.servicenow.com/blog.do?p=/post/debugging-inbound-rest-calls-and-the-business-rulesacls-that-impact-those-calls/#using-external-api-testing-tools
class TokenAuth(requests.auth.AuthBase):
    def __init__(self, user_token, jsession_id):
        self.user_token  = user_token
        self.jsession_id = jsession_id

    def __call__(self, r):
        # set token header for request
        r.headers['X-Usertoken'] = self.user_token

        # add session cookie to request
        req       = requests.get(r.url)
        cookiejar = http.cookiejar.CookieJar()
        cookie    = req.cookies.set('JSESSIONID', self.jsession_id)
        cookiejar.set_cookie(cookie)
        r.prepare_cookies(cookiejar)

        return r

# Configuration
instance    = 'https://yoursite.servicenowservices.com'  # Replace with your ServiceNow instance
user_token  = 'some_usertoken_here'   # Replace with your `X-Usertoken` header
jsession_id = 'some_jsessionid_here'  # Replace with your `JSESSIONID` cookie

# Create the ServiceNow client using basic authentication
client = ServiceNowClient(instance, TokenAuth(user_token, jsession_id))

def fetch_incidents_with_keyword(keyword):
    try:
        # Create a GlideRecord object for the 'incident' table
        gr = client.GlideRecord('incident')
        gr.add_query('active', 'true')  # Example query: active incidents
        gr.add_query('short_description', 'CONTAINS', keyword)  # Filter by keyword in the short description
        gr.query()

        # Iterate through the results and print the sys_id and other details of each record
        for record in gr:
            print(f"Incident ID: {record.sys_id}")

            # Fetch additional details for each incident
            record_details = client.GlideRecord('incident')
            if record_details.get(record.sys_id):
                print(f"Details for Incident ID {record.sys_id}:")
                print(f"Short Description: {record_details.short_description}")
                print(f"State: {record_details.state}")
                print(f"Description: {record_details.description}")
                print(f"Comments: {record_details.comments}")
                # Add more fields as needed
            else:
                print(f"Record with sys_id {record.sys_id} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Keyword to search for in incident records
keyword = input("Enter the keyword to search for in incident records: ")
fetch_incidents_with_keyword(keyword)
