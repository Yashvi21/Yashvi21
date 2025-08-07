from rest_framework import serializers
from .models import ChatSession, ChatMessage, LawyerUserConversation, LawyerUserMessage, AIResponse
from authentication.serializers import UserSerializer

class ChatSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ChatSession
        fields = '__all__'
        read_only_fields = ('user',)

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = ('created_at',)

class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('session', 'message_type', 'content', 'metadata')

class LawyerUserConversationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    lawyer = UserSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = LawyerUserConversation
        fields = '__all__'
        read_only_fields = ('user', 'lawyer', 'created_at', 'updated_at')
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return LawyerUserMessageSerializer(last_message).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0

class LawyerUserMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = LawyerUserMessage
        fields = '__all__'
        read_only_fields = ('sender', 'created_at', 'read_at')

class LawyerUserMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerUserMessage
        fields = ('conversation', 'content')

class AIResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AIResponse
        fields = '__all__'
        read_only_fields = ('user', 'created_at')