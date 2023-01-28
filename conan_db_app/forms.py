from django import forms
from .models import Question, CaseKind

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['jenre', 'kind','content','n_option','option1','option2','option3','option4','option5']

    def clean_option1(self):
        option1 = self.cleaned_data["option1"]
        option1_min = 10
        if len(option1) < option1_min:
            raise forms.ValidationError(f'{option1_min}文字以上入力してください。')
        
        return option1    

class RefineQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['jenre', 'kind']
        widgets = {
            'kind': forms.RadioSelect(),
            'jenre': forms.RadioSelect()
        }

class WithEventForm(forms.Form):
    with_event = forms.BooleanField(label='重要なイベントのみを表示する', required=False)

class WithEventForm2(forms.Form):
    with_event2 = forms.BooleanField(label='重要なイベントのみを表示する', required=False)

class CaseKindForm(forms.Form):
    CASE_KIND = [(i_kind.name, i_kind.name) for i_kind in CaseKind.objects.all()]
    fields = forms.MultipleChoiceField(choices=CASE_KIND, required=False,\
        widget=forms.CheckboxSelectMultiple())