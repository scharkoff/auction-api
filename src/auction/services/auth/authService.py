from django.contrib.auth import authenticate, login, logout
from auction.serializers.user import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .authServiceInterface import IAuthService
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction

class AuthService(IAuthService):

    def __init__(self) -> None:
        super().__init__()

    def register(self, username, password, email):
        try:
            with transaction.atomic():
                serializer = UserSerializer(data={'username': username, 'password': password, 'email': email})

                serializer.is_valid(raise_exception=True)

                user = serializer.save(password=password)

                serializedUser = UserSerializer(user).data

                return {'message': 'Пользователь успешно зарегистрирован', 'data': serializedUser}
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        except Exception as e:
            raise Exception(str(e))

    def login(self, request, username, password):
        try:
            with transaction.atomic():
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
        
    def auth(self, userId):
        try:
            user = User.objects.get(id=userId)

            serializedUser = UserSerializer(user).data

            return {'message': 'Пользователь успешно найден', 'data': serializedUser}
        except User.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый пользователь не найден или не существует')
        except Exception as e:
            raise Exception(str(e))
        

    def logout(self, request):
        try:
            with transaction.atomic():
                logout(request)
                return {'message': 'Успешный выход из аккаунта'}
        except Exception as e:
            raise Exception(str(e))

