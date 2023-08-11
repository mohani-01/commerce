from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *
from .helpers import *

def index(request):
        lists = Listing.objects.filter(active=True)
        
        return render(request, "auctions/index.html", {
            "lists": lists,
        
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
            "categories": categories,
        } )

@login_required(login_url="/login")
def lists(request, list_id):
    # GET the required listing page
    lists = Listing.objects.filter(pk=list_id, active=True).first() 

    user = request.user
    
    # Error checking
    if not lists:
        raise ValueError("You are accessing auction which is down")

    # Used to determine if the user can add it to watchlist or not 
    watchlist = is_watchlist(lists, user)


    # Get all the comment with the newest comment at top
    comments = lists.comment.all().order_by('-time')

    #get the price and amount of bid on that object
    price, length = get_bid(lists)


    # This have to be modified (current price use helper function in helpers.py)
    return render(request, 'auctions/lists.html', {
        "lists": lists,
        "watchlist" : watchlist,
        "price": price,
        "length": length,
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

            # else add that to the bid  Good it makes it else access
            bid = Bid(user=user, bid=new_bid)
            bid.save()
            bid.listing.add(lists)

        # Redirect With correct message
        return HttpResponseRedirect(reverse('lists', args=(lists.id,)))

@login_required(login_url="/login")  
def closebid(request, list_id):
    if request.method == "POST":
        # get the the user
        user = request.user

        # get the item form db
        lists = Listing.objects.get(pk=list_id)

        # get it from the database 
        if not lists:
            ...

        # check if it exist check the user have the permission user.id == listing.user.id
        if not user.id == lists.user.id:
            return HttpResponse(f"{user.username} are trying to close objects you don't own!")
        
        # Change the active field to False
        lists.active = False    
        print("This objects is ", lists.active)

        
        # Remove the list from watchlist where listing = closed list
        # Removing this list from each individual watchlist might take time when the no of user become larger
        # and larger so instead it will be removed next time every user want to 


        # Figure out what this is used for 
        lists, user, winningbid =  get_winner(lists)

        # Add the winner from the db and add it to BidWinner so that he can acess it
        winner = BidWinner(user=user, winningbid=winningbid)

   
        # then add it to list
        lists = Listing.objects.filter(active=True)
        
        return render(request, "auctions/index.html", {
            "lists": lists,
            "message": f"{user} won the auctions."
        
        })
        # return HttpResponseRedirect()
        # return HttpResponse("Working on it")
    else:
        return HttpResponse("This method is not allowed")

@login_required(login_url="/login")
def closedlistings(request):
    # get the user db

    # get all listing where the user wins
    # BidWinner.objects.filter(user=user)  

    # then return that data as template
    ...

# See you watchlist
@login_required(login_url="/login")
def see_watchlist(request):
        # user
        user = request.user

        watchlist = WatchList.objects.get(user=user)
        

        # get all deactivated lists from the user watchlist
        deactivated_lists = watchlist.listing.filter(active=False)

        # Then remove them if the exist 
        # This is much more efficient than removing it from each users when an auction is closed
        if deactivated_lists:
            for i in range(len(non_listing)):
                watchlist.listing.remove(non_listing[i])

        # get all the lists which are active
        listing = watchlist.listing.all()

        return render(request, 'auctions/index.html', {
            "lists": listing,
        })


# Add to watchlist
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

        # get WatchList with user is person logged in and list be list_id
        watchlist = WatchList.objects.filter(user=user, listing=lists).first()

        # check if the listing exist in Watchlist
        if watchlist:

            # Remove it from Watchlist
            watchlist.listing.remove(lists)

        # Check if user have other listing in WatchList models
        else:
            # get The WatchList by its user
            new_watchlist = WatchList.objects.filter(user=user).first()

            # add the new list to listing field if the user exist
            if new_watchlist:
                new_watchlist.listing.add(lists)

            # if the user doesn't exist in WatchList
            else:
                # Create new WatchList for user
                create_watchlist = WatchList(user=user)
                create_watchlist.save()

                # Add the list into listing page
                create_watchlist.listing.add(lists)


        # redirect the user to the page
        return HttpResponseRedirect(reverse("lists", args=(lists.id,)))

    # Error
    else:
        return HttpResponseNotAllowed(permitted_methods="POST")
    