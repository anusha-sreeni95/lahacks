from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserForm
from django.views.generic.edit import FormView
from .utils import add_location
from .models import LocationData
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
class DashboardView(FormView):
    template_name = 'dashboard.html'
    form_class = UserForm

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        location_data = LocationData.objects.filter(email_address=request.session['email_address'])
        context = {
            'form_class': form_class,
            'locations': json.dumps(list(location_data.values("latitutde", "longitude", "timestamp")))
        }
        for data in location_data:
            print(data.latitutde, data.longitude, data.timestamp)
        return render(request, self.template_name, context=context)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        location = json.loads(request.body.decode('utf-8'))
        add_location(request, location["latitude"], location["longitude"], location["timestamp"])
        return HttpResponseRedirect("/dashboard")
