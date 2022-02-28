from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileCreateForm
from .models import Profile, Conversation, Message


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('inbox')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('inbox')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'messaging/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('inbox')

def registerUserPage(request):
    form = ProfileCreateForm()

    if request.method == 'POST':
        form = ProfileCreateForm(request.POST)
        if form.is_valid():
            user, profile = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            profile.save()
            login(request, user)
            return redirect('inbox')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'messaging/login_register.html', {'form': form})

def inbox(request):
    messages = Message.objects.filter(conversation__members__in=[request.user.id])
    context = {'messages':messages}
    return render(request, 'messaging/inbox.html', context)

def sendMessage(request):
    context = {}
    return render(request, 'messaging/send_message.html', context)

def conversation(request, pk):
    context = {}
    return render(request, 'messaging/conversation.html', context)
