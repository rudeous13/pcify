# Import file or packages
from django.urls import path
from .views import *

# App name
app_name = "dashboard"

# All urls of dashboard app
urlpatterns = [
  # Admin login and Admin dashboard url patterns
  # Admin Login 
  path('', admin_login, name='admin_login'),

  # Mainmenu
  path('dashboard/', dashboard_home, name='dashboard_home'),

  # User
  path('customers/', dashboard_customers, name='customers'),
  path('employees/', dashboard_employees, name='employees'),
  path('suppliers/', dashboard_suppliers, name='suppliers'),

  # Management
  path('product/', dashboard_product, name='product'),
  path('brand/', dashboard_brand, name='brand'),
  path('category/', dashboard_category, name='category'),
  path('order/', dashboard_order, name='order'),
  path('task/', dashboard_task, name='task'),
  path('inventory/', dashboard_inventory, name='inventory'),
  path('compatibility/', dashboard_compatibility, name='compatibility'),
  path('trending/', dashboard_trending, name='trending'),
  path('per-built/', dashboard_per_built, name='pre_built'),

  # System
  path('analytic/', admin_analytic, name="analytic"),
  path('setting/',admin_setting, name="setting"),

  # Logout of admin
  path('logout/', admin_logout, name='logout'),
]