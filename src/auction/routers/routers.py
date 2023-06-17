from django.urls import path
from auction.controllers.auth.authController import AuthController

urlpatterns = [
    path('auth/login/', AuthController.login, name='login'),
    path('auth/register/', AuthController.register, name='register'),
    path('auth/logout/', AuthController.logout, name='logout'),
]
