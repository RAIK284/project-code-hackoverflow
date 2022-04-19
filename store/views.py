from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from messaging.models import Profile
from django.contrib.auth.models import User
from .models import Product, Purchase
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    """View for the main page of products."""
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'store/index.html', context)

@login_required(login_url='login')
def buy(request, pk):
    """View for an individual product."""
    product = Product.objects.get(id=pk)
    recent_purchasers = Purchase.objects.filter(product = product).values('buyer').order_by('-timestamp')[:3]
    user_names = []
    for obj in recent_purchasers:
        user = obj['buyer']
        user_names.append(User.objects.get(id=user).get_full_name())

    context = {'product': product, 'recent_purchasers': user_names}
    
    return render(request, 'store/buy.html', context)

@login_required(login_url='login')
def buy_page(request, pk):
    """View that actually lets a user buy a product."""
    product = Product.objects.get(id=pk)
    buyer = Profile.objects.get(user = request.user)
    recent_purchasers = Purchase.objects.filter(product = product).values('buyer').order_by('-timestamp')[:3]
    user_names = []
    for obj in recent_purchasers:
        user = obj['buyer']
        user_names.append(User.objects.get(id=user).get_full_name())

    context = {'product': product, 'recent_purchasers': user_names}
    if request.method == 'GET':
        if Purchase.objects.filter(buyer = buyer).filter(product = product) is not None:
            messages.error(request,'Already purchased item')
        elif buyer.wallet - product.point_cost >= 0:
            Product.objects.filter(id = product.id).update(amount_sold = product.amount_sold + 1)
            Purchase.objects.create(
                buyer = buyer,
                product = product
            )
        
            Profile.objects.filter(user=request.user).update(wallet=buyer.wallet - product.point_cost)
            return redirect('index')
        else:
            messages.error(request,'Not enough points')
    
    
    return render(request, 'store/buy.html', context)
    
