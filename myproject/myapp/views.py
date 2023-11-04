from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer
from .firebase import firebase_admin
from firebase_admin import auth
from django.core.exceptions import ObjectDoesNotExist
import random
import string
from .serializers import FullNameSerializer
from pymongo import MongoClient
from bson import ObjectId

def generate_unique_username(email):
    base_username = email.split('@')[0]
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    username = f"{base_username}_{random_string}"
    return username

def validate_username_email(username, email):
    client = MongoClient('mongodb://localhost:27017/bewyse_ass')
    user_collection = client.bewyse_ass.myapp_user

    if user_collection.find_one({'username': username}):
        return 1
    
    if user_collection.find_one({'email': email}):
        return 2
    
    return 0

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not email or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 8:
        return Response({'error': 'This password is too short. It must contain at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)

    if (username and len(username) > 100) or len(email) > 100 or len(password) > 100 or (first_name and len(first_name) > 100) or (last_name and len(last_name) > 100):
        return Response({'error': 'Only 100 characters are allowed for a field'}, status=status.HTTP_400_BAD_REQUEST)
     
    if not username:
        username = generate_unique_username(email)

    flag = validate_username_email(username, email)
    if flag == 1:
        return Response({'error': 'A user with that username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    if flag == 2:
        return Response({'error': 'A user with that Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
    return Response({'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)

def validate_user(username, password):
    client = MongoClient('mongodb://localhost:27017/bewyse_ass')
    user_collection = client.bewyse_ass.myapp_user
    user_data = user_collection.find_one({'username': username})
    
    if user_data:
        if user_data['password'] == password:
            return user_data
        else:
            return 0
    
    return None

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = validate_user(username, password)
    if user == 0 or user is None:
        return Response({'error': 'Username or password is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

    custom_token = auth.create_custom_token(uid=str(user['_id']))
    serializer = FullNameSerializer(user)

    response_data = {
        'username': user["username"],
        'email': user["email"],
        'full_name': serializer.data["full_name"],
        'custom_token': custom_token
    }
    return Response(response_data, status=status.HTTP_200_OK)

def verify_custom_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return None

@api_view(['GET'])
def view_profile(request):
    id_token = request.META.get('HTTP_AUTHORIZATION', '')
    decoded_token = verify_custom_token(id_token)
    if decoded_token is None:
        return Response({'detail': 'Invalid custom_token'}, status=status.HTTP_401_UNAUTHORIZED)

    _id = decoded_token["uid"]
    client = MongoClient('mongodb://localhost:27017/bewyse_ass')
    user_collection = client.bewyse_ass.myapp_user

    user_data = user_collection.find_one({'_id': ObjectId(_id) })

    if user_data is None:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    full_name = FullNameSerializer(user_data).data["full_name"]
    response_data = {
        'username': user_data.get('username'),
        'email': user_data.get('email'),
        'full_name': full_name,
    }

    return Response(response_data,  status=status.HTTP_200_OK)

@api_view(['POST'])
def edit_profile(request):
    id_token = request.META.get('HTTP_AUTHORIZATION', '')
    decoded_token = verify_custom_token(id_token)
    if decoded_token is None:
        return Response({'detail': 'Invalid custom_token'}, status=status.HTTP_401_UNAUTHORIZED)
    _vid = decoded_token["uid"]
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    username = request.data.get('username')

    client = MongoClient('mongodb://localhost:27017/bewyse_ass')
    user_collection = client.bewyse_ass.myapp_user
    user_data = user_collection.find_one({'_id': ObjectId(_vid) })
    if user_data is None:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    check_user_data = user_collection.find_one({'username': username})
    if check_user_data is not None and user_data['email'] != check_user_data['email']:
        return Response({'detail': f'User already exists with the username {username}'}, status=status.HTTP_409_CONFLICT)
    if first_name is not None:
        user_data['first_name'] = first_name
    if last_name is not None:
        user_data['last_name'] = last_name
    if username is not None:
        user_data['username'] = username
    user_collection.update_one({'_id': user_data['_id']}, {'$set': user_data})

    full_name = FullNameSerializer(user_data).data["full_name"]
    response_data = {
        'username': user_data.get('username'),
        'email': user_data.get('email'),
        'full_name': full_name,
    }
    return Response(response_data,  status=status.HTTP_200_OK)
