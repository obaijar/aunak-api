from django.shortcuts import render

# Create your views here.
from rest_framework import generics,permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializer import UserSerializer , RegisterSerializer

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        serializer= self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user":UserSerializer(user,context= self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1]
        })


from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from knox.models import AuthToken

class LoginAPI(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')  
        user = authenticate(request, username=username, password=password) 
        if user:
            _, token = AuthToken.objects.create(user)
            return Response({'user': user.username, 'token': token})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
