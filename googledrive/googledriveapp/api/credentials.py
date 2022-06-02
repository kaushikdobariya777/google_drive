from django.conf import settings
from googledriveapp.models import GoogleAuthToken


class GoogleAuthCredentials:

    def __init__(self):
        self.client_id = settings.CLIENT_ID
        self.client_secret = settings.CLIENT_SECRET
        self.project_id = settings.PROJECT_ID
        self.auth_uri = settings.AUTH_URI
        self.token_uri = settings.TOKEN_URI
        self.scopes = settings.SCOPES
        self.redirect_uri = settings.REDIRECT_URI
        self.login_hint = settings.LOGIN_HINT

    def get_client_config(self):
        client_config = {
            "web": {
                "client_id": self.client_id,
                "project_id": self.project_id,
                "auth_uri": self.auth_uri,
                "token_uri": self.token_uri,
                "client_secret": self.client_secret,
                "redirect_uris": [self.redirect_uri]
            }
        }
        data = {
            "client_config": client_config,
            "scopes": self.scopes,
            "login_hint": self.login_hint,
            "redirect_uri": self.redirect_uri
        }
        return data

    def get_credentials(self):
        auth_obj = GoogleAuthToken.objects.get(name=self.project_id)
        creds = {
            "token": auth_obj.token,
            "refresh_token": auth_obj.refresh_token,
            "token_uri": self.token_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scopes": self.scopes
        }
        return creds
