from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from django.conf import settings

from users.models import User
from .serializers import (AuthSerializer, GetTokenSerializer)
from .permissions import (IsAuthorOrReadOnly)


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny)

    def send_confirmation_code(request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email'))
            confirmation_code = default_token_generator.make_token(user)
            send_mail(f'Ваш код подтверждения - {confirmation_code}',
                      settings.SEND_EMAIL,
                      [request.data.get('email')])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    permission_classes = (permissions.AllowAny)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
