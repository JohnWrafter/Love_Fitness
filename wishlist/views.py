from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from products.models import Product
from .models import Favourites


@login_required
def view_product_favourites(request):
    """
    A view that displays users wishlist
    """
    favourites_items_count = 0
    try:
        all_favourites = Favourites.objects.filter(username=request.user.id)[0]
    except IndexError:
        favourites_items = None
    else:
        favourites_items = all_favourites.products.all()
        favourites_items_count = all_favourites.products.all().count()

    if not favourites_items:
        messages.info(request, 'Your wishlist is empty!')

    template = 'wishlist/wishlist.html'
    context = {
        'favourites_items': favourites_items,
        'favourites_items_count': favourites_items_count
    }
    return render(request, template, context)


@login_required
def add_product_to_favourites(request, item_id):
    """
    Add a product item to wishlist
    """
    product = get_object_or_404(Product, pk=item_id)
    try:
        favourites = get_object_or_404(Favourites, username=request.user.id)
    except Http404:
        favourites = Favourites.objects.create(username=request.user)
    if product in favourites.products.all():
        messages.info(request, 'The product is '
                               'already in your wishlist!')
    else:
        favourites.products.add(product)
        messages.info(request, 'Added the product to your wishlist')
    return redirect(reverse('product_detail', args=[item_id]))


@login_required
def remove_product_from_favourites(request, item_id, redirect_from):
    """
    Remove a product item from wishlist
    """
    product = get_object_or_404(Product, pk=item_id)
    favourites = get_object_or_404(Favourites, username=request.user.id)
    if product in favourites.products.all():
        favourites.products.remove(product)
        messages.info(request, 'Removed the product '
                               'from your wishlist')
    else:
        messages.error(request, 'That product is '
                                'not in your wishlist!')
    if redirect_from == 'favourites':
        redirect_url = reverse('view_product_favourites')
    else:
        redirect_url = reverse('product_detail', args=[item_id])
    return redirect(redirect_url)
