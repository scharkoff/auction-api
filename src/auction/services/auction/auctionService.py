from auction.models.auction import Auction
from auction.serializers.auction import AuctionSerializer
from .auctionServiceInterface import IAuctionService
from datetime import datetime

class AuctionService(IAuctionService):
    def __init__(self) -> None:
        pass

    def create(self, title, startTime, endTime, owner):
        startTime = self.convertMillisecondsToDatetime(startTime)
        endTime = self.convertMillisecondsToDatetime(endTime)
    
        auction = Auction(title=title, start_time=startTime, end_time=endTime, owner=owner)
        auction.save()
        serializedAuction = AuctionSerializer(auction).data
        return {'message': 'Аукцион успешно создан', 'data': serializedAuction}

    def update(self, auctionId, title=None, startTime=None, endTime=None):
        try:
            startTime = self.convertMillisecondsToDatetime(startTime)
            endTime = self.convertMillisecondsToDatetime(endTime)

            auction = Auction.objects.get(id=auctionId)
            if title:
                auction.title = title
            if startTime:
                auction.start_time = startTime
            if endTime:
                auction.end_time = endTime
            auction.save()
            serializedAuction = AuctionSerializer(auction).data
            return {'message': 'Аукцион успешно изменен', 'data': serializedAuction}
        except Auction.DoesNotExist:
            raise Exception('Запрашиваемый аукцион не найден или не существует')

    def close(self, auctionId):
        try:
            auction = Auction.objects.get(id=auctionId)
            auction.is_closed = True
            auction.save()
            serializedAuction = AuctionSerializer(auction).data
            return {'message': 'Аукцион успешно закрыт', 'data': serializedAuction}
        except Auction.DoesNotExist:
            raise Exception('Запрашиваемый аукцион не найден или не существует')

    def getById(self, auctionId):
        try:
            auction = Auction.objects.get(id=auctionId)
            serializedAuction = AuctionSerializer(auction).data
            return {'message': 'Аукцион успешно найден', 'data': serializedAuction}
        except Auction.DoesNotExist:
            raise Exception('Запрашиваемый аукцион не найден или не существует')

    def search(self, query):
        auctions = Auction.objects.filter(title__icontains=query)
        serializedAuctions = AuctionSerializer(auctions, many=True).data
        return {'message': 'Аукцион(ы) успешно найден(ы)', 'data': serializedAuctions}

    def convertMillisecondsToDatetime(self, milliseconds):
        return datetime.fromtimestamp(int(milliseconds) / 1000)