from django.core.exceptions import ObjectDoesNotExist
from auction.models.bid import Bid
from auction.models.lot import Lot
from auction.serializers.bid import BidSerializer
from auction.serializers.lot import LotSerializer
from rest_framework import serializers
from django.db import transaction
from .bidServiceInterface import IBidService

class BidService(IBidService):
    def getUserBidByLotId(self, ownerId, lotId): 
        try:

            print(ownerId)
             
            bid = Bid.objects.get(owner_id=ownerId, lot_id=lotId)

            serializedBid = BidSerializer(bid).data

            return {'message': 'Ставка успешно найдена', 'data': serializedBid}
        except Bid.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемая ставка не найдена или не существует')
        except Exception as e:
            raise Exception(str(e))
        
    def getAll(self, lotId):
        try:
          
            bids = Bid.objects.all()

            if lotId is not None and lotId != '0':
                bids = Bid.objects.filter(lot_id=lotId)

            serializedBids = BidSerializer(bids, many=True).data

            return {'message': 'Ставки успешно найдены', 'data': serializedBids}
        except Exception as e:
            raise Exception(str(e))
        
    def getById(self, bidId):
        try:
            bid = Bid.objects.get(id=bidId)

            serializedBid = BidSerializer(bid).data

            return {'message': 'Ставка успешно найдена', 'data': serializedBid}
        except Bid.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемая ставка не найдена или не существует')
        except Exception as e:
            raise Exception(str(e))
        
    def create(self, ownerId, lotId, price):
        try:
            with transaction.atomic():
                dataToValidate = {
                    "owner_id": ownerId,
                    "lot_id": lotId,
                    "price": price
                }

                serializer = BidSerializer(data=dataToValidate)

                serializer.is_valid(raise_exception=True)

                bid = serializer.save()

                serializedBid = BidSerializer(bid).data

                return {'message': 'Ставка успешно создана', 'data': serializedBid}
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        except Exception as e:
            raise Exception(str(e))
        
    def update(self, bidId, price):
        try:
            with transaction.atomic():
              bid = Bid.objects.get(id=bidId)
              bid.price = price
              serializer = BidSerializer(instance=bid, data={"price": price}, partial=True)
              serializer.is_valid(raise_exception=True)

              lot = Lot.objects.get(id=bid.lot_id_id)
              lotSerializer = LotSerializer(instance=lot, data={"price": price}, partial=True)
              lotSerializer.is_valid(raise_exception=True)
              lot.price = price
              lot.save()

              bid = serializer.save()

              serializedBid = BidSerializer(bid).data

              return {'message': 'Данные ставки успешно изменены', 'data': serializedBid}
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        except Bid.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемая ставка не найдена или не существует')
        except Exception as e:
            raise Exception(str(e))
        
    def delete(self, bidId):
        try:
            bid = Bid.objects.get(id=bidId)
            bid.delete()
            return {'message': 'Ставка успешно удалена'}
        except Bid.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемая ставка не найдена или не существует')
        except Exception as e:
            raise Exception(str(e))
