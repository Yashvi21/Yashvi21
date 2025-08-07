from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, logout_view, UserProfileView,
    UserProfileDetailView, ChangePasswordView, user_details
)

app_name = 'authentication'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/details/', UserProfileDetailView.as_view(), name='profile-details'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('user/', user_details, name='user-details'),
]