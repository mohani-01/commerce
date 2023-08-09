from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lists/<int:list_id>", views.lists, name="lists"),
    path("newlist/", views.newlist, name="newlist"),
    path("comment/<int:list_id>", views.comment, name="comment"),
    path("bid/<int:list_id>", views.bid, name="bid"),
    path("watchlist/", views.see_watchlist, name="watchlist"),
    path("watchlist/<int:list_id>", views.watchlist, name="add&removewatchlist"),
    path("closebid/<int:list_id>", views.closebid, name="closebid"),
    path("closedlistings/", views,closedlistings, name="closedlistings"),
    path("category", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
