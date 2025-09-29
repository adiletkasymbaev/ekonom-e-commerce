from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Cart
from catalog import models as catalog_models
from utils.functions import get_category_ids
from django.core.paginator import Paginator
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.url_enums import URLNames

def main_page(request):
    return render(request, "main.html")

@login_required
def cart_page(request):
    return render(request, "cart.html")

@login_required
def profile_page(request):
    return render(request, 'profile.html')

@login_required
def order_page(request):
    return render(request, 'order.html')

@login_required
def action_test_order_submit(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.delete()
    cart.save()

    messages.success(request, "Оплата успешно произведена")
    return redirect(URLNames.MAIN_PAGE)

def catalog_page(request, category_slug):
    category = get_object_or_404(catalog_models.ProductCategory, slug=category_slug)
    category_ids = get_category_ids(category)
    products_list = catalog_models.Product.objects.filter(category_id__in=category_ids).order_by("-views")

    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        "category": category,
        "products": products,
        "products_count": products_list.count(),
    }
    return render(request, "catalog.html", context)

def product_detail_page(request, product_slug):
    product = get_object_or_404(catalog_models.Product, slug=product_slug)
    catalog_models.Product.objects.all().filter(slug=product_slug).update(views=F("views") + 1)

    context = { 'product': product }

    return render(request, 'product_detail.html', context)