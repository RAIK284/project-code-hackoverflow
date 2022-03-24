from django.contrib import admin
from .models import Profile, Conversation, Message, Token, UserGroup

admin.site.register(Profile)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Token)
admin.site.register(UserGroup)
