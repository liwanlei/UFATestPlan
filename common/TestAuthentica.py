""" 
@author: lileilei
@file: TestAuthentica.py 
@time: 2018/5/5 18:50 
"""
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from app.models import Newusers
class ApptestAuten(BaseAuthentication):
    def authenticate(self, request):
        val = request.query_params.get('token')
        user=Newusers.objects.filter(token=val).first()
        if not user:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return ('认证用户')
    def authenticate_header(self, request):
        pass