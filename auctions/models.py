from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
   
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    title = models.CharField(max_length=64)
    description = models.TextField()



class Bid(models.Model):
    """
    id = automatic
    update_bid = $
    auction = Object 
                    < Listing: Listing.id, Listing.title, Listing.description, 
                        Listing.starting_bid, Listing.image_url, Listing.user = Object
                                                                                    < User: User.id, User.username, User.password >
                        Listing.comment = Object 
                                                < Comment: Comment.id, Comment.message, Comment.commenter = Object
                                                                                                                < User: User.id, User.username, User.password >
    """
    pass

class Comments(models.Model):
    user = models.ForeignKey(User, default=3, on_delete=models.CASCADE, related_name='commenter')
    message = models.TextField(default="HI")
    listing = models.ManyToManyField(Listing, blank=True, related_name="comment")