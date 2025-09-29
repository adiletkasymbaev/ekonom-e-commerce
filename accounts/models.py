from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from catalog.models import *

class Contacts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    house_number = models.CharField(max_length=255, null=True, blank=True)
    house_apartment_number = models.PositiveIntegerField(null=True, blank=True)
    phone_number = PhoneNumberField(region="KG", null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}, {self.city}, {self.street} {self.house_number}, {self.phone_number}"
    
    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
    
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def count_items(self):
        return self.items.count()
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, verbose_name="Размер", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"
        unique_together = ("cart", "product", "size")

    def __str__(self):
        return f"{self.product.name} ({self.size}) x {self.quantity}"

    def total_price(self):
        return self.product.get_final_price() * self.quantity