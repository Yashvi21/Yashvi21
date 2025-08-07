from django.urls import path
from .views import (
    ChatSessionListCreateView, ChatSessionDetailView, ChatMessageListView,
    ai_chat, LawyerUserConversationListView, LawyerUserConversationCreateView,
    LawyerUserMessageListView, LawyerUserMessageCreateView
)

app_name = 'chat'

urlpatterns = [
    # AI Chat endpoints
    path('sessions/', ChatSessionListCreateView.as_view(), name='chat-sessions'),
    path('sessions/<int:pk>/', ChatSessionDetailView.as_view(), name='chat-session-detail'),
    path('sessions/<int:session_id>/messages/', ChatMessageListView.as_view(), name='chat-messages'),
    path('ai/', ai_chat, name='ai-chat'),
    
    # Lawyer-User messaging endpoints
    path('conversations/', LawyerUserConversationListView.as_view(), name='conversations'),
    path('conversations/create/', LawyerUserConversationCreateView.as_view(), name='create-conversation'),
    path('conversations/<int:conversation_id>/messages/', LawyerUserMessageListView.as_view(), name='conversation-messages'),
    path('conversations/messages/', LawyerUserMessageCreateView.as_view(), name='send-message'),
]