from django.contrib import admin

from .models import Recipe, User

# Register your models here.
admin.site.register(Recipe)
# admin.site.register(Vote)

admin.site.register(User)
