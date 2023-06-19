from auction.serializers.lot import LotSerializer
from rest_framework import serializers
from auction.models.lot import Lot
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

class LotService():
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
        
    def create(self, owner, auction, startTime, endTime, title, description, image):
        try:
            startTime = self.convertMillisecondsToDatetime(startTime)
            endTime = self.convertMillisecondsToDatetime(endTime)

            lot = Lot(
                auction=auction,
                owner=owner,
                start_time=startTime,
                end_time=endTime,
                title=title,
                description=description,
                image=image
            )

            serializedLot = LotSerializer(lot).data

            lot.save()

            return {'message': 'Лот успешно создан', 'data': serializedLot}
        except serializers.ValidationError as e:
             raise serializers.ValidationError(e.detail)
        except Exception as e:
            raise Exception(str(e))
        
    def update(self, lotId, startTime, endTime, title, description, image):
        try:
            lot = Lot.objects.get(id=lotId)

            startTime = self.convertMillisecondsToDatetime(startTime)
            endTime = self.convertMillisecondsToDatetime(endTime)

            lot.start_time = startTime
            lot.end_time = endTime
            lot.title = title
            lot.description = description
            lot.image = image

            serializedLot = LotSerializer(lot).data

            lot.save()

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