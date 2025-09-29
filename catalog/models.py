from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class AutoSlugMixin(models.Model):
    slug_source_field = 'name' 
    slug_field_name = 'slug'

    class Meta:
        abstract = True  # чтобы Django не создавала таблицу

    def generate_unique_slug(self):
        source_value = getattr(self, self.slug_source_field, None)
        if not source_value:
            return None

        base_slug = slugify(unidecode(source_value))
        slug = base_slug
        ModelClass = self.__class__
        num = 1

        while ModelClass.objects.filter(**{self.slug_field_name: slug}).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1

        return slug

    def save(self, *args, **kwargs):
        slug_field = self.slug_field_name
        slug_value = self.generate_unique_slug()
        setattr(self, slug_field, slug_value)
        super().save(*args, **kwargs)

class ProductCategory(AutoSlugMixin):
    name = models.CharField("Название", max_length=100)
    image = models.ImageField(upload_to="product_category_images/", null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория"
    )

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return " → ".join(full_path[::-1])

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

# Пока будет недоступен в админке
class ProductType(AutoSlugMixin):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Тип товара"
        verbose_name_plural = "Типы товаров"

class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]
    name = models.CharField("Размер", max_length=5, choices=SIZE_CHOICES, unique=True)

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return self.name

class Product(AutoSlugMixin):
    category = models.ForeignKey(
        ProductCategory,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="categories"
    )
    # type = models.ForeignKey(
    #     ProductType,
    #     verbose_name="Категория",
    #     on_delete=models.CASCADE,
    #     related_name="types"
    # )
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    sizes = models.ManyToManyField(ProductSize, verbose_name="Доступные размеры", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images/")
    thumbnail = models.ImageField(upload_to="product_images/thumbnails/", blank=True, null=True)
    views = models.PositiveIntegerField("Просмотры", default=0)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image and not self.thumbnail:
            self.generate_thumbnail()

    def generate_thumbnail(self):
        img = Image.open(self.image)
        img = img.convert("RGB")  # конвертируем и сохраняем результат
        img.thumbnail((300, 300))  # делаем миниатюру

        thumb_io = BytesIO()
        img.save(thumb_io, format="JPEG", quality=85)

        thumb_name = f"thumb_{self.image.name.split('/')[-1]}"
        self.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)
        super().save(update_fields=['thumbnail'])

    def get_discount(self):
        from django.utils import timezone
        now = timezone.now()
        discounts = Discount.objects.filter(
            is_active=True,
            start_date__lte=now
        ).filter(
            models.Q(end_date__gte=now) | models.Q(end_date__isnull=True)
        ).filter(
            models.Q(products=self) |
            models.Q(categories=self.category)
            # models.Q(types=self.type)
        ).order_by('-percentage')

        return discounts.first()

    def get_final_price(self):
        discount = self.get_discount()
        if discount:
            return self.price * (1 - discount.percentage / 100)
        return self.price
    
    class Meta:
        ordering = ["-views"] 
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} - {self.price} сом"

class Discount(models.Model):
    name = models.CharField("Название акции", max_length=255)
    percentage = models.DecimalField(
        "Скидка в %",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    categories = models.ManyToManyField(
        ProductCategory,
        blank=True,
        verbose_name="Категории",
        related_name="discounts"
    )
    # types = models.ManyToManyField(
    #     ProductType,
    #     blank=True,
    #     verbose_name="Типы товаров",
    #     related_name="discounts"
    # )
    products = models.ManyToManyField(
        "Product",
        blank=True,
        verbose_name="Товары",
        related_name="discounts"
    )
    start_date = models.DateTimeField("Дата начала", default=timezone.now)
    end_date = models.DateTimeField("Дата окончания", blank=True, null=True)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

    def is_valid_now(self):
        now = timezone.now()
        return self.is_active and (not self.end_date or self.end_date >= now) and self.start_date <= now