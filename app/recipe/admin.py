from django.contrib import admin

from .models import Recipe, Tag, Ingredients

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredients)