from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('users/signup/', views.signup, name='signup'),
    path('users/login/', views.login_user, name='login'),
    path('ai_chats/', views.ai_chat_response, name="chat_response"),
    path("ai_chats/feedback/", views.ai_chat_feedback, name="chat_feedback"),
    path("chats/history/", views.get_chat_history, name="chat_history"),
    path("chats/get_chat_session/", views.get_chat_session, name="get_chat_session"),
    path('users/activate/', views.activate_user),
    path('users/user_profile/', views.user_profile, name='user_profile'),
    path('users/update_profile/', views.update_user_profile, name='update_profile'),
]