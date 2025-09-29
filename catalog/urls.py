from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static      
from django.urls import path, include
from utils.url_enums import URLNames
from .views import add_to_cart, remove_cart_item, update_cart_item

urlpatterns = [
    path("add_to_cart/<slug:product_slug>/", add_to_cart, name=URLNames.ACTION_ADD_TO_CART),
    path("update_cart/<int:cart_item_id>/<str:action>/", update_cart_item, name=URLNames.ACTION_UPDATE_CART_ITEM),
    path("remove_cart/<int:cart_item_id>/remove/", remove_cart_item, name=URLNames.ACTION_REMOVE_CART_ITEM),
]