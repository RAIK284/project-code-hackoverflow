from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

# Create your models here.
'''
- userId:int
- username:string
- password:string
- email:string
- phone number:string
- bio:string
- profile picture:image
- wallet:int
- display_points:bool
- points:int
- backpack:[Item]
- display_purchases:bool
- purchases:[Purchase]
'''

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phoneNumber = PhoneNumberField(blank=True)
    
    


class Conversation(models.Model):
    """Model controlling the entire set of messages sent back-and-forth between users."""
    members = models.ManyToManyField(User, related_name='members', blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Show the most recently updated messages first
        ordering = ['-updated', '-created']

    def __str__(self):
        # Create a comma-separated list of members in a conversation
        name = ''
        for i, user in self.members:
            if i > 0:
                name += ', '
            name += user.name
        return name

class Message(models.Model):
    """Model controlling an individual message sent by a user."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    # Track the number of token points in the message, if applicable
    points = models.IntegerField()

    def __str__(self):
        return self.body[:50]

class Token(models.Model):
    points = models.IntegerField()

    # Track the emoji/emoticon used
    tag = models.CharField(max_length=7)
