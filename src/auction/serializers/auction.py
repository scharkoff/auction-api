from rest_framework import serializers
from auction.models.auction import Auction

class AuctionSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ')

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'created', 'is_closed', 'owner_id']

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        title = data.get('title')
        description = data.get('description')

        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("Время начала должно быть меньше, чем время окончания аукциона") 
               
        if title and len(title) < 3:
            raise serializers.ValidationError("Название должно иметь не менее 3-х символов")
        
        if description and len(description) < 10:
            raise serializers.ValidationError("Описание должно иметь не менее 10-ти символов")
        
        return data
