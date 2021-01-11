from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserProfileView, ClientViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('form',ClientViewSet,basename='ClientForm')

urlpatterns = [
    path('signup/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('pro/', UserProfileView.as_view()),
    path('',include(router.urls)),
]