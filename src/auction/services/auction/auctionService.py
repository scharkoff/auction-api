from auction.models.auction import Auction
from auction.serializers.auction import AuctionSerializer
from .auctionServiceInterface import IAuctionService
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db import transaction
from django.utils import timezone

class AuctionService(IAuctionService):
    def __init__(self) -> None:
        pass

    def create(self, title, description, startTime, endTime, ownerId):
        try:
            with transaction.atomic():
                startTime = self.convertMillisecondsToDatetime(startTime)
                endTime = self.convertMillisecondsToDatetime(endTime)
            
                dataToValidate = {
                    "owner_id": ownerId,
                    "title": title,
                    "start_time": startTime,
                    "end_time": endTime,
                    "description": description
                }

                serializer = AuctionSerializer(data=dataToValidate)
                
                serializer.is_valid(raise_exception=True)

                auction = serializer.save()

                serializedAuction = AuctionSerializer(auction).data

                return {'message': 'Аукцион успешно создан', 'data': serializedAuction}
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        except Exception as e:
            raise Exception(str(e))


    def update(self, auctionId, title, startTime, endTime):
        try:
            with transaction.atomic():
                auction = Auction.objects.get(id=auctionId)

                dataToUpdate = {}

                if startTime is not None:
                    startTime = self.convertMillisecondsToDatetime(startTime)
                    dataToUpdate.update({"start_time": startTime})
                    auction.start_time = startTime
                
                if endTime is not None:
                    endTime = self.convertMillisecondsToDatetime(endTime)
                    dataToUpdate.update({"end_time": endTime})
                    auction.end_time = endTime

                if title is not None:
                    dataToUpdate.update({"title": title})
                    auction.title = title

                serializer = AuctionSerializer(instance=auction, data=dataToUpdate, partial=True)

                serializer.is_valid(raise_exception=True)

                auction = serializer.save(auction_id=auction)

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
        
    def getAll(self, ownerId, sort, filter):
        try:

            auctions = Auction.objects.all()

            if ownerId is not None and ownerId != '0':
                auctions = auctions.filter(owner_id=ownerId)

            if sort == 'asc':
                auctions = auctions.order_by('created')
            elif sort == 'desc':
                auctions = auctions.order_by('-created') 

            if filter == 'closed':
                auctions = auctions.filter(is_closed=True) 
            elif filter == 'active':
                auctions = auctions.filter(is_closed=False) 
            
            serializedAuctions = AuctionSerializer(auctions, many=True).data

            return {'message': 'Аукцион(ы) успешно найден(ы)', 'data': serializedAuctions}
        except Auction.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый аукцион не найден или не существует')
        except Exception as e:
            raise Exception(str(e))

    def search(self, query):
        try:
            
            if (query == ''):
                 auctions = Auction.objects.all()
            else:
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