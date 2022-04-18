from ipaddress import v4_int_to_packed
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from functools import reduce
import operator

from .forms import CustomUserChangeForm, ProfileCreateForm, ProfileUpdateForm, MessageSend
from .models import Profile, Conversation, Message, UserGroup
from store.models import Purchase

def getPoints(body: str) -> int:
    """
    Helper function that gets the number of points in a given message.
    
    :param body - the body of the message
    :return the total number of points in the message
    """
    emoji_list = ["🐶", "🐱", "🦋", "🐢", "🦄", "🐰", "🐾", "🦩", "🦈", "🦖"]
    points = 0
    for em in emoji_list:
        points += body.count(em) * 10
    return points

def sendPoints(newMessage: Message, members: list[User], convo: Conversation, sender: User) -> None:
    """
    Helper function to send points from the sender user to all the other members of a conversation.

    :param newMessage - the new message being sent
    :param members - all of the users in the conversation
    :param convo - the Conversation
    :param sender - the user sending the message
    """
    # print('Members:' + str(members))
    totalPoints = newMessage.points * (len(members) - 1)
    pointsToSend = 0
    if sender.profile.points < totalPoints:
        pointsToSend = sender.profile.points
    else:
        pointsToSend = totalPoints
    # print("To send:" + str(pointsToSend))
    Profile.objects.filter(user=sender).update(points = (sender.profile.points - pointsToSend))

    for member in convo.userGroup.members.all():
        if member.username != sender.username:
            Profile.objects.filter(user=member).update(wallet = (int)(member.profile.wallet +  (pointsToSend / (len(members) - 1))))
            Profile.objects.filter(user=member).update(allTimePoints = (int)(member.profile.allTimePoints +  (pointsToSend / (len(members) - 1))))
    
def login_page(request):
    """View for the site's login page."""
    page = 'login'

    # If the user's already logged in, take them to their inbox
    if request.user.is_authenticated:
        return redirect('inbox')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Make sure the user exists
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

def logout_user(request):
    """Logouts the user from the site."""
    logout(request)
    return redirect('inbox')

def register_user_page(request):
    """View to let users register a profile."""
    page = 'register'
    form = ProfileCreateForm()

    if request.method == 'POST':
        form = ProfileCreateForm(request.POST, request.FILES or None)

        # Save the data if the form is valid
        if form.is_valid():
            user, profile = form.save(commit=False)
            user.username = user.username.lower()

            user.save()
            profile.save()

            login(request, user)
            return redirect('inbox')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form': form, 'page': page}
    return render(request, 'messaging/login_register.html', context)

@login_required(login_url='login')
def inbox(request):
    """View for the user's inbox."""
    convos = Conversation.objects.filter(userGroup__members__in=[request.user.id])
    
    # Prep the data to display
    names = []
    for convo in convos:
        # Preview the first message
        first_message = Message.objects.filter(conversation=convo).first()

        # Get the users' full names
        username_list = convo.name.split('-')
        username_list.remove(request.user.username)
        name_list = []
        for username in username_list:
            name_list.append(User.objects.get(username=username).get_full_name())

        # Name the conversation based on users' full names
        name = ', '.join(name_list)
        names.append([convo, name, first_message])

    user_name = request.user.get_full_name()
    
    context = {'names': names, 'user_name': user_name}
    return render(request, 'messaging/inbox.html', context)

def send_message(request):
    """View for the user to send a message."""
    context = {}
    return render(request, 'messaging/send_message.html', context)

def conversation(request, pk):
    """View for an individual conversation."""
    convo = Conversation.objects.get(id=pk)
    messages = Message.objects.filter(conversation=convo)
    members = []
    for member in convo.userGroup.members.all():
        members.append(member.get_full_name())

    if request.method == 'POST':
        newMessage = Message.objects.create(
            sender=request.user,
            conversation=convo,
            body=request.POST.get('body')[3:-4],
            points = getPoints(request.POST.get('body')[3:-4].replace("&nbsp;", "")),
        )
        
        sendPoints(newMessage, members, convo, newMessage.sender)

        return redirect('conversation', pk=convo.id)

    first_name = request.user.first_name
    context = {'convo': convo, 'messages': messages, 'first_name': first_name, 'members': members}
    return render(request, 'messaging/conversation.html', context)

