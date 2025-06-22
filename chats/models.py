from django.db import models
from accounts.models import User  # or your custom user model

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    user_input = models.TextField()
    ai_response = models.TextField()
    intent = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Chat on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
class ChatFeedback(models.Model):
    chat = models.ForeignKey(ChatHistory, on_delete=models.CASCADE)
    is_helpful = models.BooleanField()
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Chat #{self.chat.id}"
class ModelVersion(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)