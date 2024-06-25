from pysnc import ServiceNowClient

# Configuration
instance = 'https://yoursite.servicenowservices.com'  # Replace with your ServiceNow instance
username = 'your_user_name'  # Replace with your username
password = 'your_password'  # Replace with your password

# Create the ServiceNow client using basic authentication
client = ServiceNowClient(instance, (username, password))

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
