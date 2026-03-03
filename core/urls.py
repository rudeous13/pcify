# Import file or packages
from django.urls import path
from . import views

# App name
app_name = "core"

# All urls of core app
urlpatterns = [
  path('', views.homepage, name="homepage"),
]