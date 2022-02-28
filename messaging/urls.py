from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('registerUser/', views.registerUserPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('sendMessage', views.sendMessage, name='send'),
    path('conversation/<str:pk>', views.conversation, name='conversation'),
    path('', views.inbox, name='inbox'),
]
