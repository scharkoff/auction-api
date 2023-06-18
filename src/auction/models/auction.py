from django.contrib.auth.models import User
from django.db import models

class Auction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
