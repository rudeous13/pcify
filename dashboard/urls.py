from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home_view, name='home'),
    path('', views.dashboard_home_view, name='dashboard_home'),
    path('login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('analytics/', views.analytics_view, name='analytic'),
    path('brands/', views.brands_view, name='brands'),
    path('brands/', views.brands_view, name='brand'),
    path('categories/', views.categories_view, name='categories'),
    path('categories/', views.categories_view, name='category'),
    path('compatibility/', views.compatibility_view, name='compatibility'),
    path('customers/', views.customers_view, name='customers'),
    path('employee-management/', views.employee_management_view,
         name='employee_management'),
    path('employee-management/', views.employee_management_view, name='task'),
    path('employees/', views.employees_view, name='employees'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/', views.orders_view, name='order'),
    path('prebuilt-pc/', views.prebuilt_pc_view, name='prebuilt_pc'),
    path('prebuilt-pc/', views.prebuilt_pc_view, name='pre_built'),
    path('products/', views.products_view, name='products'),
    path('products/', views.products_view, name='product'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/', views.settings_view, name='setting'),
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('trending/', views.trending_view, name='trending'),
]
