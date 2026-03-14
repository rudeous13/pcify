from django.urls import path
from .views import *

# App name
app_name = "accounts"

# All urls of core app
urlpatterns = [
    path('signin/', signin, name="signin"),
    path('signup/', signup, name="signup"),
    path('signout/', singout, name="singout"),
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('change-password/', change_password, name='change_password'),
]
