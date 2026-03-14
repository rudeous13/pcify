# Import file or packages
from django.urls import path
from . import views

# App name
app_name = "core"

# All urls of core app
urlpatterns = [
  path('', views.homepage, name="homepage"),
  path('prebuilt', views.prebuilt, name="prebuilt"),
  path('built', views.built, name="built"),
  path('profile', views.profile, name="profile"),


  path('profile/builds/', views.pro_builds, name="pro_builds"),
  path('profile/order', views.pro_order, name="pro_order"),
  path('profile/security', views.pro_security, name="pro_security"),
  path('profile/setting', views.pro_setting, name="pro_setting")
]