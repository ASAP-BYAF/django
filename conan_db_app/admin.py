from django.contrib import admin
from .models import Character, Chapter, Case, Volume, Event, Question

# Register your models here.

admin.site.register(Character)
admin.site.register(Chapter)
admin.site.register(Case)
admin.site.register(Volume)
admin.site.register(Event)
admin.site.register(Question)
