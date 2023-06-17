from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from auction.services.auction.auctionService import AuctionService
from .auctionControllerInterface import IAuctionController
from rest_framework.permissions import IsAuthenticated

class AuctionController(IAuctionController):
    auctionService = AuctionService()

    def __init__(self) -> None:
       pass

    @staticmethod
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    @api_view(['POST'])
    def create(request):
        try:
            title = request.data.get('title')
            startTime = request.data.get('startTime')
            endTime = request.data.get('endTime')

            response = AuctionController.auctionService.create(title, startTime, endTime)

            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @csrf_exempt  
    @permission_classes([IsAuthenticated])
    @api_view(['PATCH'])  
    def update(request):
        try:
            auctionId = request.data.get('auctionId')
            title = request.data.get('title')
            startTime = request.data.get('startTime')
            endTime = request.data.get('endTime')

            response = AuctionController.auctionService.update(auctionId, title, startTime, endTime)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
    @staticmethod
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    @api_view(['POST'])
    def close(request):
        try:
            auctionId = request.data.get('auctionId')

            response = AuctionController.auctionService.close(auctionId)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    @api_view(['POST'])
    def get(request):
        try:
            auctionId = request.data.get('auctionId')

            response = AuctionController.auctionService.get(auctionId)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    @csrf_exempt
    @api_view(['POST'])
    def search(request):
        try:
            query = request.data.get('query')

            response = AuctionController.auctionService.search(query)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)