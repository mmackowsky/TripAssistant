from django import forms

from .models import Reviews


class ReviewForm(forms.ModelForm):
    content = forms.CharField(max_length=500, required=True, error_messages={'required': 'Content is required.'})
    stars = forms.IntegerField(required=True, error_messages={'required': 'Stars are required.'})

    class Meta:
        model = Reviews
        fields = ["content", "stars"]
