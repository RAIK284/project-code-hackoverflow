from django.shortcuts import render

from .models import Product

def index(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'store/index.html', context)

def buy(request, pk):
    product = Product.objects.get(id=pk)

    context = {'product': product}
    return render(request, 'store/buy.html', context)
