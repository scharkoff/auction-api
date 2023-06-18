from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auction.services.users.usersService import UserService
from .usersControllerInterface import IUsersController

class UsersController(IUsersController):
    usersSerivce = UserService()

    def __init__(self) -> None:
        pass
    
    @staticmethod
    @api_view(['POST'])
    def getAll(request):
        try:
          response = UsersController.usersSerivce.getAll()

          return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    @api_view(['POST'])
    def getById(request):
        try:
            userId = request.data.get('userId')
           
            response = UsersController.usersSerivce.getById(userId)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['POST'])
    def create(request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')

            response = UsersController.usersSerivce.create(username, password, email)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['PATCH'])
    def update(request):
        try:
            userId = request.data.get('userId')
            username = request.data.get('username', None)
            password = request.data.get('password', None)
            email = request.data.get('email', None)

            response = UsersController.usersSerivce.update(userId, username, password, email)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['DELETE'])
    def delete(request):
        try:
            userId = request.data.get('userId')

            response = UsersController.usersSerivce.delete(userId)

            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)