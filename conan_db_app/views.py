from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import Character, Chapter, Question
from .forms import QuestionForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib import messages  # メッセージフレームワーク

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

class QuestionCreateView(CreateView):
    form_class = QuestionForm
    template_name = 'conan_db_app/question_form.html'
    success_url = reverse_lazy('conan_db_app:questions')

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        messages.success(self.request, "保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.warning(self.request, "保存できませんでした")
        return super().form_invalid(form)
