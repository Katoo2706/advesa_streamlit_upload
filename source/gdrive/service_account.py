import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload, MediaIoBaseDownload


class GoogleDriveAPI:
    def __init__(self,
                 service_account_info: dict = None,
                 service_account_path: str = None) -> None:
        SCOPES = ['https://www.googleapis.com/auth/drive']

        if service_account_path:
            # if os.path.exists("service_account.json"):
            try:
                # if exist service account
                credentials = service_account.Credentials.from_service_account_file(
                    service_account_path,
                    scopes=SCOPES
                )
                self.service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
            except Exception:
                raise Exception("Service account path not valid")

        elif service_account_info:
            try:
                credentials = service_account.Credentials.from_service_account_info(service_account_info,
                                                                                    scopes=SCOPES)

                self.service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
            except Exception:
                raise Exception("Service account info not valid")
        else:
            raise Exception("Please enter service account path or service account info")

    def upload_file_from_path(self, file_path, folder_id, file_name: str = None) -> str:
        """
        Insert new file from path.
        Returns : Id's of the file uploaded
        """
        if not file_name:
            file_name = os.path.basename(file_path)

        media = MediaFileUpload(file_path,
                                resumable=True)

        file_metadata = self.service.files().create(
            body={
                'name': file_name,
                'parents': [folder_id]
            },
            media_body=media,
            fields='id'
        ).execute()

        print(f"Upload file {file_name} successfully")

        return file_metadata.get('id')

    def upload_file_from_memory(self, data, file_name, folder_id) -> dict:
        """
        Insert new file from memory io.
        Returns dict['id', 'url']: Id's of the file uploaded & share url
        """
        data_str = data.to_csv(index=False)
        data_encoded = data_str.encode('utf-8')
        try:
            media = MediaIoBaseUpload(io.BytesIO(data_encoded), mimetype='text/csv', resumable=True)

            file_metadata = self.service.files().create(
                media_body=media,
                body={
                    'name': file_name,
                    'parents': [folder_id]
                }
            ).execute()

            file_metadata['url'] = f"https://drive.google.com/file/d/{file_metadata.get('id')}/view?usp=sharing"

            return file_metadata
        except Exception as e:
            print("Can't upload file", e)

    def download_file(self, file_id):
        """Downloads a file
        Args:
            file_id: ID of the file to download
        Returns : IO object with location.
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            _file = io.BytesIO()
            downloader = MediaIoBaseDownload(_file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

            return _file.getvalue()

        except Exception as e:
            print(f"An error occurred: {e}")


# if __name__ == "__main__":
#     file = GoogleDriveAPI(service_account_path="service_account.json") \
#         .download_file(file_id="1cI9NI3i_Mv6GEKea5Q0TFvNKCrv1780Q")
#
#     print(file)
