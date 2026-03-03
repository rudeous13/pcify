from django.contrib.auth import authenticate, login, logout
from .decorators import admin_required
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.db.utils import DatabaseError
import re
# Create your views here.
def is_admin(user):
  return user.is_authenticated and user.is_staff

# 👑 Admin login page
# ------------------------------------
def admin_login(request):
  if request.user.is_authenticated and request.user.is_staff:
    return HttpResponseRedirect("dashboard/")
  
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)

    if user and user.is_staff:
      login(request, user)
      return HttpResponseRedirect("dashboard/")
    else :
      message = {"error": "Invalide name and password."}
      return render(request, "AdminPage/admin_login.html", message)
      
  return render(request, "AdminPage/admin_login.html")

# --------------------------------------
# Mainmenu Section
# 🏠 dashboard of admin
# --------------------------------------
@admin_required
def dashboard_home(request): 
  return render(request, "AdminPage/admin_home.html")

# --------------------------------------
# 👤 Users Section
# 👥 customers
# --------------------------------------
@admin_required
def dashboard_customers(request):
  return render(request, "AdminPage/admin_customer.html")


# --------------------------------------
# 👤 Users Section
# 👨‍💻 Employee
# --------------------------------------
@admin_required
def dashboard_employees(request):
  return render(request, "AdminPage/admin_employee.html")


# --------------------------------------
# 👤 Users Section
# 👨 Supplier
# --------------------------------------
@admin_required
def dashboard_suppliers(request):
  return render(request, "AdminPage/admin_supplier.html")


# --------------------------------------
# 🧩 Managemet Section
# 💻💻 Product
# --------------------------------------
@admin_required
def dashboard_product(request):
  return render(request, "AdminPage/admin_products.html")


# --------------------------------------
# 🧩 Managemet Section
# 🍎🍎 dashboard of brand
# --------------------------------------
@admin_required
def dashboard_brand(request):
  if request.method == "POST":
    action = request.POST.get("action")

    if action == "insert":
      brand_name = request.POST.get("brand_name")
      if brand_name:
        Brand.objects.create(brand_name = brand_name)

    elif action == "delete":
      Brand.objects.filter(brand_id = request.POST.get("brand_id")).delete()

    elif action == "update":
      brand_id = request.POST.get("brand_id")
      brand_name = request.POST.get("brand_name")

      Brand.objects.filter(brand_id = brand_id).update(brand_name = brand_name)

    return redirect("dashboard:brand")

  brand_list = Brand.objects.all()
  return render(request, "AdminPage/admin_brand.html", {"brand_list": brand_list})


# --------------------------------------
# 🧩 Managemet Section
# 📄📄 Category
# --------------------------------------
@admin_required
def dashboard_category(request):
  if request.method == "POST":
    action = request.POST.get("action")

    if action == "insert":
      category_name = request.POST.get("category_name")
      if category_name:
        Category.objects.create(category_name = category_name)
    elif action == "delete":
      Category.objects.filter(category_id = request.POST.get("category_id")).delete()

    elif action == "update":
      category_id = request.POST.get("category_id")
      category_name = request.POST.get("category_name")

      Category.objects.filter(category_id = category_id).update(category_name = category_name)
    return redirect("dashboard:category")
  
  category_list = Category.objects.all().order_by("category_id")
  return render(request, "AdminPage/admin_category.html", {"category_list": category_list})


# --------------------------------------
# 🧩 Managemet Section
# 📦📦 Order
# --------------------------------------
@admin_required
def dashboard_order(request):
  return render(request, "AdminPage/admin_order.html")


# --------------------------------------
# 🧩 Managemet Section
# 🗄️🗄️ Task management
# --------------------------------------
@admin_required
def dashboard_task(request):
  return render(request, "AdminPage/admin_emp_management.html")


# --------------------------------------
# 🧩 Managemet Section
# 📥📥  Inventory management
# --------------------------------------
@admin_required
def dashboard_inventory(request):
  return render(request, "AdminPage/admin_inventory.html")


# --------------------------------------
# 🧩 Managemet Section
# ⑇⑇  Compatibility management
# --------------------------------------
@admin_required
def dashboard_compatibility(request):
  return render(request, "AdminPage/admin_compatibility.html")


# --------------------------------------
# 🧩 Managemet Section
# 💹💹 Trenging 
# --------------------------------------
@admin_required
def dashboard_trending(request):
  return render(request, "AdminPage/admin_trending.html")


# --------------------------------------
# 🧩 Managemet Section
# ⚒️⚒️ per_built
# --------------------------------------
@admin_required
def dashboard_per_built(request):
  return render(request, "AdminPage/admin_prebuiltpc.html")


# --------------------------------------
# 🧩 System Section
# 📊 Analytic
# --------------------------------------
@admin_required
def admin_analytic(request):
  return render(request, "AdminPage/admin_analytic.html")


# --------------------------------------
# 🧩 System Section
# ⚙️ Setting
# --------------------------------------
@admin_required
def admin_setting(request):
  return render(request, "AdminPage/admin_setting.html")


# --------------------------------------
# 🧩 System Section
# 📵 Admin logout view
# --------------------------------------
@admin_required
def admin_logout(request):
  logout(request)
  return render(request, "AdminPage/admin_login.html")