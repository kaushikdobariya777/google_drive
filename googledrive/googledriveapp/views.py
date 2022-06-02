from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import requests


class TestGoogleAuthViewSet(viewsets.ViewSet):

    def create(self, request):
        url = "https://oauth2.googleapis.com/token"
        # url = "https://www.googleapis.com/oauth2/v4/token"
        query_string = {
            "client_id": "244010260969-r65dbjauct9r2if9coivpers9dvkhb8c.apps.googleusercontent.com",
            "client_secret": "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"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            "grant_type": "authorization_code",
            "client_id": "244010260969-r65dbjauct9r2if9coivpers9dvkhb8c.apps.googleusercontent.com",
            "client_secret": "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",
            "code": "4/P7q7W91a-oMsCeLvIaQm6bTrgtp7",
            "redirect_uri": "http://localhost"
        }
        response = requests.request(
            method="POST",
            url=url,
            data=data,
            headers=headers
        )
        print("Response....", response.json())
        return Response(response.json(), status=status.HTTP_200_OK)

# https://accounts.google.com/o/oauth2/v2/auth?
# scope=https://www.googleapis.com/auth/drive.file&
#  access_type=offline&
#  include_granted_scopes=true&
#  response_type=code&
#  state=state_parameter_passthrough_value&
#  redirect_uri=http://localhost&
#  client_id=244010260969-r65dbjauct9r2if9coivpers9dvkhb8c.apps.googleusercontent.com
#
#
# http://localhost/?
# state=state_parameter_passthrough_value&
# code=4/0AX4XfWiLq_sJ_p8uOgmqtKa0e3heFEoZ4Mq0nHw0aPNdHaWru1J1qemVjLmMgQoI8a-Iog&
# scope=https://www.googleapis.com/auth/drive.file
#
#
# POST /token HTTP/1.1
# Host: oauth2.googleapis.com
# Content-Type: application/x-www-form-urlencoded
#
# code=4/P7q7W91a-oMsCeLvIaQm6bTrgtp7&
# client_id=your_client_id&
# client_secret=your_client_secret&
# redirect_uri=https%3A//oauth2.example.com/code&
# grant_type=authorization_code

# curl \
# --request POST \
# --data "code=4/P7q7W91a-oMsCeLvIaQm6bTrgtp7&client_id=244010260969-r65dbjauct9r2if9coivpers9dvkhb8c.apps.googleusercontent.com&client_secret=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&redirect_uri=http://localhost&grant_type=authorization_code" \
# https://accounts.google.com/o/oauth2/token