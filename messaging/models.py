from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    #picture = models.ImageField()
    wallet = models.IntegerField(default=0)
    displayPoints = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    #backpack = models.ManyToManyField(Item)
    displayPurchases = models.BooleanField(default=False)
    #purchases = models.ManyToManyField(Purchase)

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        return name
    
    
    


class Conversation(models.Model):
    """Model controlling the entire set of messages sent back-and-forth between users."""
    members = models.ManyToManyField(Profile, related_name='members', blank=False)
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
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
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
