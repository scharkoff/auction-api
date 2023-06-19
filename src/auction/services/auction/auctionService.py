from auction.models.auction import Auction
from auction.serializers.auction import AuctionSerializer
from .auctionServiceInterface import IAuctionService
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class AuctionService(IAuctionService):
    def __init__(self) -> None:
        pass

    def create(self, title, startTime, endTime, ownerId):
        try:
            with transaction.atomic():
                owner = get_object_or_404(User, id=ownerId)

                startTime = self.convertMillisecondsToDatetime(startTime)
                endTime = self.convertMillisecondsToDatetime(endTime)
            
                auction = Auction(title=title, start_time=startTime, end_time=endTime, owner_id=owner)

                auction.save()
                
                AuctionSerializer(data={"owner_id": ownerId,"start_time": startTime, "end_time": endTime}).is_valid(raise_exception=True)
                serializedAuction = AuctionSerializer(auction).data

                return {'message': 'Аукцион успешно создан', 'data': serializedAuction}
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        except Exception as e:
            raise Exception(str(e))

    def update(self, auctionId, title=None, startTime=None, endTime=None):
        try:
            with transaction.atomic():
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

                AuctionSerializer(data={"start_time": startTime, "end_time": endTime}).is_valid(raise_exception=True)
                serializedAuction = AuctionSerializer(auction).data

                return {'message': 'Аукцион успешно изменен', 'data': serializedAuction}
        except serializers.ValidationError as e:
           raise serializers.ValidationError(e.detail)
        except Auction.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый аукцион не найден или не существует')
        except Exception as e:
            raise Exception(str(e))

    def close(self, auctionId):
        try:
            with transaction.atomic():
                auction = Auction.objects.get(id=auctionId)
                auction.is_closed = True

                auction.save()

                serializedAuction = AuctionSerializer(auction).data

                return {'message': 'Аукцион успешно закрыт', 'data': serializedAuction}
        except Auction.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый аукцион не найден или не существует')
        except Exception as e:
            raise Exception(str(e))

    def getById(self, auctionId):
        try:
            auction = Auction.objects.get(id=auctionId)
            serializedAuction = AuctionSerializer(auction).data

            return {'message': 'Аукцион успешно найден', 'data': serializedAuction}
        except Auction.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый аукцион не найден или не существует')
        except Exception as e:
            raise Exception(str(e))
        
    def getAll(self):
        try:
            auctions = Auction.objects.all()
            serializedAuctions = AuctionSerializer(auctions, many=True).data

            return {'message': 'Аукцион(ы) успешно найден(ы)', 'data': serializedAuctions}
        except Auction.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый аукцион не найден или не существует')
        except Exception as e:
            raise Exception(str(e))

    def search(self, query):
        try:
            auctions = Auction.objects.filter(title__icontains=query)
            serializedAuctions = AuctionSerializer(auctions, many=True).data

            return {'message': 'Аукцион(ы) успешно найден(ы)', 'data': serializedAuctions}
        except Auction.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый аукцион не найден или не существует')
        except Exception as e:
            raise Exception(str(e))
        
    def delete(self, auctionId):
        try:
            auction = Auction.objects.get(id=auctionId)

            auction.delete()

            return {'message': 'Аукцион успешно удален'}
        except Auction.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый аукцион не найден или не существует')
        except Exception as e:
            raise Exception(str(e))

    def convertMillisecondsToDatetime(self, milliseconds):
        return datetime.fromtimestamp(int(milliseconds) / 1000)