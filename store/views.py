from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Product, Purchase
from messaging.models import Profile

def index(request):
    """View for the main page of products."""
    # Order by popularity
    products = Product.objects.all().order_by('-amount_sold', 'name')

    context = {'products': products}
    return render(request, 'store/index.html', context)

@login_required(login_url='login')
def buy(request, pk):
    """View for an individual product."""
    NUM_BUYERS_SHOW = 3
    product = Product.objects.get(id=pk)
    recent_purchasers = Purchase.objects.filter(product=product).values('buyer').order_by('-timestamp')[:NUM_BUYERS_SHOW]

    user_names = []
    for obj in recent_purchasers:
        user = obj['buyer']
        user_names.append(User.objects.get(id=user).get_full_name())

    context = {'product': product, 'recent_purchasers': user_names}
    return render(request, 'store/buy.html', context)

@login_required(login_url='login')
def buy_page(request, pk):
    """View that actually lets a user buy a product."""
    NUM_BUYERS_SHOW = 3
    product = Product.objects.get(id=pk)
    buyer = Profile.objects.get(user=request.user)
    recent_purchasers = Purchase.objects.filter(product=product).values('buyer').order_by('-timestamp')[:NUM_BUYERS_SHOW]

    user_names = []
    for obj in recent_purchasers:
        user = obj['buyer']
        user_names.append(User.objects.get(id=user).get_full_name())

    context = {'product': product, 'recent_purchasers': user_names}
    if request.method == 'GET':
        # Check if user already owns product
        if Purchase.objects.filter(buyer=buyer).filter(product=product):
            messages.error(request,'Already purchased item')
        elif (buyer.wallet - product.point_cost) >= 0:
            product.amount_sold += 1
            product.save(update_fields=['amount_sold'])

            Purchase.objects.create(
                buyer=buyer,
                product=product
            )
        
            buyer.wallet -= product.point_cost
            buyer.save(update_fields=['wallet'])
            return redirect('index')
        else:
            messages.error(request,'Not enough points')

    return render(request, 'store/buy.html', context)
