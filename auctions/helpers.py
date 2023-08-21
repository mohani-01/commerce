from django.db.models import Max


def get_bid(lists):
    # Get the maximum bid for the list
    price = lists.bid.aggregate(Max('bid'))['bid__max']

    # get all the data about the bider
    bider = lists.bid.filter(bid=price, listing=lists).first()

    # get how many time users bid on this item
    length = len(lists.bid.all())

    # return the price, user who bid on it and how many time the list is bade on
    if price:
        price = float(f"{price:10.2f}") 
        return (price, bider.user, length)

    # else return the first price with the user who post it
    return (lists.price, lists.user, length)

    
def is_watchlist(lists, user):
    # check if the list is already in the user watchlist
    watchlist = lists.watchlist.filter(user=user)
    if watchlist:
        return True
    return False



# Get the winner
def get_winner(lists):
    
    # get the highest bid 
    data = lists.bid.order_by('-bid').first()
    if data:
        return (data.listing.get(), data.user, data.bid)
    return None, None, None