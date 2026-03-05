from django.shortcuts import render

def dashboard_home_view(request):
    return render(request, 'dashboard/home.html')

def admin_login_view(request):
    return render(request, 'dashboard/admin_login.html')

def analytics_view(request):
    return render(request, 'dashboard/analytics.html')

def brands_view(request):
    return render(request, 'dashboard/brands.html')

def categories_view(request):
    return render(request, 'dashboard/categories.html')

def compatibility_view(request):
    return render(request, 'dashboard/compatibility.html')

def customers_view(request):
    return render(request, 'dashboard/customers.html')

def employee_management_view(request):
    return render(request, 'dashboard/employee_management.html')

def employees_view(request):
    return render(request, 'dashboard/employees.html')

def inventory_view(request):
    return render(request, 'dashboard/inventory.html')

def orders_view(request):
    return render(request, 'dashboard/orders.html')

def prebuilt_pc_view(request):
    return render(request, 'dashboard/prebuilt_pc.html')

def products_view(request):
    return render(request, 'dashboard/products.html')

def settings_view(request):
    return render(request, 'dashboard/settings.html')

def suppliers_view(request):
    return render(request, 'dashboard/suppliers.html')

def trending_view(request):
    return render(request, 'dashboard/trending.html')
