from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserForm
from django.views.generic.edit import FormView
from .utils import add_location
from .models import LocationData


# Create your views here.
class DashboardView(FormView):
    template_name = 'dashboard.html'
    form_class = UserForm

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        context = {
            'form_class': form_class
        }
        location_data = LocationData.objects.filter(email_address=request.session['email_address'])
        for data in location_data:
            print(data.latitutde, data.longitude, data.timestamp)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            location = form.cleaned_data['location']
            add_location(request, location)
            return HttpResponseRedirect("/dashboard")
        else:
            return render(request, self.template_name)
