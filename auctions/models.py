from django.contrib.auth.models import AbstractUser
from django.db import models


from django.core.files import File
import os




class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64, default=None)

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    time = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="group") 
    image = models.URLField(null=True, blank=True)

def __str__(self):
    return f"{self.title} {self.description} {self.price}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    listing = models.ManyToManyField(Listing, blank=True, related_name="comment")


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    listing =  models.ManyToManyField(Listing, blank=True, related_name="bid")

    def __str__(self):
        return f"{self.bid}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watcher')
    listing =  models.ManyToManyField(Listing, blank=True, related_name="watchlist")


