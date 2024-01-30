# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class CreateService:
    def __init__(self, api_name, api_version, scope: list):
        self.API_SERVICE_NAME = api_name
        self.API_VERSION = api_version
        self.SCOPES = scope

    def __create__(self, flow):
        cred = None

        pickle_file = f'token_{self.API_SERVICE_NAME}_{self.API_VERSION}.pickle'
        # print(pickle_file)

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(self.API_SERVICE_NAME, self.API_VERSION, credentials=cred)
            print(self.API_SERVICE_NAME, 'service created successfully')
            return service
        except Exception as e:
            print('Unable to connect.')
            print(e)
            return None

    def create_from_file(self, client_secret_file):
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, self.SCOPES)

        return self.__create__(flow)

    def create_from_config(self, client_id, client_secret):
        credentials_config = {
            "web": {
                "client_id": client_id,
                "project_id": "earnest-runner-408607",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": client_secret
            }
        }

        flow = InstalledAppFlow.from_client_config(credentials_config, self.SCOPES)

        return self.__create__(flow)


if __name__ == "__main__":
    CLIENT_ID = "899034722624-0krj7jb61u7kmt16331cl611a656i26n.apps.googleusercontent.com"
    CLIENT_SECRET = "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"

    service = CreateService(
        api_name="drive",
        api_version="v3",
        scope=['https://www.googleapis.com/auth/drive']
    ).create_from_config(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
