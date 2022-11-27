from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Character, Chapter

# Create your views here.

class IndexView(TemplateView):        

    def get(self, request):
        return render(request, 'conan_db_app/index.html')

class CharaListView(ListView):
    model = Character

def chara_detail_func(request, pk):        

    character = Character.objects.get(id = pk)
    chapter = character.chapter.all().order_by('volume_id', 'number')
    context ={
        'data' : character, # html 側で for で回すので、イテラブルとして渡す。
        'data2': chapter,
    }
    return render(request, 'conan_db_app/character_detail.html', context)
