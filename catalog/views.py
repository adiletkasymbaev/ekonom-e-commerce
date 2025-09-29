from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from accounts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from .models import Product, ProductSize
from utils.url_enums import URLNames
from django.contrib import messages

@login_required
@require_POST
def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart, created = Cart.objects.get_or_create(user=request.user)

    next_url = request.POST.get("next") or URLNames.MAIN_PAGE  # если не передали, редирект на главную

    size_id = request.POST.get("size_id")
    if not size_id:
        messages.error(request, "Выберите размер товара перед добавлением в корзину.")
        return redirect(next_url)
    
    size = get_object_or_404(ProductSize, id=size_id)
    if size not in product.sizes.all():
        messages.error(request, "Выбранный размер недоступен для этого товара.")
        return redirect(next_url)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Товар {cart_item.product} успешно добавлен в корзину')

    return redirect(next_url)

@login_required
def update_cart_item(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Количество {cart_item.product.name} увеличено")

    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f"Количество {cart_item.product.name} уменьшено")
        else:
            cart_item.delete()
            messages.info(request, f"{cart_item.product.name} удалён из корзины")

    return redirect(URLNames.CART_PAGE)

def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.info(request, f"{cart_item.product.name} удалён из корзины")
    return redirect(URLNames.CART_PAGE)