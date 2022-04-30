from django.urls import path
from django.views.generic import RedirectView

from . import views

# All possible url patterns
urlpatterns = [
    path('', views.index, name='index'),
    path('buy/<str:pk>/', views.buy, name='buy'),
    path('buy_page/<str:pk>/', views.buy_page, name='buy_page'),
]
