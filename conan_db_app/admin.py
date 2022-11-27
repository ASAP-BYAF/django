from django.contrib import admin
from .models import Character, Chapter, Case, Volume

# Register your models here.

admin.site.register(Character)
admin.site.register(Chapter)
admin.site.register(Case)
admin.site.register(Volume)
