from django.shortcuts import render
from rest_framework import generics, permissions, status, filters, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from django.db import models
from django.utils import timezone
from .models import LawyerProfile, LawyerRating
from .serializers import (
    LawyerProfileSerializer, LawyerProfileCreateSerializer, LawyerRatingSerializer,
    LawyerRatingCreateSerializer, PublicLawyerSerializer
)

# Create your views here.

class LawyerProfileCreateView(generics.CreateAPIView):
    """Create lawyer profile"""
    queryset = LawyerProfile.objects.all()
    serializer_class = LawyerProfileCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Ensure user doesn't already have a lawyer profile
        if LawyerProfile.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError("Lawyer profile already exists for this user")
        
        # Update user type to lawyer
        self.request.user.user_type = 'lawyer'
        self.request.user.save()
        serializer.save()

class LawyerProfileView(generics.RetrieveUpdateAPIView):
    """Get and update lawyer profile"""
    serializer_class = LawyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return LawyerProfile.objects.get(user=self.request.user)
        except LawyerProfile.DoesNotExist:
            raise NotFound("Lawyer profile not found")

class PublicLawyerListView(generics.ListAPIView):
    """Public listing of approved lawyers"""
    serializer_class = PublicLawyerSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchBackend, filters.OrderingFilter]
    filterset_fields = ['specializations', 'years_of_experience', 'consultation_fee']
    search_fields = ['user__first_name', 'user__last_name', 'law_firm_name', 'bio']
    ordering_fields = ['average_rating', 'total_reviews', 'consultation_fee', 'years_of_experience']
    ordering = ['-average_rating', '-total_reviews']
    
    def get_queryset(self):
        return LawyerProfile.objects.filter(status='approved')

class LawyerDetailView(generics.RetrieveAPIView):
    """Get detailed lawyer information"""
    serializer_class = PublicLawyerSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return LawyerProfile.objects.filter(status='approved')

class LawyerRatingCreateView(generics.CreateAPIView):
    """Rate a lawyer"""
    queryset = LawyerRating.objects.all()
    serializer_class = LawyerRatingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Check if user has already rated this lawyer
        lawyer = serializer.validated_data['lawyer']
        if LawyerRating.objects.filter(lawyer=lawyer, user=self.request.user).exists():
            raise serializers.ValidationError("You have already rated this lawyer")
        
        rating = serializer.save()
        
        # Update lawyer's average rating
        self.update_lawyer_rating(lawyer)
    
    def update_lawyer_rating(self, lawyer):
        ratings = LawyerRating.objects.filter(lawyer=lawyer)
        if ratings.exists():
            avg_rating = ratings.aggregate(avg=models.Avg('rating'))['avg']
            lawyer.average_rating = round(avg_rating, 2)
            lawyer.total_reviews = ratings.count()
            lawyer.save()

class LawyerRatingListView(generics.ListAPIView):
    """Get ratings for a specific lawyer"""
    serializer_class = LawyerRatingSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        lawyer_id = self.kwargs.get('lawyer_id')
        return LawyerRating.objects.filter(lawyer_id=lawyer_id).order_by('-created_at')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def lawyer_specializations(request):
    """Get all available lawyer specializations"""
    specializations = [
        {'value': choice[0], 'label': choice[1]} 
        for choice in LawyerProfile.SPECIALIZATION_CHOICES
    ]
    return Response(specializations)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_lawyer_profiles(request):
    """Get pending lawyer profiles for admin approval"""
    if request.user.user_type != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    pending_profiles = LawyerProfile.objects.filter(status='pending')
    serializer = LawyerProfileSerializer(pending_profiles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_lawyer_profile(request, profile_id):
    """Approve or reject lawyer profile"""
    if request.user.user_type != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        profile = LawyerProfile.objects.get(id=profile_id)
        action = request.data.get('action')  # 'approve' or 'reject'
        
        if action == 'approve':
            profile.status = 'approved'
            profile.verified_by = request.user
            profile.verification_date = timezone.now()
            profile.user.is_verified = True
            profile.user.save()
        elif action == 'reject':
            profile.status = 'rejected'
            profile.rejection_reason = request.data.get('reason', '')
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile.save()
        
        return Response({
            'message': f'Lawyer profile {action}ed successfully',
            'profile': LawyerProfileSerializer(profile).data
        })
        
    except LawyerProfile.DoesNotExist:
        return Response({'error': 'Lawyer profile not found'}, status=status.HTTP_404_NOT_FOUND)
