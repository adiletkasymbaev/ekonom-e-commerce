from accounts.models import Cart
from . import models
from catalog import models as product_models
from utils.url_enums import URLNames
from django.contrib.auth.decorators import login_required

from django.core.cache import cache

def site_settings(request):
    settings = cache.get_or_set("site_settings", lambda: models.SiteSettings.objects.first())
    socials = cache.get_or_set("social_links", lambda: list(models.SocialLink.objects.all()))
    banners = cache.get_or_set("banners", lambda: list(models.Banner.objects.all()))
    featured_products = cache.get_or_set("featured_products", lambda: models.FeaturedProducts.objects.first())
    categories_parent = cache.get_or_set("categories_parent", lambda: list(product_models.ProductCategory.objects.filter(parent__isnull=True)))

    cart = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)

    return {
        'site_settings': settings,
        'banners': banners,
        'socials_list': socials,
        'categories_parent': categories_parent,
        'featured_products': featured_products,
        'URLNames': {name: member.value for name, member in URLNames.__members__.items()},
        'cart': cart,
        'is_authenticated': request.user.is_authenticated,
        'user': request.user
    }