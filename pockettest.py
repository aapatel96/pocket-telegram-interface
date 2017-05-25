from pocket import Pocket

consumer_key="67229-58499186bd836a77ac726d5f"
redirect_uri="https://telegram.me/getpocket_bot"

request_token = Pocket.get_request_token(consumer_key=consumer_key, redirect_uri=redirect_uri)

# URL to redirect user to, to authorize your app
auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)

user_credentials = Pocket.get_credentials(consumer_key=consumer_key, code=request_token)

access_token = user_credentials['access_token']
