from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from .forms import ImageForm
from locations.models import Location


# Create your views here.
@login_required()
def add_image(request, location_id):
    location = Location.objects.get(id=location_id)
    if request.method == "POST":
        image_form = ImageForm(request.POST, request.FILES)

        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.uploaded_by = request.user.profile
            image.location = location
            image.save()
            messages.info(request, "Image added.")
            return redirect('add_image', location_id=location_id)
    else:
        image_form = ImageForm()

    return render(request, 'locations_images/add_image.html', {
        'form': image_form,
        'location_name': location.location_name
    })
