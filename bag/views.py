"""
Setup views for shopping bag
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render, redirect, reverse, HttpResponse, \
     get_object_or_404
from django.contrib import messages

# Internal
from products.models import Product

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def _normalise_bag_item(data):
    """Convert legacy bag data into the standard size-based dict format."""
    if isinstance(data, int):
        return {'items_by_size': {'default': data}}

    if isinstance(data, dict):
        if 'items_by_size' not in data:
            data['items_by_size'] = {}
        return data

    return {'items_by_size': {}}


def view_bag(request):
    """
    A view that renders the bag contents page
    """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})
    item_key = str(item_id)
    current_item = bag.get(item_key, bag.get(item_id))

    if size:
        bag_item = _normalise_bag_item(current_item)
        sizes = bag_item['items_by_size']
        sizes[size] = sizes.get(size, 0) + quantity
        bag[item_key] = {'items_by_size': sizes}
        messages.success(request,
                         f'Added size {size.upper()} {product.name} '
                         f'to your bag')
    else:
        if current_item is None:
            bag[item_key] = quantity
            messages.success(request, f'Added {product.name} to your bag')
        elif isinstance(current_item, int):
            bag[item_key] = current_item + quantity
            messages.success(
                request, f'Updated {product.name} quantity to {bag[item_key]}')
        else:
            total_quantity = sum(current_item.get('items_by_size', {}).values())
            bag[item_key] = total_quantity + quantity
            messages.success(
                request, f'Updated {product.name} quantity to {bag[item_key]}')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})
    item_key = str(item_id)
    current_item = bag.get(item_key, bag.get(item_id))

    if size:
        bag_item = _normalise_bag_item(current_item)
        sizes = bag_item['items_by_size']
        if quantity > 0:
            sizes[size] = quantity
            messages.success(request,
                             f'Updated size {size.upper()} {product.name} '
                             f'quantity to {sizes[size]}')
        else:
            sizes.pop(size, None)
            if not sizes:
                bag.pop(item_key, None)
                bag.pop(item_id, None)
                request.session['bag'] = bag
                return redirect(reverse('view_bag'))
            messages.success(request,
                             f'Removed size {size.upper()} '
                             f'{product.name} from your bag')
        bag[item_key] = {'items_by_size': sizes}
    else:
        if quantity > 0:
            bag[item_key] = quantity
            messages.success(
                request, f'Updated {product.name} quantity to {bag[item_key]}')
        else:
            bag.pop(item_key, None)
            bag.pop(item_id, None)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove the item from the shopping bag
    """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})
        item_key = str(item_id)

        if size:
            bag_item = _normalise_bag_item(bag.get(item_key, bag.get(item_id)))
            bag_item['items_by_size'].pop(size, None)
            if not bag_item['items_by_size']:
                bag.pop(item_key, None)
                bag.pop(item_id, None)
            else:
                bag[item_key] = {'items_by_size': bag_item['items_by_size']}
            messages.success(request,
                             f'Removed size {size.upper()} '
                             f'{product.name} from your bag')
        else:
            bag.pop(item_key, None)
            bag.pop(item_id, None)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
