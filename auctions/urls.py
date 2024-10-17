from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"), 
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.creatinglisting, name="create"),
    path("category/", views.dispalycategory, name="category"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("removefromwatchlist/<int:id>/", views.removefromwatchlist, name="removefromwatchlist"),
    path("addtowatchlist/<int:id>/", views.addtowatchlist, name="addtowatchlist"),
    path("watchlist/", views.displaywatchlist, name="watchlist"),
    path("addComment/<int:id>/", views.addComment, name="addComment"),
    path("addBid/<int:id>/", views.addBid, name="addBid"),
    path("closeauction/<int:id>/", views.closeauction, name="closeauction"),
]
