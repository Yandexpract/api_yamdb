from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .permissions import (IsAdminOrReadOnly, IsAuthorOrModerator,
                          UsersPermission)
from .serializers import (AuthSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          GetTokenSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer)


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


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModerator,
                          permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModerator,
                          permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
