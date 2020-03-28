from django.conf.urls import url
from .views import LoginView
from .utils import remove_session

urlpatterns = [
  url("^$", LoginView.as_view(), name="loginview"),
  url("^logout$", remove_session, name="logoutview")
]
