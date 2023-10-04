import logging

import boto3
from django.conf import settings
from django.contrib import messages
from django.views.generic.edit import FormView

from src.locations.models import Location

from .forms import MultiUploadForm
from .models import Images


class MultiUploadView(FormView):
    template_name = "locations_images/add_image.html"
    form_class = MultiUploadForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_id = self.kwargs.get("location_id")
        if location_id:
            location = Location.objects.get(pk=location_id)
            images = Images.objects.filter(location=location)

            context["location"] = location
            context["images"] = images

        return context

    def form_valid(self, form):
        for each in form.cleaned_data["attachments"]:
            location_id = self.kwargs["location_id"]
            uploaded_by = self.request.user.profile

            # Sending to S3
            s3 = boto3.client("s3")
            file_name = each.name
            s3.upload_fileobj(each, settings.AWS_STORAGE_BUCKET_NAME, file_name)
            logging.debug("File saved to S3.")

            Images.objects.create(
                image=file_name, location_id=location_id, uploaded_by=uploaded_by
            )
            messages.success(self.request, "Successful upload!")
        return super(MultiUploadView, self).form_valid(form)
