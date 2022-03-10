from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from matplotlib import use
from .forms import ProfileCreateForm, MessageSend
from django.db.models import Count, Q
from django.core.exceptions import ObjectDoesNotExist
import operator
from .models import Profile, Conversation, Message, UserGroup
from functools import reduce


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
    convos = Conversation.objects.filter(userGroup__members__in=[request.user.id])
    convoNames = []
    for convo in convos:
        allUsernames = convo.name.split('-')
        nameString = ""
        for username in allUsernames:
            if username is not request.user.username:
                nameString += User.objects.get(username=username).get_full_name() + ', '
        nameString = nameString[:-2]
        convoNames.append(nameString)
        
    context = {'convos':convos, 'convoNames':convoNames}
    return render(request, 'messaging/inbox.html', context)

def sendMessage(request):
    context = {}
    return render(request, 'messaging/send_message.html', context)

def conversation(request, pk):
    convo = Conversation.objects.get(id=pk)
    messages = Message.objects.filter(conversation=convo)
    members = []
    for member in convo.userGroup.members.all():
        members.append(member.get_full_name())
    first_name = request.user.first_name
    context = {'convo':convo, 'messages':messages, 'first_name':first_name, 'members':members}
    return render(request, 'messaging/conversation.html', context)

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    profile = user.profile
    context = {'user':user, 'profile':profile}
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
        sendTo = request.POST.get('send_to')
        sendTo = sendTo.replace(" ", "")
        sendToList = sendTo.split(",")
        sendToList.append(request.user.username)
        groupName = "-".join(sendToList)
        body = request.POST.get('body')

        convo = None
        userGroup = None
        userGroupQSet = UserGroup.objects.filter(reduce(operator.and_, (Q(name__icontains=x) for x in sendToList)))
        if not userGroupQSet.exists():
            userGroup = UserGroup.objects.create(name=groupName)
            userGroup.save()
            for username in sendToList:
                userGroup.members.add(User.objects.get(username=username))
            convo = Conversation.objects.create(name = groupName, userGroup=userGroup)
            convo.save()
            convo.name = groupName
        else:
            userGroup = UserGroup.objects.get(id=userGroupQSet[0].id)
            convo = userGroup.conversation


        Message.objects.create(
            sender=request.user,
            conversation=convo,
            body=body,
            points=0,
        )
        return redirect('conversation', pk=convo.id)
    context = {'form': form}
    return render(request, 'messaging/new_convo.html', context)
