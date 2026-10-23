"""
Import Render, Redirect, Reverse, Get_Object_or_404, HttpResponse
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render, redirect, reverse, get_object_or_404, \
    HttpResponse
from django.http import Http404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
import stripe
import json

# Internal:
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from bag.contexts import bag_contents
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def _render_checkout(request, order_form):
    """Render checkout with a fresh PaymentIntent for the current bag."""
    current_bag = bag_contents(request)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=round(current_bag['grand_total'] * 100),
        currency=settings.STRIPE_CURRENCY,
    )

    if not settings.STRIPE_PUBLIC_KEY:
        messages.warning(
            request,
            'Stripe public key is missing. Did you forget to set it in your environment?',
        )

    return render(request, 'checkout/checkout.html', {
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
        **current_bag,
    })


@require_POST
def cache_checkout_data(request):
    """
    To cache users shopping basket
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """ Checkout Request """

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment.")
            return redirect(reverse('view_bag'))
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            client_secret = request.POST.get('client_secret', '')
            if not client_secret or '_secret' not in client_secret:
                messages.error(
                    request,
                    'Payment details could not be verified. Please try again.',
                )
                return redirect(reverse('view_bag'))

            order = order_form.save(commit=False)
            pid = client_secret.split('_secret', 1)[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            if request.user.is_authenticated:
                order.user_profile, _ = UserProfile.objects.get_or_create(
                    user=request.user,
                )
            order.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in \
                                item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag"
                        "wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            request.session['checkout_order_number'] = order.order_number
            return redirect(reverse('checkout_success',
                            args=[order.order_number]))
        else:
            if not bag:
                messages.error(request, "There's nothing in your bag at the moment.")
                return redirect(reverse('view_bag'))
            messages.error(
                request,
                'There was an error with your form. Please check your details.',
            )
            return _render_checkout(request, order_form)
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        # Attempt to prefill the form with any info the user
        # #maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()
        return _render_checkout(request, order_form)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if order.user_profile_id != profile.id:
            raise Http404

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
    elif request.session.get('checkout_order_number') != order.order_number:
        raise Http404

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
