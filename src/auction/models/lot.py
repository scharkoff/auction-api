from django.db import models
from django.contrib.auth.models import User
from auction.models.auction import Auction

class Lot(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.CharField(max_length=255, default=None, null=True)