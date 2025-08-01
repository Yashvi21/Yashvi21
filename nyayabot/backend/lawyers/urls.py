from django.urls import path
from .views import (
    LawyerProfileCreateView, LawyerProfileView, PublicLawyerListView,
    LawyerDetailView, LawyerRatingCreateView, LawyerRatingListView,
    lawyer_specializations, pending_lawyer_profiles, approve_lawyer_profile
)

app_name = 'lawyers'

urlpatterns = [
    path('profile/create/', LawyerProfileCreateView.as_view(), name='create-profile'),
    path('profile/', LawyerProfileView.as_view(), name='profile'),
    path('public/', PublicLawyerListView.as_view(), name='public-list'),
    path('<int:pk>/', LawyerDetailView.as_view(), name='detail'),
    path('rate/', LawyerRatingCreateView.as_view(), name='rate'),
    path('<int:lawyer_id>/ratings/', LawyerRatingListView.as_view(), name='ratings'),
    path('specializations/', lawyer_specializations, name='specializations'),
    path('pending/', pending_lawyer_profiles, name='pending'),
    path('<int:profile_id>/approve/', approve_lawyer_profile, name='approve'),
]