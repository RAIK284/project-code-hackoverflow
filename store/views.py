from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from messaging.models import Profile

from .models import Product, Purchase

def index(request):
    """View for the main page of products."""
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'store/index.html', context)

@login_required(login_url='login')
def buy(request, pk):
    """View for an individual product."""
    product = Product.objects.get(id=pk)

    context = {'product': product}
    return render(request, 'store/buy.html', context)

@login_required(login_url='login')
def buy_page(request, pk):
    """View that actually lets a user buy a product."""
    product = Product.objects.get(id=pk)
   
    if request.method == 'GET':
        buyer = Profile.objects.get(user=request.user)

        # Make sure the user has enough funds to buy the product
        if buyer.wallet - product.point_cost >= 0:
            Product.objects.filter(id=product.id).update(amount_sold=product.amount_sold + 1)
            Purchase.objects.create(
                buyer = buyer,
                product = product
            )
        
            Profile.objects.filter(user=request.user).update(wallet=buyer.wallet - product.point_cost)
            return redirect('index')

    context = {'product': product}
    return render(request, 'store/buy.html', context)
    
