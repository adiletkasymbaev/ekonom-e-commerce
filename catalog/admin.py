from django.contrib import admin
from .models import (
    ProductCategory,
    ProductType,
    ProductSize,
    Product,
    Discount
)
from django.utils.html import format_html

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)


# @admin.register(ProductType)
# class ProductTypeAdmin(admin.ModelAdmin):
#     list_display = ("name", "slug")
#     prepopulated_fields = {"slug": ("name",)}
#     search_fields = ("name",)
#     ordering = ("name",)


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ("name", "category", "type", "price", "get_discount_display", "get_final_price_display")
    # list_filter = ("category", "type", "sizes")
    list_display = ("name", "thumbnail_preview", "category", "price", "get_discount_display", "get_final_price_display")
    list_filter = ("category", "sizes")
    search_fields = ("name",)
    filter_horizontal = ("sizes",)
    readonly_fields = ("slug",)

    def get_discount_display(self, obj):
        discount = obj.get_discount()
        return f"{discount.percentage}%" if discount else "—"
    get_discount_display.short_description = "Скидка"

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width: 50px; height:auto;" />', obj.thumbnail.url)
        return "—"
    thumbnail_preview.short_description = "Превью"

    def get_final_price_display(self, obj):
        return f"{obj.get_final_price():.2f} сом"
    get_final_price_display.short_description = "Цена со скидкой"


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "percentage", "is_active", "start_date", "end_date")
    list_filter = ("is_active", "start_date", "end_date")
    search_fields = ("name",)
    # filter_horizontal = ("categories", "types", "products")
    filter_horizontal = ("categories", "products")
    ordering = ("-start_date",)
