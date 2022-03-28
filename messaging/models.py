from django.contrib.auth.models import User
from django.db import models
import os

def get_image_path(profile, filename):
    """
    Gets the system path for an image to display.
    
    Taken from: https://stackoverflow.com/a/8192232/5696057
    """
    return os.path.join('profile_images', str(profile.user.id), filename)

class Profile(models.Model):
    """Model controlling a user's profile data."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, null=True)
    wallet = models.IntegerField(default=0)
    displayPoints = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    #backpack = models.ManyToManyField(Item)
    displayPurchases = models.BooleanField(default=False)
    #purchases = models.ManyToManyField(Purchase)

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        return name
    
class UserGroup(models.Model):
    """A connection between users for a conversation."""
    name = models.TextField(max_length=400)
    members = models.ManyToManyField(User, related_name='members')

class Conversation(models.Model):
    """Model controlling the entire set of messages sent back-and-forth between users."""
    name = models.TextField(max_length=400, default="Conversation")
    userGroup = models.OneToOneField(UserGroup, on_delete=models.CASCADE, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Show the most recently updated conversations first
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name[:50]

class Message(models.Model):
    """Model controlling an individual message sent by a user."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    read = models.BooleanField(default=False)

    # Track the number of token points in the message, if applicable
    points = models.IntegerField(default=0)

    class Meta:
        # Show the most recently updated messages last
        ordering = ['updated', 'created']

    def __str__(self):
        return self.body[:50]

class Token(models.Model):
    """Model to store data on what tokens are worth which values."""
    points = models.IntegerField()

    # Track the emoji/emoticon used
    tag = models.CharField(max_length=7)
