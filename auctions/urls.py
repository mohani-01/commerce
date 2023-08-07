from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lists/<int:list_id>", views.lists, name="lists"),
    path("newlist/<int:user_id>", views.newlist, name="newlist"),
    path("comment/<int:list_id>", views.comment, name="comment"),
    path("bid/<int:list_id>", views.bid, name="bid"),
    path("category", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
