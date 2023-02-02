from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from chat.script import check_for_mail, check_for_user


@login_required(login_url='/login/')
def index(request):
    print(request.method)
    if request.method == 'POST':
        print('received data ' + request.POST['textMessage'])
        myChat = Chat.objects.get(id=1)
        new_Message = Message.objects.create(
            text=request.POST['textMessage'], chat=myChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize(
            'json', [new_Message])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html',  {'messages': chatMessages})


def login_View(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect('/chat/')
            # request.POST.get('redirect')
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})


def register_View(request):
    if check_for_user(request):
        if check_for_mail(request):
            User.objects.create_user(username=request.POST.get('username', None),
                                     email=request.POST.get(
                'email', None),
                password=request.POST.get('password', None), first_name=request.POST.get('username', None))
            return render(request, 'auth/login.html')
        else:
            return render(request, 'auth/register.html')
    else:
        return render(request, 'auth/register.html')
