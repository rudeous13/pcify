from django.shortcuts import render


def home_view(request):
    return render(request, 'home/home.html')


def pc_view(request):
    return render(request, 'home/pc.html')


def prebuilt_view(request):
    return render(request, 'home/prebuilt.html')


def accessories_view(request):
    return render(request, 'home/accessories.html')
