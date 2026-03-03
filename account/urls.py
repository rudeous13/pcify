from django.urls import path
from .views import *

#App name
app_name = "account"

# All urls of core app
urlpatterns = [
  path('signin/', signin, name="signin"),
  path('signup/', signup, name="signup")
]