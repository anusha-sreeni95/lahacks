from django.conf.urls import url, include
from .views import HomePageView

urlpatterns = [
  url("^$", HomePageView.as_view(), name="homepageview")
]
