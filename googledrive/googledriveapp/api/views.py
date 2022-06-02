import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponseRedirect

from googledriveapp.api.credentials import GoogleAuthCredentials
from googledriveapp.api.service import DriveService
from googledriveapp.models import GoogleAuthToken


class GoogleAuthCode(viewsets.ViewSet):

    def list(self, request, pk=None):
        cred_obj = GoogleAuthCredentials()
        data = cred_obj.get_client_config()
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=data.get('client_config'),
            scopes=data.get('scopes')
        )
        flow.redirect_uri = data.get('redirect_uri')
        authorization_url, state = flow.authorization_url(
            state='sample_passthrough_value',
            login_hint=data.get('login_hint'),
            include_granted_scopes='true',
        )
        return HttpResponseRedirect(redirect_to=authorization_url)


class GoogleRefreshToken(viewsets.ViewSet):

    def create(self, request):
        data = request.data
        code = data.get('code', None)
        if not code:
            return Response(
                {
                    "msg": "Authorization code is missing!!"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        cred_obj = GoogleAuthCredentials()
        data = cred_obj.get_client_config()
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=data.get('client_config'),
            scopes=data.get('scopes')
        )
        flow.redirect_uri = data.get('redirect_uri')
        flow.fetch_token(code=code)
        credentials = flow.credentials
        if GoogleAuthToken.objects.filter(name=cred_obj.project_id).exists():
            auth_obj = GoogleAuthToken.objects.get(name=cred_obj.project_id)
            auth_obj.token = credentials.token
            auth_obj.refresh_token = credentials.refresh_token
            auth_obj.save()
        else:
            auth_obj = GoogleAuthToken.objects.create(
                name=cred_obj.project_id,
                token=credentials.token,
                refresh_token=credentials.refresh_token
            )
            auth_obj.save()
        return Response(
            {
                "msg": "You have successfully generated token!!",
                "details": {
                    "token": credentials.token,
                    "refresh_token": credentials.refresh_token
                }
            },
            status=status.HTTP_200_OK
        )


class GoogleRegenerateRefreshToken(viewsets.ViewSet):

    def create(self, request):
        data = request.data
        refresh_token = data.get('refresh_token', None)
        if not refresh_token:
            return Response(
                {
                    "msg": "Refresh Token is missing!!"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        cred_obj = GoogleAuthCredentials()
        data = cred_obj.get_client_config()
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=data.get('client_config'),
            scopes=data.get('scopes')
        )
        flow.redirect_uri = data.get('redirect_uri')
        flow.fetch_token(refresh_token=refresh_token)
        credentials = flow.credentials
        try:
            auth_obj = GoogleAuthToken.objects.get(name=cred_obj.project_id)
            auth_obj.token = credentials.token
            auth_obj.refresh_token = credentials.refresh_token
            auth_obj.save()
        except GoogleAuthToken.DoesNotExist:
            auth_obj = GoogleAuthToken.objects.create(
                name=cred_obj.project_id,
                token=credentials.token,
                refresh_token=credentials.refresh_token
            )
            auth_obj.save()
        return Response(
            {
                "msg": "You have successfully re-generated token!!",
                "details": {
                    "token": credentials.token,
                    "refresh_token": credentials.refresh_token
                }
            },
            status=status.HTTP_200_OK
        )


class GoogleDriveFolders(viewsets.ViewSet):

    def list(self, request):
        try:
            cred_obj = GoogleAuthCredentials()
            info = cred_obj.get_credentials()
            credentials = Credentials.from_authorized_user_info(info=info)
            service = DriveService()
            folders = service.get_folder_service(credentials=credentials)
            for folder in folders:
                print(u'{0} ({1})'.format(folder['name'], folder['id']))
            return Response(
                {
                    "count": len(folders),
                    "folders": folders
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "error": "Something went wrong with credentials!",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        try:
            cred_obj = GoogleAuthCredentials()
            info = cred_obj.get_credentials()
            credentials = Credentials.from_authorized_user_info(info=info)
            service = DriveService()
            files = service.get_file_service(credentials=credentials, file_id=pk)
            for file in files:
                print(u'{0} ({1})'.format(file['name'], file['id']))
            return Response(
                {
                    "count": len(files),
                    "files": files
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "error": "Something went wrong with credentials!",
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class GoogleDriveFileDownload(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            cred_obj = GoogleAuthCredentials()
            info = cred_obj.get_credentials()
            credentials = Credentials.from_authorized_user_info(info=info)
            service = DriveService()
            file = service.download_file(credentials=credentials, file_id=pk)
            return Response(
                {
                    "msg": "You have successfully downloaded file!!",
                    "file_id": pk
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "error": "Something went wrong with credentials!",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
