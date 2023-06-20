from rest_framework import serializers
from auction.models.bid import Bid

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'owner_id', 'lot_id', 'price']
