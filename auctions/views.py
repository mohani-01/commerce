from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, WatchList
from .forms import NewList


def index(request):
    lists = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "lists": lists
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login")
def lists(request, list_id):
    lists = Listing.objects.get(pk=list_id)
    comments = lists.comment.all()


    return render(request, 'auctions/lists.html', {
        "lists": lists,
        "comments": comments
    })



@login_required(login_url="/login")
def newlist(request, user_id):
    if request.method == "POST":
        form = NewList(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]
            # for i in range(2):
            #     print(title,type(title), description, price, type(price), category, )
            # get user 
            user = User(pk=user_id)
            listing = Listing(user=user, title=title, description=description, price=price, category=category, image=image)
            listing.save()
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, 'auctions/newlist.html', {
            "form": form
            })
        return HttpResponse("Working on it")
    else:
        return render(request, 'auctions/newlist.html', {
            "form": NewList()
        })