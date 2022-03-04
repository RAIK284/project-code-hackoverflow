from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import ProfileCreateForm
from .models import Profile, Message


def login_page(request):
    """View for the user to login."""
    page = 'login'

    if request.user.is_authenticated:
        return redirect('inbox')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Check that the user exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        # Check if the user is authenticated correctly
        if user is not None:
            login(request, user)
            return redirect('inbox')
        else:
            messages.error(request, 'Username or password does not exist.')

    context = {'page': page}
    return render(request, 'messaging/login_register.html', context)

def logout_user(request):
    """Simply logout the current user."""
    logout(request)
    return redirect('inbox')

def register_user_page(request):
    """View for registering a user."""
    form = ProfileCreateForm()

    if request.method == 'POST':
        form = ProfileCreateForm(request.POST)

        if form.is_valid():
            # Save the user/profile information
            user, profile = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            profile.save()

            login(request, user)
            return redirect('inbox')
        else:
            messages.error(request, 'An error occured during user registration.')

    return render(request, 'messaging/login_register.html', {'form': form})

def inbox(request):
    """View for displaying a user's current messages."""
    messages = Message.objects.filter(conversation__members__in=[request.user.id])
    context = {'messages': messages}
    return render(request, 'messaging/inbox.html', context)

def send_message(request):
    context = {}
    return render(request, 'messaging/send_message.html', context)

def conversation(request, pk):
    context = {}
    return render(request, 'messaging/conversation.html', context)

def leaderboard(request):
    """Display a leaderboard of the top points earners on the site."""
    NUM_TO_DISPLAY = 10
    user_points = Profile.objects.values('points', 'user', 'displayPoints').order_by('-points')[:NUM_TO_DISPLAY]
    
    # Collect usernames and associated points, then zip them together
    user_names = []
    points = []
    for obj in user_points:
        if obj['displayPoints']:
            user = obj['user']
            point = obj['points']
            points.append(point)
            user_names.append(User.objects.get(id=user).get_full_name())
    user_data = zip(user_names, points)

    context = {'users': user_data}
    return render(request, 'messaging/leaderboard.html', context)
