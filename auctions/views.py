from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseNotAllowed, Http404
from django.shortcuts import render,redirect
from django.urls import reverse

from .models import *
from .forms import *
from .helpers import *

def index(request):
        # Get all listing which are active
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


# Done
def category(request):
    # Via POST
    if request.method == "POST":   

        # Get category form user selection
        get_category = request.POST["category"]

        # Get cateogry object from db, this has to exist logical b/c of else: statement at the bottom [ categories are from the db ]
        category = Category.objects.filter(category=get_category).first()
        
        # Error if the user did with html something
        if not category:
            messages.warning(request, "There is no category by this name, Try again!")
            return HttpResponseRedirect(reverse("category"))
            
        # get all lists where their active value is True
        lists = category.group.filter(active=True).all()
        
        return render(request, "auctions/index.html", {
            "lists": lists,
        })
              
    # Via GET
    else:  
        # Get each category from Category model
        categories = Category.objects.exclude(category="").all()

        # Check if the category doesn't consists atleast one listing then remove it
        not_included = []
        for category in categories:
            if  not category.group.filter(active=True).all():

                not_included.append(category)

        new_categories = categories.exclude(category__in=not_included)

        print(new_categories, "Filtered")
        # categories = Category.objects.exclude(category="").all()
        # print(categories)

        return render(request, 'auctions/category.html', {
            "categories": new_categories,
        })


@login_required(login_url="/login")
def lists(request, list_id):
    # GET the required listing page
    lists = Listing.objects.filter(pk=list_id, active=True).first() 

    user = request.user
    
    # Error checking
    if not lists:
        # messages.success(request, "Profile details updated.")
        messages.error(request, "This Page You request is not Available. Try Another page!")
        return HttpResponseRedirect(reverse("index"))
        # raise ValueError("You are accessing auction which is down")

    # Used to determine if the user can add it to watchlist or not 
    watchlist = is_watchlist(lists, user)


    # Get all the comment with the newest comment at top
    comments = lists.comment.all().order_by('-time')

    #get the price and amount of bid on that object
    # else get the price of the item 
    price, bidder, length = get_bid(lists)
    print("is this correct", price)
    

    # This have to be modified (current price use helper function in helpers.py)
    return render(request, 'auctions/lists.html', {
        "lists": lists,
        "watchlist" : watchlist,
        "price": price,
        "bidder": bidder,
        "length": length,
        "add_comment": NewComment(),
        "comments": comments,
        "bid": NewBid(),
    })



