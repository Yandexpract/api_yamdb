from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import  SignUpView, TokenView, UsersViewSet
from .views import CommentViewSet, ReviewViewSet, GenreViewSet, TitleViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'users', UsersViewSet)

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
    # path('users/me/', UserUpdateView.as_view(), name='user-update'),
    path('auth/signup/', SignUpView.as_view()),
    path('auth/token/', TokenView.as_view()),
    
]
