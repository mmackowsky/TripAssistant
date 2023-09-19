from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.views.generic.edit import FormView

from locations.models import Location

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
            Images.objects.create(
                image=each, location_id=location_id, uploaded_by=uploaded_by
            )
        return super(MultiUploadView, self).form_valid(form)
