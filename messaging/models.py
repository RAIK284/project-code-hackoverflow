from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    members = models.ManyToManyField(User, related_name='members', blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        name = ''
        for i, a in self.members:
            if i > 0:
                name += ', '
            name += a.name
        return name

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField()
    body = models.TextField()

    def __str__(self):
        return self.body[:50]

class Token(models.Model):
    points = models.IntegerField()
    tag = models.CharField(max_length=7)