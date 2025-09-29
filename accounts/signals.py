from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Cart, Contacts

@receiver(user_signed_up)
def create_cart_for_new_user(request, user, **kwargs):
    Cart.objects.create(user=user)
    Contacts.objects.create(user=user)