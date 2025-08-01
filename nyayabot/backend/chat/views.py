from django.shortcuts import render
from rest_framework import generics, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
import openai
import time
from django.conf import settings
from authentication.models import User
from .models import ChatSession, ChatMessage, LawyerUserConversation, LawyerUserMessage, AIResponse
from .serializers import (
    ChatSessionSerializer, ChatMessageSerializer, ChatMessageCreateSerializer,
    LawyerUserConversationSerializer, LawyerUserMessageSerializer, 
    LawyerUserMessageCreateSerializer, AIResponseSerializer
)

# Initialize OpenAI
openai.api_key = settings.OPENAI_API_KEY

class ChatSessionListCreateView(generics.ListCreateAPIView):
    """List and create chat sessions"""
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, delete chat session"""
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

class ChatMessageListView(generics.ListAPIView):
    """Get messages for a chat session"""
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        return ChatMessage.objects.filter(
            session_id=session_id,
            session__user=self.request.user
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def ai_chat(request):
    """Send message to AI and get response"""
    try:
        session_id = request.data.get('session_id')
        user_message = request.data.get('message')
        
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create session
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, user=request.user)
            except ChatSession.DoesNotExist:
                return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            session = ChatSession.objects.create(
                user=request.user,
                title=user_message[:50] + "..." if len(user_message) > 50 else user_message
            )
        
        # Save user message
        user_msg = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=user_message
        )
        
        # Generate AI response
        start_time = time.time()
        ai_response = generate_legal_ai_response(user_message)
        response_time = time.time() - start_time
        
        # Save AI response
        ai_msg = ChatMessage.objects.create(
            session=session,
            message_type='ai',
            content=ai_response['content'],
            metadata=ai_response.get('metadata', {})
        )
        
        # Save AI response for analytics
        AIResponse.objects.create(
            user=request.user,
            query=user_message,
            response=ai_response['content'],
            response_time=response_time,
            confidence_score=ai_response.get('confidence_score'),
            category=ai_response.get('category')
        )
        
        # Update session
        session.updated_at = timezone.now()
        session.save()
        
        return Response({
            'session_id': session.id,
            'user_message': ChatMessageSerializer(user_msg).data,
            'ai_response': ChatMessageSerializer(ai_msg).data
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_legal_ai_response(user_message):
    """Generate AI response using OpenAI"""
    try:
        # Define legal prompt
        legal_prompt = f"""
        You are NyayaBot, an AI legal assistant for Indian law. Provide helpful, accurate legal information while clearly stating that you're not a substitute for professional legal advice.
        
        User Question: {user_message}
        
        Please provide:
        1. A clear, helpful response about the legal topic
        2. Relevant Indian laws or sections if applicable
        3. General guidance on next steps
        4. A reminder to consult with a qualified lawyer for specific legal advice
        
        Keep the response informative but accessible to non-lawyers.
        """
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI legal assistant specializing in Indian law."},
                {"role": "user", "content": legal_prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        ai_content = response.choices[0].message.content
        
        # Categorize the legal query
        category = categorize_legal_query(user_message)
        
        return {
            'content': ai_content,
            'confidence_score': 0.8,  # You can implement confidence scoring
            'category': category,
            'metadata': {
                'model': 'gpt-3.5-turbo',
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
        }
        
    except Exception as e:
        return {
            'content': "I apologize, but I'm experiencing technical difficulties. Please try again later or contact a legal professional for immediate assistance.",
            'confidence_score': 0.0,
            'category': 'error',
            'metadata': {'error': str(e)}
        }

def categorize_legal_query(message):
    """Categorize legal query for analytics"""
    message_lower = message.lower()
    
    categories = {
        'family': ['divorce', 'marriage', 'custody', 'alimony', 'domestic'],
        'criminal': ['crime', 'police', 'fir', 'arrest', 'bail', 'court'],
        'property': ['property', 'land', 'rent', 'lease', 'tenant', 'landlord'],
        'consumer': ['consumer', 'product', 'service', 'refund', 'complaint'],
        'cyber': ['cyber', 'online', 'fraud', 'digital', 'internet'],
        'labour': ['job', 'employment', 'salary', 'work', 'employee'],
        'civil': ['civil', 'contract', 'agreement', 'dispute']
    }
    
    for category, keywords in categories.items():
        if any(keyword in message_lower for keyword in keywords):
            return category
    
    return 'general'

# Lawyer-User Conversation Views
class LawyerUserConversationListView(generics.ListAPIView):
    """List conversations for current user"""
    serializer_class = LawyerUserConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return LawyerUserConversation.objects.filter(
            Q(user=user) | Q(lawyer=user)
        ).order_by('-updated_at')

class LawyerUserConversationCreateView(generics.CreateAPIView):
    """Start conversation with a lawyer"""
    serializer_class = LawyerUserConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        lawyer_id = self.request.data.get('lawyer_id')
        try:
            lawyer = User.objects.get(id=lawyer_id, user_type='lawyer')
            serializer.save(user=self.request.user, lawyer=lawyer)
        except User.DoesNotExist:
            raise serializers.ValidationError("Lawyer not found")

class LawyerUserMessageListView(generics.ListAPIView):
    """Get messages for a conversation"""
    serializer_class = LawyerUserMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = LawyerUserConversation.objects.get(
            id=conversation_id,
            Q(user=self.request.user) | Q(lawyer=self.request.user)
        )
        
        # Mark messages as read
        LawyerUserMessage.objects.filter(
            conversation=conversation,
            is_read=False
        ).exclude(sender=self.request.user).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return conversation.messages.all()

class LawyerUserMessageCreateView(generics.CreateAPIView):
    """Send message in conversation"""
    serializer_class = LawyerUserMessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        
        # Verify user is part of conversation
        if conversation.user != self.request.user and conversation.lawyer != self.request.user:
            raise serializers.ValidationError("You are not part of this conversation")
        
        serializer.save(sender=self.request.user)
        
        # Update conversation timestamp
        conversation.updated_at = timezone.now()
        conversation.save()
