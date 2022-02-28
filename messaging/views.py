from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileCreateForm
from .models import Profile
from django.db.models import Count


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
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
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'messaging/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


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
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'messaging/login_register.html', {'form': form})


def home(request):
    context = {}
    return render(request, 'messaging/home.html', context)

def leaderboard(request):
    user_points = Profile.objects.values('points', 'user', 'displayPoints').order_by('-points')[:10]
    user_names = []
    points = []
    for obj in user_points:
        if obj['displayPoints'] == True:
            user = obj['user']
            point = obj['points']
            points.append(point)
            user_names.append(User.objects.get(id = user).get_full_name())
    user_data = zip(user_names, points)
    #name_users = []
    #for user in users:
    #    new_user = Profile.objects.get(user = 1)    
    #    name_users.append(new_user)
    context = {'users': user_data}
    return render(request, 'messaging/leaderboard.html', context)