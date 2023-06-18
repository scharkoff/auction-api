from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from auction.serializers.user import UserSerializer
from rest_framework import serializers
from .usersServiceInterface import IUsersService

class UserService(IUsersService):
    def __init__(self) -> None:
        pass
    
    def getAll():
        try:
            users = User.objects.all()
            serializedUsers = UserSerializer(users, many=True)
            return {'message': 'Пользователи успешно найдены', 'data': serializedUsers}
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def getById(userId):
        try:
            user = User.objects.get(id=userId)
            serializedUser = UserSerializer(user)
            return {'message': 'Пользователь успешно найден', 'data': serializedUser}
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(username, password, email):
        try:
            serializer = UserSerializer(data={'username': username, 'password': password, 'email': email})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            serializedUser = UserSerializer(user)

            return {'message': 'Пользователь успешно создан', 'data': serializedUser}
        except serializers.ValidationError as e:
            return Response({'message': e.detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(userId, username=None, password=None, email=None):
        try:
            user = User.objects.get(id=userId)
            if username:
                user.username = username
            if password:
                user.password = password
            if email:
                user.email = email
            user.save()
            serializedUser = UserSerializer(user)

            return {'message': 'Данные пользователя успешно изменены', 'data': serializedUser}
        except serializers.ValidationError as e:
            return Response({'message': e.detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(userId):
        try:
            user = User.objects.get(id=userId)
            user.delete()

            return {'message': 'Пользователь успешно удален'}
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
