from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from .models import Character, Chapter, Question
from .forms import QuestionForm, RefineQuestionForm
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
    success_url = reverse_lazy('conan_db_app:question_list')

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        messages.success(self.request, "保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.warning(self.request, "保存できませんでした")
        return super().form_invalid(form)

class QuestionListView(ListView, FormMixin):
    model = Question
    template_name = 'conan_db_app/question_list.html'
    paginate_by = 3
    form_class = RefineQuestionForm
    
    def get_queryset(self):
        # POST リクエストパラメータがあれば、それでフィルタする
        if self.request.POST:
            queryset = Question.objects.filter(jenre=self.request.POST['jenre'])\
                .filter(kind=self.request.POST['kind'])

        # GETリクエストパラメータがあれば、それでフィルタする
        elif self.request.GET:
            # queryset = queryset.object.filter(jenre=keyword)
            queryset = Question.objects.filter(jenre=self.request.GET.get('jenre'))\
                .filter(kind=self.request.GET.get('kind'))

        # 最初のアクセス時はリクエストパラメータが存在しないので全質問データを返す。
        else:
            queryset = Question.objects.all()
        return queryset
        
    def get_context_data(self, **kwargs):
        print(self.request.GET)
        if not self.request.GET:
            # Do this...
            print('null')
            return super().get_context_data(test='test')
        else:
            # GET リクエストパラメータが存在するときこれをフォームにセットする。
            return super().get_context_data(form=self.form_class(self.request.GET))
    
    def post(self, request):
        form = self.form_class(request.POST)
        return self.get(request)