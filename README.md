# snowplow
This repository contains scripts to interact with ServiceNow deployments.
=======

# snowplow
This repository contains scripts to interact with ServiceNow deployments.
=======
Snowplow
========

This repository contains two scripts to interact with ServiceNow deployments.

Scripts
-------

- `get_tokens.py`: This script automates the process of obtaining session cookies and tokens from ServiceNow.
- `query_api.py`: This script makes authenticated API requests to ServiceNow using the obtained tokens and cookies.

Installation
------------

1. Clone the repository:

git clone https://github.com/0x0greper/snowplow.git

2. Navigate to the project directory:
cd snowplow

3. Install the required packages:
pip install -r requirements.txt

Usage
-----

### Get Tokens

python get_tokens.py <login_url> <username> <password>

This will save the session cookies to `cookies.json` and the user token to `user_token.txt`.

### Query API

python3 query_api.py <instance_url> <cookies_file> <api_endpoint> <user_token_file>

Example:
python3 query_api.py https://your_instance.service-now.com cookies.json /api/now/table/sys_user user_token.txt
