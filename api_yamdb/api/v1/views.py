from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings

from users.models import User
from .serializers import (AuthSerializer, GetTokenSerializer, UserSerializer)
from .permissions import (UsersPermission, IsAdminOrReadOnly,
                          IsAuthorOrModerator)


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

    def token(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=request.data.get('username'))
            if not default_token_generator.check_token(
                user, request.data.get('confirmation_code')
            ):
                return Response(
                    'Неверный код подтверждения',
                    status=status.HTTP_400_BAD_REQUEST)
            token = {'token': str(AccessToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class UsersViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [UsersPermission]
        lookup_field = 'username'

        @action(
            methods=['GET', 'PATCH'], detail=False, url_path='me',
            permission_classes=(permissions.IsAuthenticated,)
        )
        def get_patch_me(self, request):
            user = request.user
            if request.method == 'GET':
                serializer = self.get_serializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
