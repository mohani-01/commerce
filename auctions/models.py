from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    """
    id = automatic
    title = 
    description = 
    starting bid = 
    image_url
    user = Object
                < User: User.id, User.username, User.password >
    comment = Object < Comment: Comment.id, Comment.message, Comment.commenter = Object
                                                                                        < User: User.id, User.username, User.password >
    """
    pass

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
    """
    id = automatic
    message = 
    user_id = Object 
                    < User: User.id, User.username, User.password >  
    Listing = Object 
                    < Listing: ... >
    """
    pass