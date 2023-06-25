from rest_framework import serializers
from auction.models.auction import Auction
from django.contrib.auth.models import User
from auction.serializers.user import UserSerializer

class AuctionSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'created', 'is_closed', 'owner_id', 'owner']

    def get_owner(self, obj):
        owner_id = obj.owner_id_id

        try:
            user = User.objects.get(id=owner_id)

            serializedUser = UserSerializer(user).data

            return serializedUser
        except User.DoesNotExist:
            return None

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