# Done
@login_required(login_url="/login")
def newlist(request):
    # Via POST
    if request.method == "POST":
        form = NewList(request.POST)

        # Get the user
        user = request.user

        # Check if the form is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            
            # Get category
            get_category = request.POST["category"].strip().capitalize() 

            # check if category is given or not
            if not get_category:
                listing = Listing(user=user, title=title, description=description, price=price, image=image)
                listing.save()
                print("Executing it")

            # Get Category if it exist
            else:
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
            messages.success(request, "Your List is added Successfully!")
            return HttpResponseRedirect(reverse("index"))

        # Return inserted form to the user
        else:
            # Get all categories except empty one
            categories = Category.objects.exclude(category="").all()

            # return the form the user inserted  
            messages.warning(request, "Your list is not submitted please insert the from correctly!")

            return render(request, 'auctions/newlist.html', {
            "form": form,
            "categories": categories,
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

# Done
@login_required(login_url="/login")
def comment(request, list_id):
    # Via POST
    if request.method == "POST":

        # Get the form populated data in it
        form = NewComment(request.POST)

        # get the user from request 
        user = request.user

        # get the listing object
        lists = Listing.objects.filter(pk=list_id).first()

        # Check if list exist
        if not lists:
            # all not lists should be Http404
            messages.error(request, "This Page You request is not Available. Try Another page!")
            return HttpResponseRedirect(reverse("index"))

        # check if form is valid
        if form.is_valid():

            # Get the comment
            message = form.cleaned_data["comment"]

            # insert data to comment db
            comment = Comment(user=user, message=message)
            comment.save()

            # add the list to comment db (ManyToMany relationship)
            comment.listing.add(lists)

        # invalid form
        else:
            messages.error(request, f"{user}, Your comment is not submitted. Try again")
            return HttpResponseRedirect(reverse("lists", args=(lists.id,)))
        
        # return the user to its current page 
        return HttpResponseRedirect(reverse("lists", args=(lists.id,)))

    # Via not POST
    else:
        messages.error(request, "Method Not Allowed!")
        return HttpResponseRedirect(reverse("lists", args=(lists.id,)))

# Done
@login_required(login_url="/login")
def bid(request, list_id):
    if request.method == "POST":

        # Get the bid 
        form = NewBid(request.POST)

        # get The user from request
        user = request.user

        # get the amount of bid
        lists = Listing.objects.filter(pk=list_id).first()

        # Error: list is not found
        if not lists:
            messages.error(request, "Page Not Found!")
            return HttpResponseRedirect(reverse("index"))
        
        # Check if the owner of the page isn't bidding on it
        if lists.user.id == user.id:
            message.error(request, "Bidding on your own item is not allowed!")
            return HttpResponseRedirect(reverse('lists', args=(lists.id,)))
        
        # check for the validity
        if form.is_valid():


            # compare it with the highest bid using get_bid() function 
            new_bid = form.cleaned_data['price']

            max_bid, bidder, length = get_bid(lists)

            # Error bid must be greater than max_bid
            if max_bid > new_bid:
                messages.error(request, "Your bid must be greater than other bids!")
                return HttpResponseRedirect(reverse('lists', args=(lists.id,)))

            # else add that to the bid  
            bid = Bid(user=user, bid=new_bid)
            bid.save()
            bid.listing.add(lists)

        else:
            messages.error(request, "Invalid input. Try again")
            return HttpResponseRedirect(reverse('lists', args=(lists.id,)))

        messages.success(request, "Your Bid added successfully and your can check if you win on <a href=\"/closedlistings\">Closed listings</a>  when the auction is closed or you can bid again.")
        # Redirect With correct message
        return HttpResponseRedirect(reverse('lists', args=(lists.id,)))
    
    # Via not POST
    else:
        messages.error(request, "Method Not Allowed!")
        return HttpResponseRedirect(reverse("lists", args=(lists.id,)))



@login_required(login_url="/login")  
def closebid(request, list_id):
    if request.method == "POST":
        # get the the user
        user = request.user

        # get the item form db
        lists = Listing.objects.filter(pk=list_id).first()

        # get it from the database 
        if not lists:
            messages.error(request, "Page Not Found!")
            return HttpResponseRedirect(reverse("index"))

        # Check if the user own the item
        if  user.id != lists.user.id:
            messages.warning(request, f"{user} you are trying to close an auction you don't own!")
            return HttpResponseRedirect(reverse('lists', args=(lists.id,)))
        
        # Change the active field to False
        lists.active = False  
        lists.save()
        print("This objects is ", lists.active)


        # Figure out what this is used for 
        lists, user, winningbid =  get_winner(lists)

        # Add the winner from the db and add it to BidWinner so that he can acess it
        if not lists:
                print("NO Bider")
                messages.error(request, "Nobody bid on this auction. The Page is closed.")
                return HttpResponseRedirect(reverse("index"))

        winner = BidWinner(user=user, winningbid=winningbid, listing=lists)
        winner.save()
        # winner.listing.add(lists)

        messages.success(request, f"The Page is closed successfully. {user} won this auction.")
        return HttpResponseRedirect(reverse("index"))
       
    else:
        return HttpResponse("This method is not allowed")

@login_required(login_url="/login")
def closedlistings(request):
    # get the user db
    user = request.user

    # get all listing where the user wins
    wins = BidWinner.objects.filter(user=user)  
    
    print(wins)
    # then return that data as template
    return render(request, 'auctions/wins.html', {
        "wins": wins,
    })
    ...

# See you watchlist
@login_required(login_url="/login")
def see_watchlist(request):
        # user
        user = request.user

        watchlist = WatchList.objects.filter(user=user).first()

        if not watchlist:
            messages.error(request, "No watchlists have been added yet; please add one!")
            return HttpResponseRedirect(reverse("index"))
        # get all deactivated lists from the user watchlist
        deactivated_lists = watchlist.listing.filter(active=False)

        # Then remove them if the exist 
        # This is much more efficient than removing it from each users when an auction is closed
        if deactivated_lists:
            for i in range(len(deactivated_lists)):
                watchlist.listing.remove(deactivated_lists[i])

        # get all the lists which are active
        listing = watchlist.listing.all()

        return render(request, 'auctions/index.html', {
            "lists": listing,
            "watchlist":True, 
        })


# Add to watchlist
@login_required(login_url="/login")
def watchlist(request, list_id):
    if request.method == "POST":
        # get the user id
        user = request.user

        # Get the list 
        lists = Listing.objects.filter(pk=list_id, active=True).first()

        # Check if the list exist
        if not lists:
            messages.error(request, "Page not Found")
            return HttpResponseRedirect(reverse("index"))

        # this 'function' do both adding to watchlist and removing it

        # The following 8+ lines remove the item form watchlist
        # Check if the user add this page to their watchlist
        watchlist = WatchList.objects.filter(user=user, listing=lists).first()

        # Remove it if they already have it
        if watchlist:

            # Remove it from Watchlist
            watchlist.listing.remove(lists)

            # redirect the user to the page with message
            messages.success(request, "This page is Removed from your Watchlist Successfully!")
            return HttpResponseRedirect(reverse("lists", args=(lists.id,)))


        # The following 35+ lines add the item to watchlist

        # Get watchlist db if the user have other watchlists
        new_watchlist = WatchList.objects.filter(user=user).first()

        # Check if user have other listing in WatchList model
        if new_watchlist: 

            # add the new list to listing field if the user exist
            new_watchlist.listing.add(lists)

        # if the user doesn't exist in WatchList
        else:
            # Create new WatchList for user
            create_watchlist = WatchList(user=user)
            create_watchlist.save()

            # Add the list into listing page
            create_watchlist.listing.add(lists)
        # redirect the user to the page with a message
        messages.success(request, "This page is Add to Your Watchlist Successfully!")
        return HttpResponseRedirect(reverse("lists", args=(lists.id,)))

    # Error
    else:
        # return HttpResponseNotFound("<h1>404: Page not found</h1>")
        return HttpResponseNotAllowed(permitted_methods="POST")
    