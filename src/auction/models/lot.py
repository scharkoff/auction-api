from django.db import models
from auction.models.auction import Auction

class Lot(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='lots')
    title = models.CharField(max_length=255)
    description = models.TextField()