from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from .models import Character, Chapter, Question, Affiliation, Case
from .forms import QuestionForm, RefineQuestionForm, WithEventForm, WithEventForm2, CaseKindForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib import messages  # メッセージフレームワーク

# Create your views here.

class IndexView(TemplateView):        

    def get(self, request):
        return render(request, 'conan_db_app/index.html')

class CharaListView(ListView):
    model = Character

class AffiliationListView(ListView):
    model = Affiliation

class AffiliationDetailView(DetailView):
    model = Affiliation

class CaseListView(ListView, FormMixin):
    model = Case
    paginate_by = 3
    form_class = WithEventForm

    def get_queryset(self):
        # if self.request.POST.get('with_event') or self.request.POST.get('with_event2'):
        #     case_number_with_event = [i_case.number for i_case in Case.objects.all() if i_case.chapter_set.filter(event = True)]
        #     queryset = Case.objects.filter(number__in=case_number_with_event)
            
        if kind_list := self.request.POST.getlist('case_kind'):
        
            case_with_kind = []
            for i_case in Case.objects.all():
                for i_kind in i_case.kind.all():
                    # if any(i_kind.name in j_kind for j_kind in kind_list):
                    if i_kind.name in kind_list:
                        print(f'{i_case.name}:  あり')
                        case_with_kind.append(i_case.number)
                        break
                    else:
                        print(f'{i_case.name}:  なし')
            print(f'case_with_kind = {case_with_kind}')            
            
            queryset = Case.objects.filter(number__in=case_with_kind)

        else :
            queryset = Case.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        form_list = {
            'form2': WithEventForm2(**self.get_form_kwargs()),
            'form3': CaseKindForm(**self.get_form_kwargs())
        }
        print(self.request.POST)
        kwargs.update(form_list)
        return super().get_context_data(**kwargs)

    def post(self, request, page = None):
        return self.get(request)

class CaseDetailView(DetailView):
    model = Case

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
        if self.request.POST:
            queryset = Question.objects.filter(jenre=self.request.POST['jenre'])\
                .filter(kind=self.request.POST['kind'])
        elif self.request.GET:
            queryset = Question.objects.filter(jenre=self.request.GET.get('jenre'))\
                .filter(kind=self.request.GET.get('kind'))
        else:
            queryset = Question.objects.all()
        return queryset
        
    def get_context_data(self, **kwargs):
        if self.request.POST:
            return super().get_context_data(form=self.form_class(self.request.POST))
        elif self.request.GET:
            return super().get_context_data(form=self.form_class(self.request.GET))
        else:
            return super().get_context_data()
    
    def post(self, request):
        # form = self.form_class(request.POST)
        return self.get(request)



def chara_detail_func(request, pk, page=1):
    page_num = 5
    character = Character.objects.get(id = pk)
    event = character.event_related_to.all()

    if request.method == 'POST':
        # フォームの用意
        form = WithEventForm(request.POST)

        if request.POST.get('with_event'):
            chapter_list = character.chapter.filter(event = True)
        else :
            chapter_list = character.chapter.all()

    # GETアクセス時の処理
    else:
        # フォームの用意
        form = WithEventForm()

        chapter_list = character.chapter.all()

    chapter_list = chapter_list.order_by('number_in_all')

    context = {
    'character' : character, # html 側で for で回すので、イテラブルとして渡す。
    'chapter_page': queryset_to_page(chapter_list, page_num, page), 
    'event_list': event,
    'form':form
    }
    return render(request, 'conan_db_app/character_detail.html', context)

def queryset_to_page(queryset, page_num, page):
    page_list = Paginator(queryset, page_num)
    return page_list.get_page(page)
