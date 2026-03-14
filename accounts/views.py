from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.utils import DatabaseError
from django.contrib.auth.hashers import check_password
from .models import *
import re

# Create your views here.
def signin(request):
  if request.method == "POST":
    context = {
      "email_or_phone" : request.POST.get("emailorphone", "").strip(),
      "userPassword" : request.POST.get("password", "").strip()
    }

    try :
      user_obj = User.objects.get(email = context["email_or_phone"])
    except User.DoesNotExist : 
      try :
        user_obj = User.objects.get(phone_number = context["email_or_phone"])
      except (User.DoesNotExist, ValueError) :
        context.setdefault("message","E-mail/Phone wrong, Please enter right.")
        return render(request, "LoginPage/login.html", context)
    
    if check_password(context["userPassword"], user_obj.password):
      request.session['user_id'] = user_obj.user_id
      request.session['user_name'] = user_obj.first_name
      request.session['user_lname'] = user_obj.last_name
      request.session['active'] = user_obj.is_active
      return render(request, "Home/home.html")
    else:
      context["message"] = "Invalid password."
      return render(request, "LoginPage/login.html", context)


  return render(request, "LoginPage/login.html")

def signup(request):
  if request.method == "POST":
    # Tack data from form(web page) 
    data = {
      "f_name": request.POST.get("firstname", "").strip(),
      "l_name": request.POST.get("lastname", "").strip(),
      "Email": request.POST.get("email", "").strip().lower(),
      "PhoneNo": request.POST.get("phone", "").strip(),
      "password": request.POST.get("password", "")
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
    elif User.objects.filter(phone_number=data["PhoneNo"]).exists():
        errors.setdefault("phoneissue", "Phone number is already used.")

    # -------------------- EMAIL UNIQUENESS --------------------
    if User.objects.filter(email=data["Email"]).exists():
      errors.setdefault("emailissue", "E-mail address is already used.")

    # -------------------- RETURN ERRORS IF ANY --------------------
    if errors:
      context = {**data, **errors}
      return render(request, "LoginPage/signup.html", context)

    # -------------------- CREATE User --------------------
    try:
      user = User.objects.create(
        first_name=data["f_name"],
        last_name=data["l_name"],
        email=data["Email"],
        phone_number=data["PhoneNo"],
        password=data["password"],  
        role="customer"
      )

      context = {
        "successful" : "You'r account is created."
      }
      return render(request, "LoginPage/login.html", context)
    except DatabaseError:
      return HttpResponse("Server issue. Try again later.")
  return render(request, "LoginPage/signup.html")

def singout(request):
  request.session.flush()
  return redirect("core:homepage")