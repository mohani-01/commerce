from django.db.models import Max


def get_bid(lists):
    price = lists.bid.aggregate(Max('bid'))['bid__max']
    bider = lists.bid.filter(bid=price, listing=lists).first()
    length = len(lists.bid.all())

    if price:
        price = float(f"{price:10.2f}") 

        return (price, bider.user, length)
    return (lists.price, lists.user, length)

    
def is_watchlist(lists, user):
    watchlist = lists.watchlist.filter(user=user)
    if watchlist:
        return True
    return False



# Get the winner
def get_winner(lists):
    data = lists.bid.order_by('-bid').first()
    if data:
        return (data.listing.get(), data.user, data.bid)
    return None, None, None