from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('registerUser/', views.register_user_page, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('sendMessage', views.send_message, name='send'),
    path('conversation/<str:pk>', views.conversation, name='conversation'),

    path('', views.inbox, name='inbox'),
]
