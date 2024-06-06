from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User,Category,Listing,Comment,Bid


def index(request):
    activelistings=Listing.objects.filter(isActive=True)
    allcategories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":activelistings,
        "categories":allcategories
    })
def dispalycategory(request):
    if request.method=="POST":
        categoryinput=request.POST['categoryobject']
        category=Category.objects.get(categoryName=categoryinput)
        #in the below line we've already filtered the required listings to be rendered on the page
        activelistings=Listing.objects.filter(isActive=True,category=category)
        categories=Category.objects.all()
        return render(request, "auctions/index.html",{
        "listings":activelistings,
        "categories":categories
    })
def listing(request,id):
    listingobject=Listing.objects.get(pk=id)
    isOwner= request.user.username==listingobject.owner.username
    #verifying user in watchlist
    isListinginWatchList=request.user in listingobject.watchlist.all()
    allcomments=Comment.objects.filter(listing=listingobject)
    return render(request,"auctions/listing.html",{
        "listingitem":listingobject,
        "isListinginWatchList":isListinginWatchList,
        "comments":allcomments,
        "isOwner":isOwner
    })
def removefromwatchlist(request,id):
    listingdata=Listing.objects.get(pk=id)
    curruser=request.user
    listingdata.watchlist.remove(curruser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))
def addtowatchlist(request,id):
    listingdata=Listing.objects.get(pk=id)
    curruser=request.user
    listingdata.watchlist.add(curruser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))
def displaywatchlist(request):
    curruser=request.user
    #retriving the listings using the user and related name from models.py
    listings=curruser.watchlist.all()
    return render(request,"auctions/watchlist.html",{
        "listings":listings
    })

def addComment(request,id):
    if request.method=="POST":
        curruser=request.user
        listingdata=Listing.objects.get(pk=id)
        comment=request.POST['newcomment']
        newComment=Comment(author=curruser,listing=listingdata,message=comment)
        newComment.save()
        #we can retrieve this data by using listing function by taking of comments.objects.all
        return HttpResponseRedirect(reverse("listing",args=(id, )))

def creatinglisting(request):
    if request.method=="GET":
        allCategories=Category.objects.all()
        return render(request,"auctions/create.html",{
            "category":allCategories
        })
    else:
        #Get the Data From the form
        titleinput=request.POST['title']
        descriptioninput=request.POST['description']
        imgurlinput=request.POST['imageurl']
        priceinput=request.POST['price']
        categoryinput=request.POST['category']
        #retriving user
        currentuser=request.user
        #get category data
        categorydata=Category.objects.get(categoryName=categoryinput)
        #create a bid object
        bid=Bid(bid=float(priceinput),user=currentuser)
        bid.save()
        #Create new Listing Object
        newListing=Listing(title=titleinput,description=descriptioninput,imageurl=imgurlinput,price=bid,category=categorydata,owner=currentuser)
        #Insert objects into our database
        newListing.save()
        #Redirect to index page
        return HttpResponseRedirect(reverse("index"))


def addBid(request,id):
    listingobject=Listing.objects.get(pk=id)
    newbid=request.POST['newbid']
    isListinginWatchList=request.user in listingobject.watchlist.all()
    allcomments=Comment.objects.filter(listing=listingobject)
    isOwner= request.user.username==listingobject.owner.username
    if(float(newbid)>listingobject.price.bid):
        updateBid=Bid(user=request.user,bid=newbid)
        updateBid.save()
        listingobject.price=updateBid
        listingobject.save()
        return render(request,"auctions/listing.html",{
            "listingitem":listingobject,
            "message":"Bid updated Successfully",
            "update":True,
            "comments":allcomments,
            "isOwner":isOwner
        })
    else:
        return render(request,"auctions/listing.html",{
            "listingitem":listingobject,
            "message":"Unsuccessful Bid",
            "update":False,
            "isListinginWatchList":isListinginWatchList,
            "comments":allcomments,
            "isOwner":isOwner
        })
    
def closeauction(request,id):
    #just making isactive is false we can delete the listings from active listings page
    listing=Listing.objects.get(pk=id)
    listing.isActive=False
    listing.save()
    isOwner= request.user.username==listing.owner.username
    #verifying user in watchlist
    isListinginWatchList=request.user in listing.watchlist.all()
    allcomments=Comment.objects.filter(listing=listing)
    return render(request,"auctions/listing.html",{
        "listingitem":listing,
        "isListinginWatchList":isListinginWatchList,
        "comments":allcomments,
        "isOwner":isOwner,
        "update":True,
        "message":"Congratulations,Your Auction is Closed"
        
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
