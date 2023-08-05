from django.contrib.auth.models import AbstractUser
from django.db import models


from django.core.files import File
import os




class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    title = models.CharField(max_length=64)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255, null=True)
    image = models.URLField(null=True, blank=True)


    


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    message = models.TextField()
    listing = models.ManyToManyField(Listing, blank=True, related_name="comment")


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    listing =  models.ManyToManyField(Listing, blank=True, related_name="bid")


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watcher')
    listing =  models.ManyToManyField(Listing, blank=True, related_name="watchlist")


