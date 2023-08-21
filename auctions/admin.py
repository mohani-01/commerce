from django.contrib import admin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "price", "active", "category", "time")

class CommentAdmin(admin.ModelAdmin):
    filter_horizontal = ("listing",) 
    list_display = ("user", "message", "time")   

class BidAdmin(admin.ModelAdmin):
    filter_horizontal = ("listing",)
    list_display = ("user", "bid")

class WatchListAdmin(admin.ModelAdmin):
    filter_horizontal = ("listing",)
    list_display = ("user",)

class BidWinnerAdmin(admin.ModelAdmin):
    list_display = ("user", "winningbid", "listing")


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Bid, BidAdmin)   
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(BidWinner, BidWinnerAdmin)
