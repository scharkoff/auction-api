from django.urls import path
from auction.controllers.auth.authController import AuthController
from auction.controllers.auction.auctionController import AuctionController
from auction.controllers.users.usersController import UsersController

urlpatterns = [
    path('auth/login/', AuthController.login, name='login'),
    path('auth/register/', AuthController.register, name='register'),
    path('auth/logout/', AuthController.logout, name='logout'),

    path('auction/create/', AuctionController.create, name='create'),
    path('auction/update/', AuctionController.update, name='update'),
    path('auction/close/', AuctionController.close, name='close'),
    path('auction/getById/', AuctionController.getById, name='getById'),
    path('auction/getAll/', AuctionController.getAll, name='getAll'),
    path('auction/search/', AuctionController.search, name='search'),

    path('users/getAll/', UsersController.getAll, name='getAll'),
    path('users/getById/', UsersController.getById, name='getById'),
    path('users/create/', UsersController.create, name='create'),
    path('users/update/', UsersController.update, name='update'),
    path('users/delete/', UsersController.delete, name='delete'),
]
