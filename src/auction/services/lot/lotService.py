from auction.serializers.lot import LotSerializer
from auction.serializers.bid import BidSerializer
from rest_framework import serializers
from auction.models.lot import Lot
from auction.models.bid import Bid
from django.db.models import Max
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .lotServiceInterface import ILotService

class LotService(ILotService):
    def __init__(self) -> None:
        pass

    def finish(self, lotId):
        try:
            with transaction.atomic():
                maxBid = Bid.objects.filter(lot_id=int(lotId)).aggregate(Max('price'))
                maxPrice = maxBid['price__max']

                if maxPrice is not None:
                    winningBid = Bid.objects.filter(lot_id=int(lotId), price=maxPrice).first()

                    if winningBid is not None:
                        winningLot = Lot.objects.get(id=int(lotId))
                        winningLot.winner_id_id = winningBid.owner_id_id
                        winningLot.save()

                        serializer = LotSerializer(instance=winningLot, data={"winner_id": winningBid.owner_id_id}, partial=True)
                        serializer.is_valid(raise_exception=True)

                        serializedLot = serializer.data
                        print(serializedLot)
                        return  {'message': 'Победитель успешно определен', 'data': serializedLot}
                    else:
                        raise Exception('Не удалось найти победителя ставки')
                else:
                    raise Exception('Нет ставок для данного лота')
        except Bid.DoesNotExist:
            raise Exception('Нет ставок для данного лота')
        except Exception as e:
            print(e)
            raise Exception(str(e))
        
    def checkStatus(self, lotId):
        try:
            self.finish(lotId)

            with transaction.atomic():
                lot = Lot.objects.get(id=lotId)

            
                if (lot.end_time <= timezone.now()):
                    lot.is_closed = True
                    lot.save()
              
                serializedLot = LotSerializer(lot).data

                return {'message': 'Обновленная информация о лоте', 'data': serializedLot}
        except Lot.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый лот не найден или не существует')
        except Exception as e:
            raise Exception(str(e))

    
    def getAll(self, ownerId, auctionId):
        try:
            lots = Lot.objects.all()

            if ownerId is not None and ownerId != '0':
                lots = lots.filter(owner_id=ownerId)

            if auctionId is not None and auctionId != '0':
                lots = lots.filter(auction_id=auctionId)

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
                startTime = self.convertMillisecondsToDatetime(startTime)
                endTime = self.convertMillisecondsToDatetime(endTime)

                dataToValidate = {
                    "title": title, 
                    "description": description, 
                    "owner_id": ownerId, 
                    "auction_id": auctionId, 
                    "start_time": startTime, 
                    "end_time": endTime,
                    "image": image
                }

                serializer = LotSerializer(data=dataToValidate)
                
                serializer.is_valid(raise_exception=True)
                
                lot = serializer.save()

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

                dataToUpdate = {}

                if startTime is not None:
                    startTime = self.convertMillisecondsToDatetime(startTime)
                    dataToUpdate.update({"start_time": startTime})
                    lot.start_time = startTime
                
                if endTime is not None:
                    endTime = self.convertMillisecondsToDatetime(endTime)
                    dataToUpdate.update({"end_time": endTime})
                    lot.end_time = endTime

                if title is not None:
                    dataToUpdate.update({"title": title})
                    lot.title = title

                if description is not None:
                    dataToUpdate.update({"description": description})
                    lot.description = description

                if image is not None:
                    dataToUpdate.update({"image": image})
                    lot.image = image

                serializer = LotSerializer(instance=lot, data=dataToUpdate, partial=True)

                serializer.is_valid(raise_exception=True)

                lot = serializer.save()

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

            return {'data': {'id': int(lotId)}, 'message': 'Лот успешно удален'}
        except Lot.DoesNotExist:
            raise ObjectDoesNotExist('Запрашиваемый лот не найден или не существует')
        except Exception as e:
            raise Exception(str(e))
      
    def convertMillisecondsToDatetime(self, milliseconds):
        return datetime.fromtimestamp(int(milliseconds) / 1000)