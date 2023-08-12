from django.db.models import Max


def get_bid(lists):
    price = lists.bid.aggregate(Max('bid'))['bid__max']
    length = len(lists.bid.all())

    if price:
        return (price, length)
    return (lists.price, length)

# def get_category(get_category, Category):
#     category = Category.objects.get(category=get_category)
#     if category:
#         return category
    
def is_watchlist(lists, user):
    watchlist = lists.watchlist.filter(user=user)
    if watchlist:
        return True
    return False




def get_winner(lists):
    data = lists.bid.order_by('-bid').first()
    if data:
        return (data.listing.get(), data.user, data.bid)
    return None, None, None