from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Default page for when first call
def homepage(request):
  return render(request, "Home/home.html")