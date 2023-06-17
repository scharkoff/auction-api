from django.contrib import admin
from django.urls import path, include
from auction.routers.routers import urlpatterns as auction_routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(auction_routers)),
]
