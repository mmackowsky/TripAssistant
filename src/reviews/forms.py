from django import forms
from .models import Reviews


class ReviewForm(forms.ModelForm):
    content = forms.CharField(max_length=500)

    class Meta:
        model = Reviews
        fields = ['content']
