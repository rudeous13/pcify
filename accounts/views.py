from django.contrib.auth import authenticate, get_user_model, login
from django.db import IntegrityError
from django.shortcuts import redirect, render

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated and request.user.role == User.Roles.CUSTOMER:
        return redirect("home")

    context = {}
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        context["email"] = email

        if not email or not password:
            context["message"] = "Email and password are required."
            return render(request, "accounts/login.html", context)

        user = authenticate(request, email=email, password=password)
        if user is None:
            context["message"] = "Invalid email or password."
            return render(request, "accounts/login.html", context)

        if user.role != User.Roles.CUSTOMER:
            context["message"] = "Customer account not found for this user."
            return render(request, "accounts/login.html", context)

        login(request, user)
        if not request.POST.get("remember"):
            request.session.set_expiry(0)
        return redirect("home")

    return render(request, "accounts/login.html", context)


def signup_view(request):
    if request.user.is_authenticated and request.user.role == User.Roles.CUSTOMER:
        return redirect("home")

    context = {}
    if request.method == "POST":
        first_name = request.POST.get("firstname", "").strip()
        last_name = request.POST.get("lastname", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone_number = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirmpassword", "")

        context.update(
            {
                "f_name": first_name,
                "l_name": last_name,
                "Email": email,
                "PhoneNo": phone_number,
            }
        )

        has_error = False
        if not first_name:
            context["fnameissue"] = "First name is required."
            has_error = True
        if not last_name:
            context["lnameissue"] = "Last name is required."
            has_error = True
        if not email:
            context["emailissue"] = "Email is required."
            has_error = True
        elif User.objects.filter(email=email).exists():
            context["emailissue"] = "Email already registered."
            has_error = True
        if not phone_number:
            context["phoneissue"] = "Phone number is required."
            has_error = True
        if not password:
            context["message"] = "Password is required."
            has_error = True
        elif password != confirm_password:
            context["message"] = "Passwords do not match."
            has_error = True

        if has_error:
            return render(request, "accounts/signup.html", context)

        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                role=User.Roles.CUSTOMER,
            )
        except IntegrityError:
            context["emailissue"] = "Unable to create account with these details."
            return render(request, "accounts/signup.html", context)

        login(request, user)
        return redirect("home")

    return render(request, "accounts/signup.html", context)
