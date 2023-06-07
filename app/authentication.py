import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from .models import Recruiters, User

class SafeJWTAuthentication(BaseAuthentication):
    '''
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    '''

    def authenticate(self, request):

        authorization_heaader = request.headers.get('Authorization')

        if not authorization_heaader:
            return None
        try:
           
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(id=payload['user_id']).first()
        if user:
            return (user, None)
        recruiter = Recruiters.objects.filter(id=payload['user_id']).first()
        if recruiter:
            return (recruiter, None)
       