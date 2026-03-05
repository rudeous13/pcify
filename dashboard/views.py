from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, "staff_profile"):
            return redirect("dashboard:admin_login")
        return view_func(request, *args, **kwargs)

    return _wrapped


@staff_required
def dashboard_home_view(request):
    return render(request, 'dashboard/home.html')


def admin_login_view(request):
    if request.user.is_authenticated and hasattr(request.user, "staff_profile"):
        return redirect("dashboard:home")

    context = {}
    if request.method == "POST":
        email = request.POST.get("email", request.POST.get("username", "")).strip().lower()
        password = request.POST.get("password", "")

        if not email or not password:
            context["error"] = "Email and password are required."
            return render(request, "dashboard/admin_login.html", context)

        user = authenticate(request, email=email, password=password)
        if user is None or not hasattr(user, "staff_profile"):
            context["error"] = "Invalid staff credentials."
            return render(request, "dashboard/admin_login.html", context)

        login(request, user)
        if not request.POST.get("remember"):
            request.session.set_expiry(0)
        return redirect("dashboard:home")

    return render(request, 'dashboard/admin_login.html')


@staff_required
def analytics_view(request):
    return render(request, 'dashboard/analytics.html')


@staff_required
def brands_view(request):
    return render(request, 'dashboard/brands.html')


@staff_required
def categories_view(request):
    return render(request, 'dashboard/categories.html')


@staff_required
def compatibility_view(request):
    return render(request, 'dashboard/compatibility.html')


@staff_required
def customers_view(request):
    return render(request, 'dashboard/customers.html')


@staff_required
def employee_management_view(request):
    return render(request, 'dashboard/employee_management.html')


@staff_required
def employees_view(request):
    return render(request, 'dashboard/employees.html')


@staff_required
def inventory_view(request):
    return render(request, 'dashboard/inventory.html')


@staff_required
def orders_view(request):
    return render(request, 'dashboard/orders.html')


@staff_required
def prebuilt_pc_view(request):
    return render(request, 'dashboard/prebuilt_pc.html')


@staff_required
def products_view(request):
    return render(request, 'dashboard/products.html')


@staff_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')


@staff_required
def suppliers_view(request):
    return render(request, 'dashboard/suppliers.html')


@staff_required
def trending_view(request):
    return render(request, 'dashboard/trending.html')


def logout_view(request):
    logout(request)
    return redirect('dashboard:admin_login')
