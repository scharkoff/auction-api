from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from auction.services.auth.authService import AuthService
from .authControllerInterface import IAuthController
from rest_framework.exceptions import AuthenticationFailed

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

            if not username or not password or not email:
                raise Exception("Неправильный формат запроса")

            try:
                response = AuthController.authService.register(username, password, email)
                return Response(response, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response({'message': "Ошибка валидации", 'data': e.detail}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod  
    @api_view(['POST'])  
    def login(request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                raise Exception("Неправильный формат запроса")

            try:
                response = AuthController.authService.login(request, username, password)
                return Response(response, status=status.HTTP_200_OK)
            
            except AuthenticationFailed as e:
                return Response({'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod  
    @api_view(['GET'])  
    def auth(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                response = AuthController.authService.auth(request, request.user.id)
                return Response(response, status=status.HTTP_200_OK)
            
            except AuthenticationFailed as e:
                return Response({'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['GET'])
    def logout(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                response = AuthController.authService.logout(request)
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
