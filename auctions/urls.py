from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('newlisting/<int:user_id>', views.newlisting, name="newlisting"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
