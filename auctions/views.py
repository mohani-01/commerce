from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *
from .helpers import *

def index(request):
    lists = Listing.objects.filter(active=True)
    print(lists)
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


def category(request):
    # Via POST
    if request.method == "POST":   

        # Get category form user selection
        get_category = request.POST["category"]


        # Get cateogry object from db, this has to exist logical b/c of else: statement at the bottom [ categories are from the db ]
        category = Category.objects.get(category=get_category)
        
        # Error the user did something
        if not category:
            ...
        # get all lists where their active value is True
        lists = category.group.filter(active=True).all()
        
        return render(request, "auctions/index.html", {
            "lists": lists,
        })
              
    # Via GET
    else:  
        # Get each category from Category model
        categories = Category.objects.exclude(category="").all()
        return render(request, 'auctions/category.html', {
            "categories":categories,
        } )

@login_required(login_url="/login")
def lists(request, list_id):

    
    # GET the required listing page
    lists = Listing.objects.get(pk=list_id)
   
    user = request.user
    watchlist = get_watchlist(lists, user)
    

    # Error checking
    if not lists:
        ... 

    # Get all the comment with the newest comment at top
    comments = lists.comment.all().order_by('-time')

    # This have to be modified (current price use helper function in helpers.py)
    return render(request, 'auctions/lists.html', {
        "lists": lists,
        "watchlist" : watchlist,
        "add_comment": NewComment(),
        "comments": comments,
        "bid": NewBid(),
    })



@login_required(login_url="/login")
def newlist(request):
    # Via POST
    if request.method == "POST":
        form = NewList(request.POST)

        # Check if the form is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            
            # Get category
            get_category = request.POST["category"].strip().capitalize() 

           
            # Get the user
            user = request.user
        
    
            # Get Category if it exist
            category = Category.objects.filter(category=get_category).first()

            # add that category and others into Listing db
            if category:
                
                # Add all datas into listing database and save the data
                listing = Listing(user=user, title=title, description=description, price=price, category=category, image=image)
                listing.save()

            # create new category and add others into 
            else:
                category = Category(category=get_category)
                category.save()

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
        # Get all categories except empty one
        categories = Category.objects.exclude(category="").all()

        # return to user with input tag for title, description, price, category and image url
        return render(request, 'auctions/newlist.html', {
            "form": NewList(),
            "categories": categories,
        })


@login_required(login_url="/login")
def comment(request, list_id):
    # Via POST
    if request.method == "POST":

        # Get the form populated data in it
        form = NewComment(request.POST)

        # check if form is valid
        if form.is_valid():

        
            # get the user from request 
            user = request.user

            # get the listing object
            lists = Listing.objects.get(pk=list_id)

            # Check if list exist
            if not lists:
                ...
            # Get the comment
            message = form.cleaned_data["comment"]

            # insert data to comment db
            comment = Comment(user=user, message=message)
            comment.save()

            # add the list to comment db (ManyToMany relationship)
            comment.listing.add(lists)

        # return the user to its current page 
        return HttpResponseRedirect(reverse("lists", args=(lists.id,)))

    else:
        return HttpResponse("Method Not allowed")
@login_required(login_url="/login")
def bid(request, list_id):
    if request.method == "POST":
        
        # Get the bid 
        form = NewBid(request.POST)

        # check for the validity
        if form.is_valid():

            # get The user from request
            user = request.user

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
                raise ValueError("This needs to return eRroR page   ")

            # else add that to the bid 
            bid = Bid(user=user, bid=new_bid)
            bid.save()
            bid.listing.add(lists)

        # Redirect With correct message
        return HttpResponseRedirect(reverse('lists', args=(lists.id,)))

@login_required(login_url="/login")  
def closebid(request, list_id):
    # get the items id

    # get it from the database 

    # check if it exist check the user have the permission user.id == listing.user.id

    # check the active field to False
    
    # Remove the list from watch list where listing = closed list
   
    # Add the winner from the db and add it to BidWinner so that he can acess it
    ...
@login_required(login_url="/login")
def watchlist(request, list_id):
    if request.method == "POST":
        # get the user id
        user = request.user

        # Get the list 
        lists = Listing.objects.get(pk=list_id, active=True)

        # Check if the list exist
        if not lists:
            ...
        watchlist = WatchList.objects.filter(user=user, listing=lists).first()



        # check if the listing exist in Watchlist
        if watchlist:
            watchlist.listing.remove(lists)
            listsss = watchlist.listing.all()
            print(f"Watchlist.id {listsss} ")
            # Remove it from Watchlist
            remove = watchlist
            print(remove)

        # Add it to watchlist
        else:
            # Get the user by its id
            new_watchlist = WatchList.objects.filter(user=user).first()
            print(new_watchlist)
            if new_watchlist:
                new_watchlist.listing.add(lists)

            else:
                create_watchlist = WatchList(user=user)
                create_watchlist.save()
                create_watchlist.listing.add(lists)


        # redirect the user to the page
        return HttpResponseRedirect(reverse("lists", args=(lists.id,)))

    # Error
    else:
        return HttpResponse("This page can't be accessed")

@login_required(login_url="/login")
def see_watchlist(request):
   
        # user
        user = request.user

        watchlist = WatchList.objects.get(user=user)
        listing = watchlist.listing.all()
       
    
        return render(request, 'auctions/index.html', {
            "lists": watchlist.listing.all(),
        })