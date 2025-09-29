from django.db import models
from catalog import models as catalog_models

class SiteSettings(models.Model):
    company_name = models.CharField("Название компании", max_length=255)
    working_hours_start = models.TimeField("Начало работы")
    working_hours_end = models.TimeField("Конец работы")
    phone_number = models.CharField("Номер телефона (1)", max_length=255)
    phone_number2 = models.CharField("Номер телефона (2)", max_length=255)
    address = models.CharField("Адрес", max_length=255)
    logo = models.ImageField(upload_to='logos/')
    bg_transparent_logo = models.ImageField(upload_to='logos/', default="...")

    def __str__(self):
        return "Изменить настройки сайта"

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

class SocialLink(models.Model):
    settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, verbose_name="Настройки")
    logo = models.ImageField(upload_to='social_logos/')
    name = models.CharField("Название", max_length=255)
    link = models.CharField("Ссылка", max_length=1000)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Социальные сети"
        verbose_name_plural = "Социальные сети"

class Banner(models.Model):
    image = models.ImageField("Изображение", upload_to="banners/")
    title = models.CharField("Заголовок", max_length=255)
    description = models.CharField("Описание", max_length=255)
    button_text = models.CharField("Текст кнопки", max_length=255)
    button_link = models.CharField("Ссылка кнопки", max_length=255)

    def __str__(self):
        return f"{self.title} — {self.description}"
    
    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

class FeaturedProducts(models.Model):
    title = models.CharField("Название подборки", max_length=255, default="Главная страница")
    products = models.ManyToManyField(catalog_models.Product, verbose_name="Товары для главной")

    class Meta:
        verbose_name = "Товары на главной"
        verbose_name_plural = "Товары на главной"

    def __str__(self):
        return self.title