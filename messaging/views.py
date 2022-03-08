from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileCreateForm, MessageSend
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
    convos = Conversation.objects.filter(members__in=[request.user.id])
    context = {'convos':convos}
    return render(request, 'messaging/inbox.html', context)

def sendMessage(request):
    context = {}
    return render(request, 'messaging/send_message.html', context)

def conversation(request, pk):
    convo = Conversation.objects.get(id=pk)
    messages = Message.objects.filter(conversation=convo)
    members = []
    for member in convo.members.all():
        members.append(member.get_full_name())
    first_name = request.user.first_name
    context = {'convo':convo, 'messages':messages, 'first_name':first_name, 'members':members}
    return render(request, 'messaging/conversation.html', context)

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    #profile = Profile.objects.get(user=user)
    context = {'user':user}
    return render(request, 'messaging/profile.html', context)

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
    context = {'users': user_data}
    return render(request, 'messaging/leaderboard.html', context)

@login_required(login_url='login')
def createConvo(request):
    form = MessageSend()
    if request.method == 'POST':
        conversation_name = request.POST.get('conversation_name')
        sendTo = request.POST.get('send_to')
        sendToList = sendTo.split(",")
        body = request.POST.get('body')
        users = User.objects.filter(username=sendToList)
        convo, created = Conversation.objects.get_or_create(members=users)
        convo.save()
        for name in sendToList:
            convo.members.add(request.user, User.objects.get(username=name))


        Message.objects.create(
            sender=request.user,
            conversation=convo,
            body=body,
            points=0,
        )
        return redirect('conversation', pk=convo.id)
    context = {'form': form}
    return render(request, 'messaging/new_convo.html', context)
