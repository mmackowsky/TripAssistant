from django import forms

from .models import Reviews


class ReviewForm(forms.ModelForm):
    content = forms.CharField(max_length=500)
    stars = forms.IntegerField()

    class Meta:
        model = Reviews
        fields = ["content", "stars"]
