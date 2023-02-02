from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from .models import Character, Chapter, Question, Affiliation, Case, Wiseword
from .forms import QuestionForm, RefineQuestionForm, WithEventForm,\
     WithEventForm2, CaseKindForm, VolumeForm, CharaForm, CaseNameForm
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


class WisewordListView(ListView, FormMixin):
    model = Wiseword
    paginate_by = 3
    form_class = CharaForm

    def post(self, request, page = None):
        return self.get(request)

    def get_queryset(self):
        # 各絞り込みに当てはまる事件の番号の集合を記録
        refined_wiseword_number_list = []

        # 名言をキャラクターについて or 検索
        if chara_list := self.request.POST.getlist('character'):       
            tmp = set()
            for i_wiseword in Wiseword.objects.all():
                if any([ j_chara == i_wiseword.character.name for j_chara in chara_list]):
                    tmp.add(i_wiseword.id)
            refined_wiseword_number_list.append(tmp)

        if refined_wiseword_number_list:
            for i, i_refined_set in enumerate(refined_wiseword_number_list, 1):
                if i == 1:
                    and_refined_set = i_refined_set
                else:
                    and_refined_set &= i_refined_set
            queryset = Wiseword.objects.filter(id__in=and_refined_set)
            
        else :
            queryset = Wiseword.objects.all()

        return queryset

class CaseListView(ListView, FormMixin):
    model = Case
    paginate_by = 3
    form_class = WithEventForm

    def get_queryset(self):
        # 各絞り込みに当てはまる事件の番号の集合を記録
        refined_case_number_list = []
        
        # 重要な出来事がに対する絞り込みがあれば当てはまる事件の番号の集合を
        # 集合のリスト refined_case_number_list に登録    
        if self.request.POST.get('with_event'):
            tmp = set()
            for i_case in Case.objects.all():
                for i_chapter in i_case.chapter_set.all():
                    if i_chapter.event_set.all():
                        tmp.add(i_case.number)
            refined_case_number_list.append(tmp)            

        # 事件の種類による絞り込みがあれば当てはまる事件の番号の集合を
        # 集合のリスト refined_case_number_list に登録    
        if kind_list := self.request.POST.getlist('case_kind'):       
            tmp = set()
            for i_case in Case.objects.all():
                kind_list_i_case = [ i_kind.name for i_kind in i_case.kind.all()]
                if all([ j_kind in kind_list_i_case for j_kind in kind_list]):
                    tmp.add(i_case.number)
            refined_case_number_list.append(tmp)
            
        # 巻数による絞り込みがあれば当てはまる事件の番号の集合を
        # 集合のリスト refined_case_number_list に登録    
        if vol_list := self.request.POST.getlist('volume'):       
            tmp = set()
            for i_case in Case.objects.all():
                vol_list_i_case = { i_chapter.volume.number for i_chapter in i_case.chapter_set.all()}
                if all([ int(j_vol) in vol_list_i_case for j_vol in vol_list]):
                    tmp.add(i_case.number)
            refined_case_number_list.append(tmp)
            
        # 登場人物による絞り込みがあれば当てはまる事件の番号の集合を
        # 集合のリスト refined_case_number_list に登録    
        if chara_list := self.request.POST.getlist('character'):       
            tmp = set()
            for i_case in Case.objects.all():
                chara_list_i_case = { i_chara.name for i_chapter in i_case.chapter_set.all()\
                     for i_chara in i_chapter.character_set.all()}
                if all([ j_chara in chara_list_i_case for j_chara in chara_list]):
                    tmp.add(i_case.number)
            refined_case_number_list.append(tmp)

        # 事件名による絞り込みがあれば当てはまる事件の番号の集合を
        # 集合のリスト refined_case_number_list に登録    
        if case_name := self.request.POST.get('case_name'):
            case_name_list = case_name.split()
            if not case_name_list:
                pass
            else:
                tmp = set()
                for i, i_case_name in enumerate(case_name_list, 1):
                    if i == 1:
                        tmp = {i_case.number for i_case in Case.objects.filter(name__contains=str(i_case_name))}
                    else:
                        tmp &= {i_case.number for i_case in Case.objects.filter(name__contains=str(i_case_name))}
                refined_case_number_list.append(tmp)
            
        # すべての絞り込みに対して積集合をとり、当てはまるものだけに
        # クエリ検索をかける。
        if refined_case_number_list:
            for i, i_refined_set in enumerate(refined_case_number_list, 1):
                if i == 1:
                    and_refined_set = i_refined_set
                else:
                    and_refined_set &= i_refined_set
            queryset = Case.objects.filter(number__in=and_refined_set)
            
        else :
            queryset = Case.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        form_list = {
            'form1': CaseKindForm(**self.get_form_kwargs()),
            'form2': VolumeForm(**self.get_form_kwargs()),
            'form3': CharaForm(**self.get_form_kwargs()),
            'form4': CaseNameForm(**self.get_form_kwargs())
        }
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
