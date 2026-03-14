from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.utils import DatabaseError
from django.contrib.auth.hashers import identify_hasher
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import *
import re
import random

# Create your views here.


def signin(request):
    if request.method == "POST":
        context = {
            "email_or_phone": request.POST.get("emailorphone", "").strip(),
            # Preserve password exactly as entered.
            "userPassword": request.POST.get("password", "")
        }

        try:
            user_obj = User.objects.get(
                email__iexact=context["email_or_phone"])
        except User.DoesNotExist:
            try:
                user_obj = User.objects.get(
                    phone_number=context["email_or_phone"])
            except (User.DoesNotExist, ValueError):
                context.setdefault(
                    "message", "E-mail/Phone wrong, Please enter right.")
                return render(request, "LoginPage/login.html", context)

        password_ok = user_obj.check_password(context["userPassword"])

        # Backward compatibility for legacy rows that may still contain
        # plaintext passwords from older code paths.
        if not password_ok and user_obj.password:
            try:
                identify_hasher(user_obj.password)
            except ValueError:
                if context["userPassword"] == user_obj.password:
                    user_obj.set_password(context["userPassword"])
                    user_obj.save(update_fields=["password"])
                    password_ok = True

        if password_ok:
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
            errors.setdefault(
                "fnameissue", "First name must contain letters only.")
        if not data["l_name"].isalpha():
            errors.setdefault(
                "lnameissue", "Last name must contain letters only.")

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
            errors.setdefault(
                "phoneissue", "Enter a valid 10-digit phone number starting with 6-9.")
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
            User.objects.create_user(
                first_name=data["f_name"],
                last_name=data["l_name"],
                email=data["Email"],
                phone_number=data["PhoneNo"],
                password=data["password"],
                role="customer"
            )

            context = {
                "successful": "You'r account is created."
            }
            return render(request, "LoginPage/login.html", context)
        except DatabaseError:
            return HttpResponse("Server issue. Try again later.")
    return render(request, "LoginPage/signup.html")


def singout(request):
    request.session.flush()
    return redirect("core:homepage")


def send_otp(request):
    if request.method == "POST":
        email = request.POST.get("emailorphone", "").strip().lower()

        if not email:
            messages.error(request, "Please enter your registered email.")
            return render(request, "LoginPage/send_otp.html")

        user_exists = User.objects.filter(email=email).first()

        if not user_exists:
            messages.error(request, "No account found with that email.")
            return render(request, "LoginPage/send_otp.html")

        otp = str(random.randint(100000, 999999))
        request.session["reset_otp"] = otp
        request.session["reset_email"] = email

        subject = "PCify_Nexus Auth - Your Password Reset Code"
        plain_message = (
            f"Hello!\n\nYour 6-digit verification code is: {otp}\n\n"
            "Please enter this on the verification page."
        )
        verify_url = request.build_absolute_uri("/accounts/verify-otp/")

        html_message = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f5f7; margin: 0; padding: 40px 20px;">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 500px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; border: 1px solid #e5e7eb; border-top: 5px solid #0ea5e9; overflow: hidden; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);">
            <tr>
                <td style="padding: 35px 35px 15px 35px; text-align: center;">
                    <h2 style="margin: 0; font-size: 26px; font-weight: 800; color: #111827; text-transform: uppercase; letter-spacing: 1px;">
                        PCify_<span style="color: #0ea5e9;">Nexus</span>
                    </h2>
                </td>
            </tr>
            <tr>
                <td style="padding: 0 35px 30px 35px; text-align: center;">
                    <h1 style="color: #1f2937; font-size: 22px; margin-bottom: 12px;">Reset Your Password</h1>
                    <p style="color: #4b5563; font-size: 15px; line-height: 1.6; margin-bottom: 35px;">
                        We received a request to reset the password for your account. Here is your code:
                    </p>
                    <table align="center" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 250px;">
                        <tr>
                            <td style="background-color: #f0f9ff; border: 2px dashed #bae6fd; padding: 20px; border-radius: 10px; text-align: center;">
                                <span style="font-family: 'Courier New', Courier, monospace; font-size: 32px; font-weight: 800; letter-spacing: 6px; color: #0369a1;">
                                    {otp}
                                </span>
                            </td>
                        </tr>
                    </table>
                    <br>
                    <table align="center" cellpadding="0" cellspacing="0" style="margin-bottom: 30px;">
                        <tr>
                            <td align="center" style="border-radius: 8px; background-color: #0ea5e9; box-shadow: 0 4px 6px rgba(14, 165, 233, 0.25);">
                                <a href="{verify_url}" target="_blank" style="font-size: 16px; font-weight: 600; font-family: 'Segoe UI', sans-serif; color: #ffffff; text-decoration: none; padding: 14px 32px; display: inline-block; border-radius: 8px;">
                                    Enter Code Here
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, "Verification code sent to your email.")
            return redirect("accounts:verify_otp")
        except Exception:
            messages.error(
                request, "Error sending email. Check SMTP settings.")
            return render(request, "LoginPage/send_otp.html")

    return render(request, "LoginPage/send_otp.html")


def verify_otp(request):
    if "reset_otp" not in request.session:
        messages.error(request, "Please request an OTP first.")
        return redirect("accounts:send_otp")

    if request.method == "POST":
        entered_otp = request.POST.get("otp", "").strip()
        saved_otp = request.session.get("reset_otp")

        if entered_otp == saved_otp:
            request.session["otp_verified"] = True
            messages.success(request, "OTP verified successfully.")
            return redirect("accounts:change_password")

        messages.error(request, "Incorrect OTP. Please try again.")
        return redirect("accounts:verify_otp")

    return render(request, "LoginPage/verify_otp.html")


def change_password(request):
    if not request.session.get("otp_verified"):
        messages.error(request, "Please verify OTP before changing password.")
        return redirect("accounts:send_otp")

    if request.method == "POST":
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "LoginPage/changepassword.html")

        email = request.session.get("reset_email")
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(
                request, "Account not found. Please retry password reset.")
            return redirect("accounts:send_otp")

        # Disallow reusing the current password. Handle both hashed and
        # legacy-plaintext stored passwords.
        is_same = False
        if user.password:
            try:
                identify_hasher(user.password)
                # password is hashed
                is_same = user.check_password(new_password)
            except Exception:
                # legacy plaintext stored
                is_same = (new_password == user.password)

        if is_same:
            messages.error(
                request, "Please enter a new password different from the current one.")
            return render(request, "LoginPage/changepassword.html")

        user.set_password(new_password)
        user.save()

        request.session.pop("reset_otp", None)
        request.session.pop("reset_email", None)
        request.session.pop("otp_verified", None)

        messages.success(
            request, "Password reset successfully. Please sign in.")
        return redirect("accounts:signin")

    return render(request, "LoginPage/changepassword.html")
