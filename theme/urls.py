from django.urls import path
from . import views
from utils.url_enums import URLNames

urlpatterns = [
    path("", views.main_page, name=URLNames.MAIN_PAGE),
    path("cart/", views.cart_page, name=URLNames.CART_PAGE),
    path("order/", views.order_page, name=URLNames.ORDER_PAGE),
    path("action_test_order_submit/", views.action_test_order_submit, name="action_test_order_submit"),
    path("catalog/<slug:category_slug>/", views.catalog_page, name=URLNames.CATALOG_PAGE),
    path("product/<slug:product_slug>/", views.product_detail_page, name=URLNames.PRODUCT_DETAIL_PAGE),
]