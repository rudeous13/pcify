from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pc/', views.pc_view, name='pc'),
    path('prebuilt/', views.prebuilt_view, name='prebuilt'),
    path('accessories/', views.accessories_view, name='accessories'),
]
