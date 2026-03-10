from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('overview/', views.profile_overview_view, name='profile_overview'),
    path('my-builds/', views.profile_my_builds_view, name='profile_my_builds'),
    path('order-history/', views.profile_order_history_view,
         name='profile_order_history'),
    path('security/', views.profile_security_view, name='profile_security'),
    path('settings/', views.profile_settings_view, name='profile_settings'),
]
