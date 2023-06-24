from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, serializers
from auction.services.lot.lotService import LotService
from django.core.exceptions import ObjectDoesNotExist
from .lotControllerInterface import ILotController
from auction.models.lot import Lot

class LotController(ILotController):
    lotService = LotService()

    @staticmethod
    @api_view(['POST'])
    def create(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            ownerId = request.user.id
            auctionId = request.data.get('auctionId')
            startTime = request.data.get('startTime')
            endTime = request.data.get('endTime')
            title = request.data.get('title')
            description = request.data.get('description')
            image = request.data.get('image')

            try:
                response = LotController.lotService.create(ownerId, auctionId, startTime, endTime, title, description, image)
                return Response(response, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response({'message': "Ошибка валидации", 'data': e.detail}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['GET'])
    def getAll(request):
        try:

            ownerId = request.query_params.get('owner_id', None)
            auctionId = request.query_params.get('auction_id', None)

            try:
                response = LotController.lotService.getAll(ownerId, auctionId)
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['GET'])
    def getById(request):
        try:
            lotId = request.query_params.get('id', None)

            if not lotId:
                raise Exception("Неправильный формат запроса")
            
            try:
                response = LotController.lotService.getById(lotId)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
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
            
            lotId = request.data.get('lotId')

            lot = Lot.objects.get(id=lotId)
            if lot.owner_id != request.user.id and not request.user.is_superuser:
                return Response({'message': 'Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)
            
            startTime = request.data.get('startTime', None)
            endTime = request.data.get('endTime', None)
            title = request.data.get('title', None)
            description = request.data.get('description', None)
            image = request.data.get('image', None)

            if (not startTime and not endTime and not title and not description and not image):
                raise Exception("Хотя бы одно поле должно быть заполнено") 

            try:
                response = LotController.lotService.update(lotId, startTime, endTime, title, description, image)
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
    @api_view(['DELETE'])
    def delete(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            lotId = request.data.get('lotId')

            if not lotId:
                raise Exception("Неправильный формат запроса") 
            
            lot = Lot.objects.get(id=lotId)
            if lot.owner_id != request.user.id and not request.user.is_superuser:
                return Response({'message': 'Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)

            try:
                response = LotController.lotService.delete(lotId)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
