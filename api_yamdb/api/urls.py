from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserUpdateView, UserCreateView

urlpatterns = [
    path('api/v1/users/me/', UserUpdateView.as_view(), name='user-update'),
    path('api/v1/users/', UserCreateView.as_view(), name='user-create'),
    path('api/v1/auth/signup/', ...),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
