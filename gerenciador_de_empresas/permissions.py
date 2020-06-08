from rest_framework import permissions
import jwt
import os

class PermClass(permissions.BasePermission):
 
    message = 'Você não tem a permissão para isso.'
    def has_permission(self, request, view):
        if('Token' in request.headers):
            token = request.headers['Token']
            decoded = jwt.decode(token, verify=False)
            if 'cognito:groups' in decoded:
                if os.getenv("FOLHA_PROD"):
                    if "FOLHA" in decoded['cognito:groups']:
                        return True
                    else:
                        return False
                else:
                    if "FOLHA" or 'FOLHA_DEV' in decoded['cognito:groups']:
                        return True
                    else:
                        return False
            else:
                return False            
        else:
            if request.user and request.user.is_authenticated:
                return True
            else:
                return False    

      


              