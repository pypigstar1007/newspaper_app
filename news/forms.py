from django import forms
from .models import News

class NewsForms(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'headline', 'news_body', 'category')
        widgets={
                   "title":forms.TextInput(attrs={'placeholder':'enter title','class':'form-control'}),
                   "headline":forms.TextInput(attrs={'placeholder':'enter headline','class':'form-control'}),
                   "news_body":forms.Textarea(attrs={'placeholder':'enter news body','class':'form-control'}),
                #    "category":forms.ChoiceField(),
                }  

