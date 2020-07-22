import configparser
import os
import sys

from requests_oauthlib import OAuth2Session

try:
    platform = str(sys.argv[1])
    print(f"Resource is sourced from {platform} platform.")
except IndexError:
    sys.exit(0)

config = configparser.ConfigParser()
config.read("credentials.ini")

res_client_id = config[platform]['client_id']
res_client_secret = config[platform]['client_secret']
res_scope = config[platform]['scope']
res_redirect_url = config[platform]['redirect_url']
res_auth_url = config[platform]['auth_url']
res_token_url = config[platform]['token_url']
res_api_call = config[platform]['api_call']

token = {}

# Start the example code
# Set environment variables
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

target_platform = OAuth2Session(res_client_id, redirect_uri=res_redirect_url, scope=res_scope, token=token)

# Redirect user to LinkedIn for authorization
authorization_url, state = target_platform.authorization_url(res_auth_url)
print(f"Please go here and authorize: {authorization_url}")

# Get the authorization verifier code from the callback url
redirect_response = input('Paste the full redirect URL here:')

# Fetch the access token
target_platform.fetch_token(res_token_url, client_secret=res_client_secret,
                            include_client_id=True,
                            authorization_response=redirect_response)

print("Fetched token")

# Fetch a protected resource, i.e. user profile
r = target_platform.get('https://api.linkedin.com/v2/me')
print(r.content)
