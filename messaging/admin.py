from django.contrib import admin

from .models import Conversation, Message, Profile, UserGroup

# Register different models for admin use
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(UserGroup)
