from .models import Conversation, Profile, Message
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class ProfileCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=75, required=True)
    bio = forms.CharField(max_length=200, widget=forms.Textarea, required=True)
    make_my_points_public = forms.BooleanField()
    make_my_purchaes_public = forms.BooleanField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def save(self, commit=True):
        user = super(ProfileCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        profile = Profile(user=user, bio=self.cleaned_data['bio'], displayPoints=self.cleaned_data['make_my_points_public'], displayPurchases=self.cleaned_data['make_my_purchaes_public'])
        if commit:
            user.save()
            profile.save()
        return user, profile

class MessageSend(ModelForm):
    conversation_name = forms.CharField(max_length=30, required=True)
    send_to = forms.CharField(required=True)
    body = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Message
        fields = ['body']
        exclude = ['host', 'participants']