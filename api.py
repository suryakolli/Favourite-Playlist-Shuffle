import base64
import datetime
import os
from dotenv import load_dotenv
import requests


load_dotenv()


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret is None or client_id is None:
            raise Exception("You must set client_id and client_secret")
        client_credentials = f"{client_id}:{client_secret}"
        client_credentials_b64 = base64.b64encode(client_credentials.encode())
        return client_credentials_b64.decode()

    def get_token_headers(self):
        client_credentials_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_credentials_b64}"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = {
            "grant_type": "client_credentials"
        }
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token is None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup='new-releases', resource_type='playlists', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()


client = SpotifyAPI(os.getenv('client_id', ""), os.getenv('client_secret', ""))

client.perform_auth()
