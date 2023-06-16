from django.urls import path
from auction.controllers.controllers import test_view

urlpatterns = [
    path('test/', test_view, name='test'),
]
