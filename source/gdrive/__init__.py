import streamlit as st
from .service_account import GoogleDriveAPI

service_account_info = {
    "type": "service_account",
    "project_id": st.secrets["PROJECT_ID"],
    "private_key_id": st.secrets["PRIVATE_KEY_ID"],
    "private_key": st.secrets["PRIVATE_KEY"],
    "client_email": st.secrets["CLIENT_EMAIL"],
    "client_id": st.secrets["CLIENT_ID"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets["CLIENT_URL"],
    "universe_domain": "googleapis.com"
}


def upload_file_from_path(file_path, folder_id, file_name: str = None):
    return GoogleDriveAPI(service_account_info=service_account_info).upload_file_from_path(
        file_path, folder_id, file_name)


def upload_file_from_memory(data, file_name, folder_id):
    return GoogleDriveAPI(service_account_info=service_account_info).upload_file_from_memory(data, file_name, folder_id)
