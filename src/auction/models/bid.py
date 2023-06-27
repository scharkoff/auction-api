from django.db import models
from django.contrib.auth.models import User
from auction.models.lot import Lot

class Bid(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lot_id = models.ForeignKey(Lot, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        unique_together = ['owner_id', 'lot_id']