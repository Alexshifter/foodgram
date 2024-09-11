from django.contrib import admin
from .models import NewUser
from recipes.models import Tag, Ingredient, Recipe
# Register your models here.


admin.site.register(NewUser)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
