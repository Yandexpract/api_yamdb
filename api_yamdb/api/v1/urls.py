from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import (SignUpView, TokenView, UsersViewSet,
                    CommentViewSet, ReviewViewSet, GenreViewSet,
                    TitleViewSet, CategoryViewSet)
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'users', UsersViewSet, basename='user')

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenView.as_view(), name='create_token'),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
]
