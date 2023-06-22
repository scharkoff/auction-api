from django.db import models
from django.contrib.auth.models import User
from auction.models.auction import Auction

class Lot(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lots_as_owner')
    winner_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, related_name='lots_as_winner')
    title = models.CharField(max_length=255)
    description = models.TextField(default=None, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.CharField(max_length=255, default=None, null=True)