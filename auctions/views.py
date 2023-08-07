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

    # Error checking
    if not lists:
        ... 
    # Get all the comment with the newest comment at top
    comments = lists.comment.all().order_by('-time')

    # This have to be modified (current price use helper function in helpers.py)
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
            image = form.cleaned_data["image"]
            
            # Get category
            get_category = request.POST["category"].strip().capitalize() 
            print(get_category)
            if not get_category:
                raise ValueError("making sure that the field is correct") 
            # Get the user
            user = User(pk=user_id)
        
            # Return to newlisting page if the user doesn't exist
            # it is not possbile if db is malfunctioning or the user change 
            # the value of user.id in newlisting.html is changed
            if not user:
                ...
                
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
            # GET the user id from the form
            user_id = int(request.POST["commenter"])

            # get the user db
            user = User.objects.get(pk=user_id)


            # Check if user exist
            if not user:
                ...
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
                raise ValueError("This needs to return eRroR page")

            # else add that to the bid 
            bid = Bid(user=user, bid=new_bid)
            bid.save()
            bid.listing.add(lists)

        # Redirect With correct message
        return HttpResponseRedirect(reverse('lists', args=(lists.id,)))