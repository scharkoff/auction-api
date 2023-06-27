from rest_framework import serializers
from django.contrib.auth.models import User
from auction.models.bid import Bid
from auction.models.lot import Lot
from auction.serializers.user import UserSerializer
from auction.serializers.lot import LotSerializer

class BidSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    lot = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ['id', 'owner_id', 'owner', 'lot_id', 'lot', 'price']


    def get_lot(self, obj):
        lotId = obj.lot_id_id

        try:
            lot = Lot.objects.get(id=lotId)

            serializedAuction = LotSerializer(lot).data

            return serializedAuction
        except Lot.DoesNotExist:
            return None
        
    def get_owner(self, obj):
        owner_id = obj.owner_id_id

        try:
            user = User.objects.get(id=owner_id)

            serializedUser = UserSerializer(user).data

            return serializedUser
        except User.DoesNotExist:
            return None
