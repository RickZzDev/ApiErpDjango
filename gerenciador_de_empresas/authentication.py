from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.response import Response
import requests

class TokenAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        tokenHeader = request.headers['Token'] # get the token request header
        token = {
            "token":tokenHeader
        }
        if not token: # no token passed in request header
            raise exceptions.AuthenticationFailed("no such token") # authentication did not succeed
            
        response = requests.post(url = "https://api.upp.vc/token/decode", json = token)
        if(response.status_code == 200):
            return (response, None)
        else:
            raise exceptions.AuthenticationFailed({"msg":"Token inválido"})

   