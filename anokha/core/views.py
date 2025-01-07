from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.shortcuts import render, get_object_or_404
from .models import Category, Item
import razorpay
from django.conf import settings



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# @login_required
# def home(request):
#     return render(request, 'home/home.html')


# View to display the homepage with all categories
@login_required
def home(request):
    categories = Category.objects.all()
    return render(request, 'home/home.html', {'categories': categories})

# View to display items of a particular category
def category_items(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = category.items.all()
    return render(request, 'category/category_items.html', {'category': category, 'items': items})


# add_to_cart

from decimal import Decimal

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Ensure the cart is a dictionary
    if not isinstance(request.session.get('cart'), dict):
        request.session['cart'] = {}

    cart = request.session['cart']

    # Check if item_id is already in the cart
    if str(item_id) in cart:
        # If the item exists, increase the quantity
        cart[str(item_id)]['quantity'] += 1
    else:
        # Add new item to the cart
        cart[str(item_id)] = {
            'name': item.name,
            'price': float(item.price),  # Convert Decimal to float
            'quantity': 1,
        }
    
    # Save the updated cart back to the session
    request.session['cart'] = cart

    return redirect('category_items', category_id=item.category.id)




# remove item from cart

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        del cart[str(item_id)]  # Remove the item
        request.session['cart'] = cart  # Save updated cart
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in cart.")

    return redirect('cart_view')

# cart view

def cart_view(request):
    cart = request.session.get('cart', {})
    print("Cart contents:", cart)  # Debugging print
    items = []
    total_price = 0

    if isinstance(cart, dict):
        for item_id, details in cart.items():
            item_total = details['price'] * details['quantity']
            total_price += item_total
            items.append({
                'id': item_id,
                'name': details['name'],
                'price': details['price'],
                'quantity': details['quantity'],
                'total_price': item_total,
            })
    
    return render(request, 'category/cart.html', {'items': items, 'total_price': total_price})




# Buy Now
def buy_now(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return redirect('checkout', item_id=item.id)

# payment gateway

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def checkout(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Ensure the amount is in paise and within limits
    price_in_rupees = item.price  # Assuming price is in rupees
    amount = int(price_in_rupees * 100)  # Convert rupees to paise

    if amount > 10000000:  # 10,000,000 paise = ₹1,00,000
        return HttpResponse("Amount exceeds Razorpay's maximum limit.", status=400)

    # Create Razorpay Order
    razorpay_order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        'item': item,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_amount': amount,
        'currency': "INR",
    }
    return render(request, 'category/checkout.html', context)


def payment_success(request):
    # Handle successful payment here
    return render(request, 'category/payment_success.html')



# Add item to cart
# def add_to_cart(request, item_id):
#     # Fetch the item from the database
#     item = get_object_or_404(Item, id=item_id)
    
#     # Retrieve cart from session, or initialize as an empty dictionary if not present
#     cart = request.session.get('cart', {})

#     # Check if the item is already in the cart
#     if str(item_id) in cart:
#         # If the item is already in the cart, increment the quantity
#         cart[str(item_id)]['quantity'] += 1
#     else:
#         # If it's a new item, add it to the cart
#         cart[str(item_id)] = {
#             'name': item.name,
#             'price': item.price,
#             'quantity': 1,
#         }

#     # Save the updated cart back to the session
#     request.session['cart'] = cart

#     # Optionally, add a success message
#     messages.success(request, f"Added {item.name} to your cart.")

#     # Redirect back to the category page
#     return redirect('category_items', category_id=item.category.id)
