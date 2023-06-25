from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Auction(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default=None, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(default=timezone.now)
    is_closed = models.BooleanField(default=False)
