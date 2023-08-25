from rest_framework import serializers
from auction.models.lot import Lot
from django.contrib.auth.models import User
from auction.models.auction import Auction
from auction.serializers.user import UserSerializer
from auction.serializers.auction import AuctionSerializer

class LotSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    auction = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()

    class Meta:
        model = Lot
        fields = ['id', 'title', 'description', 'price', 'start_time', 'end_time', 'is_closed', 'owner_id', 'owner', 'auction_id', 'auction', 'winner_id', 'winner', 'image']

    def get_winner(self, obj):
        winner_id = obj.winner_id_id

        try:
            winner = User.objects.get(id=winner_id)

            serializedUser = UserSerializer(winner).data

            return serializedUser
        except User.DoesNotExist:
            return None
        
    def get_auction(self, obj):
        auction_id = obj.auction_id_id

        try:
            auction = Auction.objects.get(id=auction_id)

            serializedAuction = AuctionSerializer(auction).data

            return serializedAuction
        except Auction.DoesNotExist:
            return None
        
    def get_owner(self, obj):
        owner_id = obj.owner_id_id

        try:
            user = User.objects.get(id=owner_id)

            serializedUser = UserSerializer(user).data

            return serializedUser
        except User.DoesNotExist:
            return None
        
    def validate(self, data):
        price = data.get('price')
        instance = self.instance
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        title = data.get('title')
        description = data.get('description')

        if instance and price is not None:
            current_price = instance.price

            if current_price > 0 and price < current_price:
                raise serializers.ValidationError("Ставка не может быть меньше текущей цены")

        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("Время начала должно быть меньше, чем время окончания")
            
        if title and len(title) < 3:
            raise serializers.ValidationError("Название должно иметь не менее 3-х символов")
        
        if description and len(description) < 10:
            raise serializers.ValidationError("Описание должно иметь не менее 10-ти символов")
        
        
        return data
