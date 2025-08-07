from rest_framework import serializers
from .models import LawyerProfile, LawyerRating
from authentication.serializers import UserSerializer

class LawyerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = LawyerProfile
        fields = '__all__'
        read_only_fields = ('user', 'status', 'average_rating', 'total_reviews', 
                          'total_consultations', 'verified_by', 'verification_date')

class LawyerProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerProfile
        fields = ('bar_council_id', 'bar_council_certificate', 'specializations', 
                 'years_of_experience', 'education', 'law_firm_name', 'office_address',
                 'consultation_fee', 'languages_spoken', 'bio', 'available_days',
                 'available_time_start', 'available_time_end', 'identity_proof', 
                 'degree_certificate')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class LawyerRatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = LawyerRating
        fields = '__all__'
        read_only_fields = ('user',)

class LawyerRatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerRating
        fields = ('lawyer', 'rating', 'review')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PublicLawyerSerializer(serializers.ModelSerializer):
    """Public serializer for lawyer listing - excludes sensitive information"""
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = LawyerProfile
        fields = ('id', 'user', 'specializations', 'years_of_experience', 'law_firm_name',
                 'consultation_fee', 'languages_spoken', 'bio', 'average_rating', 
                 'total_reviews', 'total_consultations')
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'profile_picture': str(obj.user.profile_picture) if obj.user.profile_picture else None,
            'city': obj.user.city,
            'state': obj.user.state
        }