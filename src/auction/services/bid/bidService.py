from django.core.exceptions import ObjectDoesNotExist
from auction.models.bid import Bid
from auction.serializers.bid import BidSerializer
from rest_framework import serializers
from django.db import transaction
from .bidServiceInterface import IBidService

class BidService(IBidService):
    def getAll(self, owner_id):
        try:
          
            if owner_id is not None:
                bids = Bid.objects.filter(owner_id=owner_id)
            else:
                bids = Bid.objects.all()

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
