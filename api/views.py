from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import messages
from rest_framework.response import Response
from accounts.utility import generate_username
from .serializers import UserSerializer, ChatHistorySerializer
from accounts.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
import json
import os
from datetime import datetime
import pickle
import random
from chats.models import ChatHistory, ChatFeedback
# Create your views here.
MODEL_PATH =  os.path.join("ml_workings", "intents.pkl")
VECTORIZER_PATH = os.path.join("ml_workings", "vectorizer.pkl")
ENCODER = os.path.join("ml_workings", "label_encoder.pkl")

with open (MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
with open("ml_workings/intents.json", "r") as w:
    intents_data = json.load(w)
with open(VECTORIZER_PATH, 'rb') as d:
    vectorizer = pickle.load(d)
with open(ENCODER, 'rb') as e:
    encoder = pickle.load(e)

def generate_chat_title(user_input):
    return user_input[:50] + "..." if len(user_input) > 50 else user_input
@api_view(['POST'])
def signup(request):
    print("🔍 RAW REQUEST DATA:", request.data)
    print("📦 DATABASE_URL:", os.environ.get("DATABASE_URL"))
    full_name = request.data.get('full_name', '').strip()
    if not full_name:
        print("❌ Full name is missing")
        return Response({'messages': 'Full name is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Split full_name into first and last
    names = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')
    first_name = names[0]
    last_name = names[1] if len(names) > 1 else ''
    print("✅ First Name:", first_name)
    print("✅ Last Name:", last_name)

    # Prepare user data
    user_data = {
        'username': generate_username(first_name, last_name),
        'email': request.data.get('email'),
        'first_name': first_name,
        'last_name': last_name,
        'phone_num': request.data.get('phone_num'),
        'role': request.data.get('role'),
        'password': make_password(request.data.get('password')),
        'profile_pic': request.FILES.get('profile_pic'),
    }

    print("📦 User data prepared for serializer:", user_data)

    user = UserSerializer(data=user_data)

    if user.is_valid():
        print("✅ Serializer is valid")
        try:
            user = user.save()
            print("✅ User saved to DB:", user)
            token = Token.objects.create(user=user)
            print("🔑 Token created:", token.key)

            json = UserSerializer(user).data
            json['token'] = token.key

            context = {
                'email': json['email'],
                'username': json['username'],
                'first_name': json['first_name'],
                'last_name': json['last_name'],
                'phone_num': json['phone_num'],
                'token': json['token']
            }

            messages = "Account created successfully, please check your email for verification"
            print("🎉 Signup successful")
            return Response({'messages': messages, 'token': token.key}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("❌ ERROR SAVING USER:", str(e))
            return Response({'messages': 'Registration failed, internal error occurred'}, status=500)

    else:
        print("❌ Serializer errors:", user.errors)
        return Response({
            'messages': "Registration failed, please try again",
            'errors': user.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    print("RAW LOGIN DATA:", request.data)
    email = request.POST.get('email').strip()
    password= request.POST.get('password').strip()
    
    if not email or not password:
        print("📧 EMAIL VALUE:", repr(request.data.get('email')))
        print("🔑 PASSWORD VALUE:", repr(request.data.get('password')))
        return Response({'messages': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'messages': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    user = authenticate(request, email=email, password=password)
    if user:
        if user.is_active:
            if user.status == 'del':
                return Response({'messages': 'Your account has been deleted'}, status=status.HTTP_403_FORBIDDEN)
            if user.status == '0':
                return Response({'messages': 'Your account is inactive'}, status=status.HTTP_403_FORBIDDEN)
            if user.status == '2':
                return Response({'messages': 'Your account is unverified'}, status=status.HTTP_403_FORBIDDEN)
            token, created = Token.objects.get_or_create(user=user)
            json = UserSerializer(user).data
            json['token'] = token.key
            context = {
                'email': json['email'],
                'username': json['username'],
                'first_name': json['first_name'],
                'last_name': json['last_name'],
                'phone_num': json['phone_num'],
            }           
            return Response({'messages': 'Login successful', 'user': context}, status=status.HTTP_200_OK)
        else:
            return Response({'messages': 'Your account is inactive'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'messages': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])    
def logout_user(request):
    user = request.user
    if user.is_active:
        Token.objects.filter(user=user).delete()
        return Response({'messages': 'Logout successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'messages': 'You are not logged in'}, status=status.HTTP_401_UNAUTHORIZED)                                                                                             
@api_view(["POST"])
@csrf_exempt
def ai_chat_response(request):
    try:
        user_input = request.data.get('messages', '')
    except Exception as e:
        print("UNPICKLE ERROR:", str(e))
        return Response({"error": str(e)}, status=500)

    if not user_input:
        return Response({"error": "No input was provided"}, status=400)

    try:
        x_input = vectorizer.transform([user_input])
        prediction_index = model.predict(x_input)[0]
        print(f"PREDICTION:{prediction_index}")

        predicted_label = encoder.inverse_transform([prediction_index])[0]

        response_text = "I'm not sure how to respond to that."
        for intent in intents_data["intents"]:
            if intent["tag"] == predicted_label:
                response_text = random.choice(intent["responses"])
                break
        ChatHistory.objects.create(
        user = request.user if request.user.is_authenticated else None,
        title=generate_chat_title(user_input),
        user_input=user_input,
        ai_response=response_text,
        intent=predicted_label
    )
    except Exception as e:
        print("PREDICTION ERROR:", str(e))
        return Response({"error": str(e)}, status=500)
    
    return Response({
        "user_input": user_input,
        "intent": predicted_label,
        "response": response_text,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }, status=200)
@api_view(['POST'])
def ai_chat_feedback(request):
    chat_id = request.POST.get('chat_id')
    is_helpful = request.POST.get('is_helpful') 
    comment = request.POST.get('comment', '')

    try:
        chat = ChatHistory.objects.get(id=chat_id)
        feedback = ChatFeedback.objects.create(
            chat=chat,
            is_helpful=is_helpful,
            comment=comment
        )
        return Response({'message': 'Feedback submitted successfully'}, status=status.HTTP_201_CREATED)
    except ChatHistory.DoesNotExist:
        return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def get_chat_history(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.query_params.get("user_id")
    if not user_id:
        return Response({"error": "user_id is required"}, status=400)
    chat_history = ChatHistory.objects.filter(user=user_id).order_by('-timestamp')
    data = [{
        "user_input": chat.user_input,
        "ai_response": chat.ai_response,
        "intent": chat.intent,
        "timestamp": chat.timestamp
    } for chat in chat_history]

    return Response(data, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_chat_session(request):
    user_id = request.query_params.get("user_id")
#     if not request.user.is_authenticated:
#         return Response({
#             "error": "Authentication required"
#         }, status=status.HTTP_401_UNAUTHORIZED)
    session_data = ChatHistory.objects.filter(user=user_id).order_by('-timestamp').values('id', 'title','user_input', 'timestamp')
    return Response(session_data, status=status.HTTP_200_OK)