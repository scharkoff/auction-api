from django.urls import path
from auction.controllers.auth.authController import AuthController
from auction.controllers.auction.auctionController import AuctionController

urlpatterns = [
    path('auth/login/', AuthController.login, name='login'),
    path('auth/register/', AuthController.register, name='register'),
    path('auth/logout/', AuthController.logout, name='logout'),

    path('auction/create/', AuctionController.create, name='create'),
    path('auction/update/', AuctionController.update, name='update'),
    path('auction/close/', AuctionController.close, name='close'),
    path('auction/get/', AuctionController.get, name='get'),
    path('auction/search/', AuctionController.search, name='search'),
]
