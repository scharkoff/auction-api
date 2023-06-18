from django.contrib.auth import authenticate, login, logout
from auction.serializers.user import UserSerializer
from rest_framework import serializers
from .authServiceInterface import IAuthService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

class AuthService(IAuthService):
    def register(self, username, password, email):
        try:
            serializer = UserSerializer(data={'username': username, 'password': password, 'email': email})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            serializedUser = UserSerializer(user).data

            return {'message': 'Пользователь успешно зарегистрирован', 'data': serializedUser}
        except serializers.ValidationError as e:
            return Response({'message': e.detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            raise Exception(str(e))

    def login(self, request, username, password):
        try:
            user = authenticate(username=username, password=password)

            if user is None:
                raise AuthenticationFailed()

            login(request, user)
            serializedUser = UserSerializer(user).data

            return {'message': 'Пользователь успешно авторизован', 'data': serializedUser}
        except AuthenticationFailed as e:
            raise AuthenticationFailed('Неверные учетные данные пользователя')
        except Exception as e:
            raise Exception(str(e))

    def logout(self, request):
        try:
            logout(request)

            return {'message': 'Успешный выход из аккаунта'}
        except Exception as e:
            raise Exception(str(e))

