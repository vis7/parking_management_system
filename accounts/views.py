import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .serializers import RegistrationSerializer
from .models import User
from drf_yasg.utils import swagger_auto_schema


class RegistrationView(APIView):
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = {}
            user = serializer.save()
            # sending token for further authenticate requests
            token = Token.objects.get_or_create(user=user)[0].key
            data["username"] = user.username
            data["email"] = user.email
            data["token"] = token
            data["message"] = "user created successfully"
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        # try to optimise using authenticate
        data = {}
        request_body = request.data
        username = request_body["username"]
        password = request_body["password"]

        user = get_object_or_404(User, username=username)
        token = Token.objects.get_or_create(user=user)[0].key

        if not check_password(password, user.password):
            return Response(
                {"message": "incorrect password"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if user and user.is_active:
            login(request, user)
            data["message"] = "login successful"
            data["username"] = username
            data["token"] = token
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "account not exist or active"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "logout successful"}, status=status.HTTP_200_OK)
