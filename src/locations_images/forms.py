from django import forms
from multiupload.fields import MultiImageField

from .models import Images


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ["image"]


class MultiUploadForm(forms.Form):
    attachments = MultiImageField(min_num=1, max_num=3, max_file_size=1024 * 1024 * 5)

    class Meta:
        model = Images
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super(MultiUploadForm, self).__init__(*args, **kwargs)
        self.fields["attachments"].validators = []
