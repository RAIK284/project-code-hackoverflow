from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('registerUser/', views.register_user_page, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('leaderboard/', views.leaderboard, name='leaderboard'),

    path('sendMessage', views.send_message, name='send'),
    path('conversation/<str:pk>', views.conversation, name='conversation'),
    path('createConvo', views.create_convo, name='createConvo'),

    path('profile/<str:pk>', views.profile, name='profile'),
    path('updateProfile/<str:pk>', views.update_profile, name='updateProfile'),

    
    path('', views.inbox, name='inbox'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
