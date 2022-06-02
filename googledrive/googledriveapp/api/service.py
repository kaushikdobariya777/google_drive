from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

import io
import shutil

from rest_framework.response import Response
from rest_framework import status


class DriveService:

    def get_folder_service(self, credentials=None):
        if not credentials:
            return Response(
                {
                    "msg": "Credentials are missing!",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            service = build('drive', 'v3', credentials=credentials)
            results = service.files().list(
                q="mimeType='application/vnd.google-apps.folder'",
                spaces='drive',
                pageSize=100,
                fields="nextPageToken, files(id, name)").execute()

            items = results.get('files', [])

            if not items:
                return Response(
                    {
                        "count": 0,
                        "folders": []
                    },
                    status=status.HTTP_200_OK
                )
            return items

        except HttpError as error:
            return Response(
                {
                    "msg": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_file_service(self, credentials=None, file_id=None):
        if not credentials:
            return Response(
                {
                    "msg": "Credentials are missing!",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            service = build('drive', 'v3', credentials=credentials)
            results = service.files().list(
                q="parents in '" + file_id + "'",
                spaces='drive',
                pageSize=100,
                fields="nextPageToken, files(id, name)").execute()

            items = results.get('files', [])

            if not items:
                return Response(
                    {
                        "count": 0,
                        "files": []
                    },
                    status=status.HTTP_200_OK
                )
            return items

        except HttpError as error:
            return Response(
                {
                    "msg": error.reason,
                    "details": error.error_details
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def download_file(self, credentials=None, file_id=None):
        if not credentials:
            return Response(
                {
                    "msg": "Credentials are missing!",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            service = build('drive', 'v3', credentials=credentials)
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            # fh = io.FileIO('file.tar.gz', 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                file_status, done = downloader.next_chunk()
                print("Download %d%%." % int(file_status.progress() * 100))
            fh.seek(0)
            with open(file_id, 'wb') as f:
                shutil.copyfileobj(fh, f)
        except Exception as e:
            return Response(
                {
                    "error": e
                },
                status=status.HTTP_400_BAD_REQUEST
            )
