from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

class ProfileCreateForm(UserCreationForm):
    """Form to allow users to create their profiles."""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=75, required=True)
    bio = forms.CharField(max_length=200, widget=forms.Textarea, required=True)

    class Meta:
        """Order users by the 'fields' list."""
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def save(self, commit=True):
        # Saves a user and their profile based on docstring requirements
        user = super(ProfileCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        profile = Profile(user=user, bio=self.cleaned_data['bio'])
        if commit:
            user.save()
            profile.save()

        return user, profile
