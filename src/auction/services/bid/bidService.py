from django.core.exceptions import ObjectDoesNotExist
from auction.models.bid import Bid
from auction.serializers.bid import BidSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from auction.models.lot import Lot
from django.shortcuts import get_object_or_404
from django.db import transaction
from .bidServiceInterface import IBidService

class BidService(IBidService):
    def getAll(self):
        try:
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
              owner = get_object_or_404(User, id=ownerId)
              lot = get_object_or_404(Lot, id=lotId)

              bid = Bid(owner_id=owner, lot_id=lot, price=price)

              bid.save()

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

              bid.save()

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
