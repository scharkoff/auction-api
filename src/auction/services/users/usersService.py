from django.contrib.auth.models import User
from auction.serializers.user import UserSerializer
from rest_framework import serializers
from .usersServiceInterface import IUsersService
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

class UserService(IUsersService):
    def __init__(self) -> None:
        pass
    
    def getAll(self):
        try:
            users = User.objects.all()
            serializedUsers = UserSerializer(users, many=True).data
            return {'message': 'Пользователи успешно найдены', 'data': serializedUsers}
        except Exception as e:
            raise Exception(str(e))
        
    def getById(self, userId):
        try:
            user = User.objects.get(id=userId)
            serializedUser = UserSerializer(user).data
            return {'message': 'Пользователь успешно найден', 'data': serializedUser}
        
        except User.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый пользователь не найден или не существует')
        except Exception as e:
            raise Exception(str(e))
        
    def create(self, username, password, email):
        try:
            with transaction.atomic():
                serializer = UserSerializer(data={'username': username, 'password': password, 'email': email})
                serializer.is_valid(raise_exception=True)

                user = serializer.save()

                serializedUser = UserSerializer(user).data

                return {'message': 'Пользователь успешно создан', 'data': serializedUser}
        except serializers.ValidationError as e:
             raise serializers.ValidationError(e.detail)
        except Exception as e:
            raise Exception(str(e))
        
    def update(self, userId, username, password, email, role):
        try:
            with transaction.atomic():
                user = User.objects.get(id=userId)

                dataToUpdate = {}

                if username is not None:
                    user.username = username
                    dataToUpdate.update({'username': username})

                if password is not None:
                    user.set_password(password)
                    dataToUpdate.update({'password': password})

                if email is not None:
                    user.email = email
                    dataToUpdate.update({'email': email})

                if role is not None:
                    user.role = role
                    dataToUpdate.update({'role': role})

                serializer = UserSerializer(instance=user, data=dataToUpdate, partial=True)

                serializer.is_valid(raise_exception=True)

                serializer.save()

                serializedUser = UserSerializer(user).data

                return {'message': 'Данные пользователя успешно изменены', 'data': serializedUser}
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        except User.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый пользователь не найден или не существует')
        except Exception as e:
            raise Exception(str(e))

    def delete(self, userId):
        try:
            user = User.objects.get(id=userId)
            user.delete()

            return {'message': 'Пользователь успешно удален'}
        except User.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый пользователь не найден или не существует')
        except Exception as e:
            raise Exception(str(e))
