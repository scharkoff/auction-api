from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from auction.models.lot import Lot
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
            ownerId = request.user.id
            owner = get_object_or_404(User, id=ownerId)
            auctionId = request.data.get('auctionId')
            auction = get_object_or_404(Auction, id=auctionId)
            startTime = request.data.get('startTime')
            endTime = request.data.get('endTime')
            title = request.data.get('title')
            description = request.data.get('description')
            image = request.data.get('image')

            response = LotController.lotService.create(owner, auction, startTime, endTime, title, description, image)

            return Response(response, status=status.HTTP_201_CREATED)
        except Lot.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый лот не найден или не существует')
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    @api_view(['GET'])
    def getAll(request):
        try:
            response = LotController.lotService.getAll()

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    @api_view(['GET'])
    def getById(request):
        try:
            lotId = request.data.get('lotId')

            response = LotController.lotService.getById(lotId)

            return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    @api_view(['PATCH'])
    def update(request):
        try:
            lotId = request.data.get('lotId')
            startTime = request.data.get('startTime')
            endTime = request.data.get('endTime')
            title = request.data.get('title')
            description = request.data.get('description')
            image = request.data.get('image')

            response = LotController.lotService.update(lotId, startTime, endTime, title, description, image)

            return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    @api_view(['DELETE'])
    def delete(request):
        try:
            lotId = request.data.get('lotId')

            response = LotController.lotService.delete(lotId)

            return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
