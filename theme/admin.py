from django.contrib import admin
from . import models 

admin.site.register(models.SiteSettings)
admin.site.register(models.SocialLink)  
admin.site.register(models.Banner)  
admin.site.register(models.FeaturedProducts)  