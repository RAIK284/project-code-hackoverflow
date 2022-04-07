from datetime import timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
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
    
    def __str__(self):
        return self.user.name
    bio = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, null=True)
    wallet = models.IntegerField(default=0)
    displayPoints = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    #backpack = models.ManyToManyField(Item)
    displayPurchases = models.BooleanField(default=False)
    #purchases = models.ManyToManyField(Purchase)

    def _has_sent_message_recently(self, time_to_check: timedelta) -> bool:
        """
        Checks if a user has sent a message (in any conversation) in the last <time_to_check> set of time.

        :param time_to_check - the max. amount of time that define "recent"
        :return True if the user has sent a message recently, False if not
        """
        latest_user_message = None
        try:
            latest_user_message = Message.objects.filter(sender=self.user).latest('updated')
        except Message.DoesNotExist:
            return False

        if not latest_user_message or timezone.now() - time_to_check > latest_user_message.updated:
            return False

        return True

    def remind_user_to_send_message(self) -> int:
        """
        Sends an email to a user if they haven't sent a message recently.

        :return 0 if the message failed, or 1 if successful (1 message was sent)
        """
        DAYS_TO_CHECK = 2
        recent = self._has_sent_message_recently(timedelta(days=DAYS_TO_CHECK))

        status = 0
        if not recent:
            status = send_mail(
                subject="Pawsitivity Reminder",
                message=f"Hi {self.user.first_name}! We noticed you haven't sent any messages of positivity lately. We would love to see you again on Pawsitivity!",
                from_email=None,
                recipient_list=[self.user.email],
                fail_silently=False
            )

        return status

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
