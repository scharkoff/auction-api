from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

class AuthService:
    def register(self, username, password, email):
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            serialized_user = self.serializeUser(user)
            return {'message': 'Пользователь успешно зарегистрирован', 'data': serialized_user}
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def login(self, request, username, password):
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                serialized_user = self.serializeUser(user)
                return {'message': 'Пользователь успешно авторизован', 'data': serialized_user}
            else:
                raise Exception('Неправильный логин или пароль')
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def logout(self, request):
        try:
            logout(request)
            return {'message': 'Успешный выход из аккаунта'}
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def serializeUser(self, user):
        serialized_user = {
            'username': user.username,
            'email': user.email,
            'password': user.password,
        }
        return serialized_user
