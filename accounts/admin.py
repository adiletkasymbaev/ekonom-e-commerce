from django.contrib import admin
from .models import Contacts, Cart, CartItem
from catalog.models import *

@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "street", "house_number", "house_apartment_number", "phone_number")
    search_fields = ("user__email", "city", "street", "house_number", "phone_number")
    list_filter = ("city",)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("total_price_display",)
    autocomplete_fields = ("product", "size")
    
    def total_price_display(self, obj):
        return f"{obj.total_price():.2f} ₽"
    total_price_display.short_description = "Сумма"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "total_price_display")
    search_fields = ("user__email",)
    inlines = [CartItemInline]

    def total_price_display(self, obj):
        return f"{obj.total_price():.2f} ₽"
    total_price_display.short_description = "Общая сумма"