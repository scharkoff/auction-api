from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from auction.models.user import UserSerializer

class AuthController:
    def __init__(self) -> None:
        pass

    @staticmethod
    @csrf_exempt
    @api_view(['POST'])
    def register(request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')

            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                serializer = UserSerializer(user)
                serialized_user = serializer.data
                return Response({'message': 'Пользователь успешно зарегистрирован', 'data': serialized_user}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    @csrf_exempt  
    @api_view(['POST'])  
    def login(request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user = User.objects.get(username=username)
                serializer = UserSerializer(user)
                serialized_user = serializer.data
                return Response({'message': 'Пользователь успешно авторизован', 'data': serialized_user}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Неправильный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    @csrf_exempt
    @api_view(['POST'])
    def logout(request):
        try:
            logout(request)
            return Response({'message': 'Успешный выход из аккаунта'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
