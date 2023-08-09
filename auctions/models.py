from django.contrib.auth.models import AbstractUser
from django.db import models


from django.core.files import File
import os




class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64, default=None)

    def __str__(self):
        return f"{self.category}"
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
    return f"Listing with Title: {self.title}, Description: {self.description}, Price: {self.price}, and Time created: {self.time}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    listing = models.ManyToManyField(Listing, blank=True, related_name="comment")

    def __str__(self):
        return f"User: {self.user}, Commented {self.message} This, at {self.time} on object called {self.listing.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    listing =  models.ManyToManyField(Listing, blank=True, related_name="bid")

    def __str__(self):
        return f"User: {self.user} bid with {self.bid} money on object {self.listing}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    listing =  models.ManyToManyField(Listing, blank=True, related_name="watchlist")

def __str__(self):
    return f"User: {self.user}, added object {self.listing.title} as a Watchlist"


class BidWinner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner")
    winningbid = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, blank=True, related_name="winner")