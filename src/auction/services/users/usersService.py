from django.contrib.auth.models import User
from auction.serializers.user import UserSerializer
from rest_framework import serializers
from .usersServiceInterface import IUsersService
from django.core.exceptions import ObjectDoesNotExist

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
            serializer = UserSerializer(data={'username': username, 'password': password, 'email': email})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            serializedUser = UserSerializer(user).data

            return {'message': 'Пользователь успешно создан', 'data': serializedUser}
        except serializers.ValidationError as e:
             raise serializers.ValidationError(e.detail)
        except Exception as e:
            raise Exception(str(e))
        
    def update(self, userId, username, password, email):
        try:
            user = User.objects.get(id=userId)

            user.username = username
            user.set_password(password)
            user.email = email

            data = {'username': username, 'password': password, 'email': email}
            
            serializer = UserSerializer(instance=user, data=data, partial=True)
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
