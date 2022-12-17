from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['kind','content','n_option','option1','option2','option3','option4','option5']

    def clean_option1(self):
        option1 = self.cleaned_data["option1"]
        option1_min = 10
        if len(option1) < option1_min:
            raise forms.ValidationError(f'{option1_min}文字以上入力してください。')
        
        return option1    
