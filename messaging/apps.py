from django.apps import AppConfig

# Identifies 'messaging' as a django app
class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'
