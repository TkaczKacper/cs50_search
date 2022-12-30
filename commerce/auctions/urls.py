from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('create_listing', views.create_listing, name='create_listing'),
    path('listings/<int:number>', views.listing, name='listings'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:number>/bid", views.make_bid, name='make_bid'),
    path("listings/<int:number>/comment", views.add_comment, name='add_comment'),
    path("listings/<int:number>/finish", views.finish_auction, name='finish_auction'),
    path("listings/<int:number>/add_watchlist", views.add_to_watchlist, name='add_to_watchlist'),
    path("listings/<int:number>/remove_watchlist", views.remove_from_watchlist, name='remove_from_watchlist'),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category")
]

urlpatterns += staticfiles_urlpatterns()
