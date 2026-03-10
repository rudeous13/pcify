from django.shortcuts import render


def profile_overview_view(request):
    return render(request, 'profile/overview.html')


def profile_my_builds_view(request):
    return render(request, 'profile/my_builds.html')


def profile_order_history_view(request):
    return render(request, 'profile/order_history.html')


def profile_security_view(request):
    return render(request, 'profile/security.html')


def profile_settings_view(request):
    return render(request, 'profile/settings.html')
