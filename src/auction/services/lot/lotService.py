from auction.serializers.lot import LotSerializer
from rest_framework import serializers
from auction.models.lot import Lot
from auction.models.auction import Auction
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .lotServiceInterface import ILotService

class LotService(ILotService):
    def __init__(self) -> None:
        pass
    
    def getAll(self):
        try:
            lots = Lot.objects.all()

            serializedLots = LotSerializer(lots, many=True).data

            return {'message': 'Лоты успешно найдены', 'data': serializedLots}
        except Exception as e:
            raise Exception(str(e))
        
    def getById(self, lotId):
        try:
            lot = Lot.objects.get(id=lotId)

            serializedLot = LotSerializer(lot).data

            return {'message': 'Лот успешно найден', 'data': serializedLot}
        except Lot.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый лот не найден или не существует')
        except Exception as e:
            raise Exception(str(e))
        
    def create(self, ownerId, auctionId, startTime, endTime, title, description, image):
        try:
            with transaction.atomic():
                owner = get_object_or_404(User, id=ownerId)
                auction = get_object_or_404(Auction, id=auctionId)

                startTime = self.convertMillisecondsToDatetime(startTime)
                endTime = self.convertMillisecondsToDatetime(endTime)

                lot = Lot(
                    auction_id=auction,
                    owner_id=owner,
                    start_time=startTime,
                    end_time=endTime,
                    title=title,
                    description=description,
                    image=image
                )

                lot.save()

                LotSerializer(data={"owner_id": ownerId, "auction_id": auctionId, "start_time": startTime, "end_time": endTime}).is_valid(raise_exception=True)
                serializedLot = LotSerializer(lot).data

                return {'message': 'Лот успешно создан', 'data': serializedLot}
        except serializers.ValidationError as e:
             raise serializers.ValidationError(e.detail)
        except Exception as e:
            raise Exception(str(e))
        
    def update(self, lotId, startTime, endTime, title, description, image):
        try:
            with transaction.atomic():
                lot = Lot.objects.get(id=lotId)

                startTime = self.convertMillisecondsToDatetime(startTime)
                endTime = self.convertMillisecondsToDatetime(endTime)

                lot.start_time = startTime
                lot.end_time = endTime
                lot.title = title
                lot.description = description
                lot.image = image

                lot.save()

                LotSerializer(data={"start_time": startTime, "end_time": endTime}).is_valid(raise_exception=True)
                serializedLot = LotSerializer(lot).data

                return {'message': 'Данные лота успешно изменены', 'data': serializedLot}
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        except Lot.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый лот не найден или не существует')
        except Exception as e:
            raise Exception(str(e))
        
    def delete(self, lotId):
        try:
            lot = Lot.objects.get(id=lotId)

            lot.delete()

            return {'message': 'Лот успешно удален'}
        except Lot.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый лот не найден или не существует')
        except Exception as e:
            raise Exception(str(e))
      
    def convertMillisecondsToDatetime(self, milliseconds):
        return datetime.fromtimestamp(int(milliseconds) / 1000)