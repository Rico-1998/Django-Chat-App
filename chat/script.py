from django.shortcuts import render
from django.contrib.auth.models import User


def check_for_user(request):
    if request.method == 'POST' and not User.objects.filter(
            username=request.POST.get('username')).exists():
        return True
    else:
        print('user already exists')


def check_for_mail(request):
    if request.method == 'POST' and not User.objects.filter(
            email=request.POST.get('email')).exists():
        return True
    else:
        print('email already exists')
