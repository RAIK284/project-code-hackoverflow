from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from django.forms import ModelForm

from .models import Message, Profile

class ProfileCreateForm(UserCreationForm):
    """Form to allow a user to make a profile."""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=75, required=True)
    bio = forms.CharField(max_length=200, widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)
    make_my_points_public = forms.BooleanField(required=False)
    make_my_purchases_public = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def save(self, commit=True):
        """Saves the data for a given profile (and tied user)."""
        # Create "User" data
        user = super(ProfileCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # Create "Profile" data
        profile = Profile(user=user, bio=self.cleaned_data['bio'], image=self.cleaned_data['image'], displayPoints=self.cleaned_data['make_my_points_public'], displayPurchases=self.cleaned_data['make_my_purchases_public'])
        
        if commit:
            user.save()
            profile.save()
        
        return user, profile

class CustomUserChangeForm(UserChangeForm):
    """Wrapper class to allow users to update only their relevant information."""
    # Don't display password reset settings
    password = None
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(ModelForm):
    """Form to allow users to update their profile."""
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'image', 'displayPoints', 'displayPurchases']

class MessageSend(ModelForm):
    """Sends a message to other users."""
    send_to = forms.CharField(required=True)
    body = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Message
        fields = ['body']
        exclude = ['host', 'participants']
