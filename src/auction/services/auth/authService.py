from django.contrib.auth import authenticate, login, logout
from auction.models.user import UserSerializer
from rest_framework import serializers
from .authServiceInterface import IAuthService

class AuthService(IAuthService):
    def register(self, username, password, email):
        try:
            serializer = UserSerializer(data={'username': username, 'password': password, 'email': email})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            serialized_user = self.serializeUser(user)
            return {'message': 'Пользователь успешно зарегистрирован', 'data': serialized_user}
        except serializers.ValidationError as e:
            return {'message': e.detail}
        except Exception as e:
            return {'message': str(e)}

    def login(self, request, username, password):
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                serialized_user = UserSerializer(user).data
                return {'message': 'Пользователь успешно авторизован', 'data': serialized_user}
            else:
                raise Exception('Неправильный логин или пароль')
        except Exception as e:
            return {'message': str(e)}

    def logout(self, request):
        try:
            logout(request)
            return {'message': 'Успешный выход из аккаунта'}
        except Exception as e:
            return {'message': str(e)}

