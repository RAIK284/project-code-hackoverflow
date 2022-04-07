from django.shortcuts import redirect, render

from messaging.models import Profile

from .models import Product, Purchase
from django.contrib.auth.decorators import login_required

def index(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'store/index.html', context)

@login_required(login_url='login')
def buy(request, pk):
    product = Product.objects.get(id=pk)

    context = {'product': product}
    
    return render(request, 'store/buy.html', context)

@login_required(login_url='login')
def buy_page(request, pk):
    product = Product.objects.get(id=pk)
    #points = Profile.objects.filter(user = request.user).values('points')
    context = {'product': product}
   
    if request.method == 'GET':
        buyer = Profile.objects.get(user = request.user)
        if buyer.wallet - product.point_cost >= 0:
            Product.objects.filter(id = product.id).update(amount_sold = product.amount_sold + 1)
            Purchase.objects.create(
                buyer = buyer,
                product = product
            )
        
            Profile.objects.filter(user = request.user).update(wallet = buyer.wallet - product.point_cost)
            return redirect('index')
        #else: 
         #   raise ValueError('Not enough points')
    
    return render(request, 'store/buy.html', context)
    
