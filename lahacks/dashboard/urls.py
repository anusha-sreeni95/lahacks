from django.conf.urls import url
from .views import DashboardView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
  url("^$", csrf_exempt(DashboardView.as_view()), name="dashboardview")
]
