from rest_framework import serializers
from accounts.models import User
from chats.models import ChatHistory, ChatFeedback, ModelVersion
from django.contrib.auth import get_user_model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_num', 'role', 'profile_pic', 'is_active','status', )

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ('id', 'user', 'user_input', 'ai_response', 'intent', 'timestamp')