from django.conf.urls import url
from .views import SignUpView


urlpatterns = [
  url("^$", SignUpView.as_view(), name="signupview")
]
