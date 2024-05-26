import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from .cart import Cart
from .forms import CheckoutForm
from order.utilities import checkout, notify_vendor, notify_customer

def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']

            if payment_method == 'stripe':
                stripe.api_key = settings.STRIPE_SECRET_KEY
                stripe_token = form.cleaned_data['stripe_token']

                try:
                    charge = stripe.Charge.create(
                        amount=int(cart.get_total_cost() * 100), # Amount in Paisa (1 PKR = 100 Paisa)
                        currency='PKR',
                        description='Charge From Multivendor Shop',
                        source=stripe_token
                    )
                except Exception:
                    messages.error(request, "Something went wrong with the payment.")
                    return redirect('cart:cart')
            elif payment_method == 'cod':
                # Handle Cash on Delivery (COD)
                messages.success(request, "Order placed successfully with Cash on Delivery.")

            # Handle order saving for both payment methods
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            place = form.cleaned_data['place']

            order = checkout(request, first_name, last_name, email, phone, address, zipcode, place, cart.get_total_cost())

            cart.clear()

            # Send Email Notification
            # notify_customer(order)
            # notify_vendor(order)

            return redirect('cart:success')

    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart:cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart:cart')

    return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

def success(request):
    return render(request, 'cart/success.html')
