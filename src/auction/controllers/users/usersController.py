from rest_framework import status, serializers
from rest_framework.response import Response
from auction.services.users.usersService import UserService
from .usersControllerInterface import IUsersController
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist

class UsersController(IUsersController):
    usersSerivce = UserService()

    def __init__(self) -> None:
        pass
    
    @staticmethod
    @api_view(['GET'])
    def getAll(request):
        try:
          if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
          
          try:
              response = UsersController.usersSerivce.getAll()
              return Response(response, status=status.HTTP_200_OK)
          except Exception as e:
              return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    @api_view(['GET'])
    def getById(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            userId = request.data.get('userId')

            if not userId:
                raise Exception("Неправильный формат запроса") 
           
            try:
                response = UsersController.usersSerivce.getById(userId)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['POST'])
    def create(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')

            if not username or not password or not email:
                raise Exception("Неправильный формат запроса") 

            try:  
                response = UsersController.usersSerivce.create(username, password, email)
                return Response(response, status=status.HTTP_200_OK)
            except serializers.ValidationError as e:
                return Response({'message': "Ошибка валидации", 'data': e}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
    @staticmethod
    @api_view(['PATCH'])
    def update(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            userId = request.data.get('userId')
            username = request.data.get('username', None)
            password = request.data.get('password', None)
            email = request.data.get('email', None)

            if not userId:
                raise Exception("Неправильный формат запроса") 

            try:  
                response = UsersController.usersSerivce.update(userId, username, password, email)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except serializers.ValidationError as e:
                return Response({'message': "Ошибка валидации", 'data': e}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['DELETE'])
    def delete(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            userId = request.data.get('userId')

            if not userId:
                raise Exception("Неправильный формат запроса") 

            try:
                response = UsersController.usersSerivce.delete(userId)
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)