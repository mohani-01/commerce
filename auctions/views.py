from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *
from .helper import *

def index(request):
    lists = Listing.objects.filter(active=True)
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
    # GET the required listing page
    lists = Listing.objects.get(pk=list_id)

    # Error checking
    if not lists:
        ... 
    comments = lists.comment.all().order_by('-time')
    # comments = Comment.objects.all().order_by('-time').values()
    for comment in comments:
        print(comments)
    # Get the price or max bid and the number of bids for that object
    # price, length= get_bid(lists)

    # GET empty from
    # newbid = NewBid()

    # make the min value of price tag to max bid or price of the object
    # newbid.fields['price'].widget.attrs['min'] = price


    # This have to be modified
    return render(request, 'auctions/lists.html', {
        "lists": lists,
        "add_comment": NewComment(),
        "comments": comments,
        "bid": NewBid(),
    })



@login_required(login_url="/login")
def newlist(request, user_id):
    # Via POST
    if request.method == "POST":
        form = NewList(request.POST)

        # Check if the form is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            get_category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]
            
            # Get the user
            user = User(pk=user_id)
            
            # Return to newlisting page if the user doesn't exist
            # it is not possbile if db is malfunctioning or the user change 
            # the value of user.id in newlisting.html is changed
            if not user:
                ...
            
            # Insert category into Category's database
            category = Category(category=get_category)
            category.save()

            # Add all datas into listing database and save the data
            listing = Listing(user=user, title=title, description=description, price=price, category=category, image=image)
            listing.save()

            # Redirect the user into active listing page
            return HttpResponseRedirect(reverse("index"))

        # Return inserted form to the user
        else:
            return render(request, 'auctions/newlist.html', {
            "form": form
            })


    
    # Via GET
    else:
        return render(request, 'auctions/newlist.html', {
            "form": NewList()
        })


@login_required(login_url="/login")
def comment(request, list_id):
    if request.method == "POST":
        print(request.POST)
        form = NewComment(request.POST)
        if form.is_valid():
            # GET the user id from the form
            user_id = int(request.POST["commenter"])
            # get the user db
            user = User.objects.get(pk=user_id)


            # Check if user exist
            if not user:
                ...
            
            lists = Listing.objects.get(pk=list_id)
            # Check if list exist
            if not lists:
                ...
            # Get the comment
            message = form.cleaned_data["comment"]

            # insert data to db
            comment = Comment(user=user, message=message)
            comment.save()

            comment.listing.add(lists)

            print(comment)


        return HttpResponseRedirect(reverse("lists", args=(lists.id,)))

@login_required(login_url="/login")
def bid(request, list_id):
    if request.method == "POST":
        
        # Get the bid 
        form = NewBid(request.POST)

        # check for the validity
        if form.is_valid():

            # get The user db
            user_id = request.POST["bider"]
            user = User.objects.get(pk=user_id)

            # Error
            if not user:
                ...

            # get the amount of bid
            lists = Listing.objects.get(pk=list_id)

            # Error: list is not found
            if not lists:
                ...
        
            
            # compare it with the highest bid using get_bid() function 
            new_bid = form.cleaned_data['price']
            max_bid, length = get_bid(lists)

            # Error bid must be greater than max_bid
            if max_bid > new_bid:
                raise ValueError

            # else add that to the bid 
            bid = Bid(user=user, bid=new_bid)
            bid.save()
            bid.listing.add(lists)

        # Redirect With correct message
        return HttpResponseRedirect(reverse('lists', args=(lists.id,)))