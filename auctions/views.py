from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import New
from .models import User, Listing, Comments

def index(request):
    listing = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "lists": listing,
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


def newlisting(request, user_id):
    if request.method == 'POST':
        form = New(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            user = User.objects.get(pk=user_id)
            print(user)
            # listing = Listing(title=)
            listing = Listing(user=user, title=title, description=description)
            listing.save()
            
            return HttpResponseRedirect(reverse("index"))    
    else:
        return render(request, 'auctions/newlisting.html', {
            "form": New(),
        })

def item(request, list_id):
    if request.method == "POST":
        message = request.POST["comment"]
        user = User.objects.get(pk=int(request.POST["commenter"]))
        lis = Listing.objects.get(pk=list_id)
        common = Comments(user=user, message=message)
        common.save()
        common.listing.add(lis)
        return HttpResponse("working on that")


    else:
        listing = Listing.objects.get(pk=list_id)
        comment = listing.comment.all()
        return render(request, 'auctions/list.html', {
            "list": listing,
            "comments": comment
        })