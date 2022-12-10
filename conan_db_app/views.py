from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Character, Chapter
from django.core.paginator import Paginator

# Create your views here.

class IndexView(TemplateView):        

    def get(self, request):
        return render(request, 'conan_db_app/index.html')

class CharaListView(ListView):
    model = Character

def chara_detail_func(request, pk, page):        

    character = Character.objects.get(id = pk)
    chapter = character.chapter.all().order_by('volume_id', 'number')
    chapter_page = Paginator(chapter, 5)
    event = character.event_related_to.all()
    context ={
        'character' : character, # html 側で for で回すので、イテラブルとして渡す。
        # 'chapter_list': chapter,
        'chapter_list': chapter_page.get_page(page),
        'event_list': event,
    }
    return render(request, 'conan_db_app/character_detail.html', context)
