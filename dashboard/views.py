from django.contrib.auth import authenticate, login, logout
from .decorators import admin_required
from accounts.models import *
from locations.models import *
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
  user_list = User.objects.filter(role="customer")
  return render(request, "AdminPage/admin_customer.html", {"user_list": user_list})


# --------------------------------------
# 👤 Users Section
# 👨‍💻 Employee
# --------------------------------------
@admin_required
def dashboard_employees(request):
  context = {
  "employees": User.objects.filter(role="employee").prefetch_related('addresses__pincode'),
  }
  if request.method == "POST":
    action = request.POST.get("action")
    data = {
      "f_name": request.POST.get("first_name"),
      "l_name": request.POST.get("last_name"),
      "Email": request.POST.get("employee_email"),
      "PhoneNo": request.POST.get("employee_phone_no"),
      "password": request.POST.get("employe_password"),
      "image": request.FILES.get("image"),
      "street_address": request.POST.get("street_address"),
      "area_name": request.POST.get("area_name"),
      "pincode": request.POST.get("pincode"),
    }
    if action == "insert":
      
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
      elif User.objects.filter(phone_number=data["PhoneNo"]).exists():
          errors.setdefault("phoneissue", "Phone number is already used.")

      # -------------------- EMAIL UNIQUENESS --------------------
      if User.objects.filter(email=data["Email"]).exists():
        errors.setdefault("emailissue", "E-mail address is already used.")

      # ---------------- PINCODE VALIDATION ----------------
      if not re.match(r'^\d{6}$', data["pincode"]):
        errors["pincodeissue"] = "Pincode must be 6 digits."

      # ---------------- AREA NAME VALIDATION ----------------
      if not re.match(r'^[A-Za-z\s]+$', data["area_name"]):
        errors["areaissue"] = "Area name must contain alphabets only."

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
          phone_number=data["PhoneNo"],
          password=data["password"],  
          role='employee',
          profile_image = data["image"]
        )

        # ---------------- PINCODE CHECK ----------------
        pincode_obj = Pincode.objects.filter(pincode=data["pincode"]).first()

        if not pincode_obj:
            pincode_obj = Pincode.objects.create(
              pincode=data["pincode"],
              area_name=data["area_name"],
              city="Ahmedabad"
            )

        # ---------------- CREATE ADDRESS ----------------
        Address.objects.create(
          user=user,
          address=data["street_address"],
          pincode=pincode_obj,
          is_primary=False
        )

        context.setdefault("successful", "account is added.")
        return render(request, "AdminPage/admin_employee.html", context)
      except DatabaseError:
        context.setdefault("errors", "account is not added.")
        return render(request, "AdminPage/admin_employee.html", context)
      
    elif action == "update":
      emp_id = request.POST.get("emp_id")

      try :
        user = User.objects.get(user_id = emp_id)

        user.first_name = data["f_name"] or user.first_name
        user.last_login = data["l_name"] or user.last_name
        user.email = data["Email"] or user.email
        user.phone_number = data["PhoneNo"] or user.phone_number

        if data["image"]:
          user.profile_image = data["image"]
        
        user.save()

        pincode_obj = Pincode.objects.filter(pincode=data["pincode"]).first()
        if not pincode_obj:
          pincode_obj = Pincode.objects.create(
            pincode = data["pincode"],
            area_name = data["area_name"],
            city = "Ahmedabad"
          )

        address = Address.objects.filter(user=user).first()

        if address:
          address.address = data['street_address']
          address.pincode = data['pincode']
          address.save()
        
        context["successful"] = "Employee updated successfully."

      except Exception:
        context["errors"] = "Employee Update Failed."
        
      return redirect("dashboard:employees")

    elif action == "delete":
      emp_id = request.POST.get("emp_id")
      if emp_id:
          User.objects.filter(user_id=emp_id).delete()
      return redirect("dashboard:employees")
      
    
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