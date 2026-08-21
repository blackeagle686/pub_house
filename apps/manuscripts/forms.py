from django import forms
from .models import Manuscript

class ManuscriptForm(forms.ModelForm):
    class Meta:
        model = Manuscript
        fields = ['author_name', 'email', 'phone_number', 'title', 'idea', 'cover', 'file']
        widgets = {
            'idea': forms.Textarea(attrs={'rows': 4, 'placeholder': 'اكتب ملخصاً وافياً عن فكرة الكتاب...'}),
        }