@login_required(login_url='login')
def profile(request, pk):
    """View for a user's own profile."""
    current_user = request.user
    user = User.objects.get(id=pk)
    profile = user.profile
    purchases = Purchase.objects.filter(buyer=profile)

    context = {'current_user': current_user, 'user': user, 'profile': profile, 'purchases': purchases}
    return render(request, 'messaging/profile.html', context)

@login_required(login_url='login')
def change_password(request, pk):
    """View to let users change their password."""
    page = 'changePassword'

    user = User.objects.get(id=pk)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            update_session_auth_hash(request, user)
            messages.success(request, 'Successfully updated your password!')
            return redirect('profile', user.id)
        else:
            messages.error(request, 'An error occurred during password update')
    else:
        form = PasswordChangeForm(user)

    context = {'form': form, 'page': page}
    return render(request, 'messaging/login_register.html', context)

@login_required(login_url='login')
def update_profile(request, pk):
    """View to let users update their login information and profiles."""
    page = 'updateProfile'

    user = User.objects.get(id=pk)
    profile = user.profile

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES or None, instance=profile)

        # Save the data if the form is valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)

            user.save()
            profile.save()

            return redirect('profile', user.id)
        else:
            messages.error(request, 'An error occured during profile update')
    else:
        profile_form = ProfileUpdateForm(request.FILES or None, instance=profile)
        user_form = CustomUserChangeForm(instance=user)

    context = {'profile_form': profile_form, 'user_form': user_form, 'page': page}
    return render(request, 'messaging/login_register.html', context)

def leaderboard(request):
    """View for the global leaderboard."""
    # Get only the top users that have their points public
    NUM_USERS_TO_SHOW = 10
    user_points = Profile.objects.filter(displayPoints=True).values('points', 'user').order_by('-points')[:NUM_USERS_TO_SHOW]

    # Prepare data for each user on the leaderboard
    user_names = []
    points = []
    for obj in user_points:
        user = obj['user']
        point = obj['points']
        points.append(point)
        user_names.append(User.objects.get(id=user).get_full_name())

    user_data = list(zip(user_names, points))
    context = {'users': user_data}
    return render(request, 'messaging/leaderboard.html', context)

@login_required(login_url='login')
def create_convo(request):
    """View to create a conversation for a user."""
    def _make_group_convo(group_name: str, send_to_list: list[str]) -> tuple[UserGroup, Conversation]:
        """
        Make a group conversation.
        
        :param group_name - the name of the UserGroup
        :param send_to_list - a list of usernames to add to the conversation
        :return a tuple with the new UserGroup and Conversation
        """
        user_group = UserGroup.objects.create(name=group_name)
        user_group.save()

        for username in send_to_list:
            user_group.members.add(User.objects.get(username=username))

        convo = Conversation.objects.create(name=group_name, userGroup=user_group)
        convo.save()
        
        return user_group, convo

    # Create a message if the user wants to
    form = MessageSend()
    if request.method == 'POST':
        send_to = request.POST.get('send_to')
        send_to = send_to.replace(" ", "")
        send_to_list = send_to.split(",")
        send_to_list.append(request.user.username)
        group_name = "-".join(send_to_list)
        body = request.POST.get('body')

        # Create the user group and the conversation from it
        convo = None
        user_group = None

        # Query for if the user group exists
        user_group_Qset = UserGroup.objects.filter(reduce(operator.and_, (Q(name__icontains=x) for x in send_to_list)))
        try:
            if not user_group_Qset.exists():
                user_group, convo = _make_group_convo(group_name, send_to_list)
            else:
                user_group = UserGroup.objects.get(id=user_group_Qset[0].id)
                if user_group.members.all().count() > len(send_to_list):
                    user_group, convo = _make_group_convo(group_name, send_to_list)
                else:
                    convo = user_group.conversation
            print(body)

            newMessage = Message.objects.create(
                sender=request.user,
                conversation=convo,
                body=request.POST.get('body')[3:-4],
                points = getPoints(request.POST.get('body')[3:-4].replace("&nbsp;", "")),
            )
            members = []
            for member in convo.userGroup.members.all():
                members.append(member.get_full_name())

            sendPoints(newMessage, members, convo, newMessage.sender)

            return redirect('conversation', pk=convo.id)
        except ObjectDoesNotExist as e:
            messages.error(request, e)


    context = {'form': form}
    return render(request, 'messaging/new_convo.html', context)
