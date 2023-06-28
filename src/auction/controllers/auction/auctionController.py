from rest_framework import status, serializers
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from auction.services.auction.auctionService import AuctionService
from .auctionControllerInterface import IAuctionController
from auction.models.auction import Auction


class AuctionController(IAuctionController):
    auctionService = AuctionService()

    def __init__(self) -> None:
       pass

    @staticmethod
    @api_view(['POST'])
    def create(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
             
            ownerId = request.user.id
            title = request.data.get('title')
            description = request.data.get('description')
            startTime = request.data.get('startTime')
            endTime = request.data.get('endTime')

            if not ownerId or not title or not startTime or not endTime:
                raise Exception("Неправильный формат запроса")

            try:
                response = AuctionController.auctionService.create(title, description, startTime, endTime, ownerId)
                return Response(response, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response({'message': "Ошибка валидации", 'data': e.detail}, status=status.HTTP_400_BAD_REQUEST)
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
            
            auctionId = request.data.get('auctionId')

            auction = Auction.objects.get(id=auctionId)
            if auction.owner_id_id != request.user.id and not request.user.is_superuser:
                return Response({'message': 'Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)

            title = request.data.get('title', None)
            startTime = request.data.get('startTime', None)
            endTime = request.data.get('endTime', None)

            if not title and not startTime and not endTime:
                raise Exception("Хотя бы одно поле должно быть заполнено") 

            try:
                response = AuctionController.auctionService.update(auctionId, title, startTime, endTime)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except serializers.ValidationError as e:
                return Response({'message': "Ошибка валидации", 'data': e.detail}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['POST'])
    def close(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            auctionId = request.query_params.get('id', None)

            auction = Auction.objects.get(id=auctionId)
            if auction.owner_id_id != request.user.id and not request.user.is_superuser:
                return Response({'message': 'Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)

            if not auctionId:
                raise Exception("Неправильный формат запроса")

            try:
                response = AuctionController.auctionService.close(auctionId)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['GET'])
    def getById(request):
        try: 
            auctionId = request.query_params.get('id', None)

            if not auctionId:
                raise Exception("Неправильный формат запроса")

            try:
                response = AuctionController.auctionService.getById(auctionId)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['GET'])
    def getAll(request):
        try:

            ownerId = request.query_params.get('owner_id', None)
            sort = request.query_params.get('sort', '')
            filter = request.query_params.get('filter', '')

            try:
                response = AuctionController.auctionService.getAll(ownerId, sort, filter)
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(['GET'])
    def search(request):
        try:   
            query = request.query_params.get('query', '')

            try:
                response = AuctionController.auctionService.search(query)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
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
            
            auctionId = request.query_params.get('id', None)

            if not auctionId:
                raise Exception("Неправильный формат запроса")

            auction = Auction.objects.get(id=auctionId)
            if auction.owner_id_id != request.user.id and not request.user.is_superuser:
                return Response({'message': 'Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)

            try:
                response = AuctionController.auctionService.delete(auctionId)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)