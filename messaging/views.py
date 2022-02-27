from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'messaging/home.html', context)
