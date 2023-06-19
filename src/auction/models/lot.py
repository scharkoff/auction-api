from django.db import models
from django.contrib.auth.models import User
from auction.models.auction import Auction

class Lot(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default=None, null=True)
    description = models.TextField(default=None, null=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.URLField(default=None, null=True)