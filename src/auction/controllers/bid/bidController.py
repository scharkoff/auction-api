from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from auction.models.bid import Bid
from auction.services.bid.bidService import BidService
from django.core.exceptions import ObjectDoesNotExist
from .bidContollerInterface import IBidController

class BidController(IBidController):
    bidService = BidService()

    @staticmethod
    @api_view(['POST'])
    def create(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            ownerId = request.user.id
            lotId = request.data.get('lotId')
            price = request.data.get('price')

            if not ownerId or not lotId or not price:
              raise Exception("Неправильный формат запроса")

            try:
                response = BidController.bidService.create(ownerId, lotId, price)
                return Response(response, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response({'message': 'Ошибка валидации', 'data': e.detail}, status=status.HTTP_400_BAD_REQUEST)
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
            owner_id = request.query_params.get('owner_id', None)

            try:
                response = BidController.bidService.getAll(owner_id)
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['GET'])
    def getById(request):
        try:
          
            bidId = request.query_params.get('id', None)

            if not bidId:
                raise Exception("Неправильный формат запроса")
            
            try:
                response = BidController.bidService.getById(bidId)
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
            
            bidId = request.data.get('bidId')

            bid = Bid.objects.get(id=bidId)
            if bid.owner_id != request.user.id and not request.user.is_superuser:
                return Response({'message': 'Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)
            
            price = request.data.get('price')

            if not bidId or not price:
                raise Exception("Неправильный формат запроса")
            
            try:
                response = BidController.bidService.update(bidId, price)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except serializers.ValidationError as e:
                return Response({'message': 'Ошибка валидации', 'data': e.detail}, status=status.HTTP_400_BAD_REQUEST)
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
            
            bidId = request.data.get('bidId')

            if not bidId:
                raise Exception("Неправильный формат запроса")

            bid = Bid.objects.get(id=bidId)
            if bid.owner_id != request.user.id and not request.user.is_superuser:
                return Response({'message': 'Недостаточно прав для выполнения операции'}, status=status.HTTP_403_FORBIDDEN)

            try:
                response = BidController.bidService.delete(bidId)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
