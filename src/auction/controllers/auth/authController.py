from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from auction.services.auth.authService import AuthService
from .authControllerInterface import IAuthController

class AuthController(IAuthController):
    authService = AuthService()

    def __init__(self) -> None:
       pass

    @staticmethod
    @api_view(['POST'])
    def register(request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')

            response = AuthController.authService.register(username, password, email)

            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod  
    @api_view(['POST'])  
    def login(request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            response = AuthController.authService.login(request, username, password)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
    @staticmethod
    @api_view(['POST'])
    def logout(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            response = AuthController.authService.logout(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
