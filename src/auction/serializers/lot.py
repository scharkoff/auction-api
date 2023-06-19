from rest_framework import serializers
from datetime import datetime
from auction.models.lot import Lot

class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'owner_id', 'auction_id', 'image']

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("Время начала должно быть меньше, чем время окончания аукциона")

        return data
