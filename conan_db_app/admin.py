from django.contrib import admin
from .models import Character, Chapter, CaseKind, Case, Volume, Event,\
    Question, Profession, Affiliation, Wiseword

# Register your models here.

admin.site.register(Character)
admin.site.register(Chapter)
admin.site.register(CaseKind)
admin.site.register(Case)
admin.site.register(Volume)
admin.site.register(Event)
admin.site.register(Question)
admin.site.register(Profession)
admin.site.register(Affiliation)
admin.site.register(Wiseword)
