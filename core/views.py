from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Default page for when first call
def homepage(request):
  return render(request, "Home/home.html")

def prebuilt(request):
  return render(request, "Home/prebuilt.html")

def built(request):
  return render(request, "Home/pc.html")

def profile(request):
  return render(request, "Home/pro_overview.html")

def pro_builds(request):
  return render(request, "Home/pro_my_builds.html")

def pro_order(request):
  return render(request, "Home/pro_order_history.html")

def pro_security(request):
  return render(request, "Home/pro_security.html")

def pro_setting(request):
  return render(request, "Home/pro_settings.html")

