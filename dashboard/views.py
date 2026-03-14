from django.contrib.auth import authenticate, login, logout
from .decorators import admin_required
# from account.models import *
# from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.db.utils import DatabaseError
from datetime import datetime
from django.utils import timezone
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
  user_list = Customer.objects.select_related('user').all()
  return render(request, "AdminPage/admin_customer.html", {"user_list": user_list})


# --------------------------------------
# 👤 Users Section
# 👨‍💻 Employee
# --------------------------------------
@admin_required
def dashboard_employees(request):
  context = {
  "employees" : Staff.objects.select_related('user').all(),
  }
  if request.method == "POST":
    action = request.POST.get("action")

    if action == "insert":
      data = {
        "f_name": request.POST.get("first_name"),
        "l_name": request.POST.get("last_name"),
        "Email": request.POST.get("employee_email"),
        "PhoneNo": request.POST.get("employee_phone_no"),
        "password": request.POST.get("employe_password"),
        "jod": request.POST.get("employee_join_date"),
        "address": request.POST.get("employee_address"),
        "image": request.FILES.get("image")
      }
      
      errors = {}

      # -------------------- NAME VALIDATION --------------------
      if not data["f_name"].isalpha():
        errors.setdefault("fnameissue", "First name must contain letters only.")
      if not data["l_name"].isalpha():
        errors.setdefault("lnameissue", "Last name must contain letters only.")

      # -------------------- EMAIL VALIDATION --------------------
      email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
      if not re.match(email_pattern, data["Email"]):
        errors.setdefault("emailissue", "Enter a valid email address.")
      else:
        allowed_domains = [
          "gmail.com", 
          "yahoo.com",
          "outlook.com", 
          "hotmail.com",
        ]
        domain = data["Email"].split("@")[-1].lower()
        if domain not in allowed_domains:
            errors.setdefault("emailissue", "Email domain not allowed.")

      # -------------------- PHONE VALIDATION --------------------
      phone_pattern = r'^[6-9]\d{9}$'
      if not re.match(phone_pattern, data["PhoneNo"]):
        errors.setdefault("phoneissue", "Enter a valid 10-digit phone number starting with 6-9.")
      elif User.objects.filter(phone=data["PhoneNo"]).exists():
          errors.setdefault("phoneissue", "Phone number is already used.")

      # -------------------- EMAIL UNIQUENESS --------------------
      if User.objects.filter(email=data["Email"]).exists():
        errors.setdefault("emailissue", "E-mail address is already used.")

      # -------------------- DATE VALIDATION --------------------
      try:
          user_date = datetime.strptime(data["jod"], "%Y-%m-%d").date()
          today = timezone.now().date()

          if user_date > today:
              errors.setdefault("dateissue", "Date cannot be in the future.")
      except ValueError:
          errors.setdefault("dateissue", "Invalid date format.")

      # -------------------- RETURN ERRORS IF ANY --------------------
      if errors:
        context.setdefault("errors", errors)
        return render(request, "AdminPage/admin_employee.html", context)

      # -------------------- CREATE User --------------------
      try:
        user = User.objects.create(
          first_name=data["f_name"],
          last_name=data["l_name"],
          email=data["Email"],
          phone=data["PhoneNo"],
          password=data["password"],  
          role=Role.objects.get(role='employee'),
          profile_image = data["image"]
        )

        Staff.objects.create(
          user=user,
          jod=data["jod"]
        )
        context.setdefault("successful", "account is added.")
        return render(request, "AdminPage/admin_employee.html", context)
      except DatabaseError:
        context.setdefault("errors", "account is not added.")
        return render(request, "AdminPage/admin_employee.html", context)
      
    elif action == "update":
      return render(request, "AdminPage/admin_products.html")

    elif action == "delete":
      User.objects.filter(user_id = request.POST.get("emp_id")).delete()
      context.setdefault("errors", "Account has deleted.")
      return render(request, "AdminPage/admin_employee.html", context)
      
    
  return render(request, "AdminPage/admin_employee.html", context)


# --------------------------------------
# 👤 Users Section
# 👨 Supplier
# --------------------------------------
@admin_required
def dashboard_suppliers(request):
  context = {
    "suppliers" : Suppliers.objects.all(),
  }
  if request.method == "POST":
    action = request.POST.get("action") 

    if action == "insert":
      data = {
        "name": request.POST.get("owner_name"),
        "C_name": request.POST.get("company_name"),
        "phone": request.POST.get("sup_mobilenum"),
        "email": request.POST.get("sup_email"),
        "gstNumber": request.POST.get("gst_number"),
      }

      try: 
        Suppliers.objects.create(
          supplier_name = data["name"],
          company_name = data["C_name"],
          phone_number = data["phone"],
          email = data["email"],
          gst_number = data["gstNumber"],
        )

        context.setdefault("successful", "account is added.")
        return render(request, "AdminPage/admin_supplier.html", context)
      except:
        return render(request, "AdminPage/admin_supplier.html", context)
      
    if action == "delete":
      Suppliers.objects.get(supplier_id = request.POST.get("sup_id")).delete()
      context.setdefault("errors", "Account has deleted.")
      return render(request, "AdminPage/admin_supplier.html", context)

      

  return render(request, "AdminPage/admin_supplier.html", context)


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