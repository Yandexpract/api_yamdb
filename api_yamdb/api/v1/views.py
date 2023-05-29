from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from django.db.models import Avg

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .permissions import (IsAdminOrReadOnly, IsAuthorOrModerator,
                          UsersPermission,)
from .serializers import (SignupSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          GetTokenSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer,
                          UsersMeSerializer)


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def send_confirmation_code(request):
        serializer = SignupSerializer(data=request.data)
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
    permission_classes = (UsersPermission, permissions.IsAuthenticated,)
    lookup_field = 'username'


class UsersMeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Метод GET."""
        me = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """Метод PATCH."""
        me = get_object_or_404(User, username=request.user.username)
        serializer = UsersMeSerializer(me, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GetTokenSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrModerator,
                          permissions.IsAuthenticatedOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerator,
                          permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerator,
                          permissions.IsAuthenticatedOrReadOnly,)
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
