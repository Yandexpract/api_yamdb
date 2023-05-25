from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import SignUpView, TokenView

router = DefaultRouter()
router.register()

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUpView.as_view()),
    path('token/', TokenView.as_view())]
