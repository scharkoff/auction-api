from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from auction.models.lot import Lot
from rest_framework import status, serializers
from auction.models.auction import Auction
from auction.services.lot.lotService import LotService
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

class LotController:
    lotService = LotService()

    @staticmethod
    @api_view(['POST'])
    def create(request):
        try:
            if not request.user.is_authenticated or not request.user.is_active:
                return Response({'message': 'Ошибка авторизации'}, status=status.HTTP_401_UNAUTHORIZED)
            
            ownerId = request.user.id
            owner = get_object_or_404(User, id=ownerId)
            auctionId = request.data.get('auctionId')
            auction = get_object_or_404(Auction, id=auctionId)
            startTime = request.data.get('startTime')
            endTime = request.data.get('endTime')
            title = request.data.get('title')
            description = request.data.get('description')
            image = request.data.get('image')

            try:
                response = LotController.lotService.create(owner, auction, startTime, endTime, title, description, image)
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
            
            try:
                response = LotController.lotService.getAll()
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['GET'])
    def getById(request):
        try:
            lotId = request.data.get('lotId')
            
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
            startTime = request.data.get('startTime')
            endTime = request.data.get('endTime')
            title = request.data.get('title')
            description = request.data.get('description')
            image = request.data.get('image')

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

            try:
                response = LotController.lotService.delete(lotId)
                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
