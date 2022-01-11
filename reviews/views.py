from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review
from django.contrib.auth.models import User
from products.models import Product
from django.contrib import messages


# Add review view
# got a helping hand here https://www.youtube.com/watch?v=lSX8nzu9ozg
@login_required
def add_review(request, product_id):
    # adds a review to the site
    product = Product.objects.get(id=product_id)
    if not request.user.is_authenticated:
        messages.error(request,
                       'Sorry, only logged in members may leave a review')
        return redirect(reverse('home'))

    if request.user.is_authenticated:
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.title = request.POST['title']
                review.comment = request.POST['comment']
                review.rating = int(request.POST['rating'])
                review.product = product
                review.save()
                messages.success(request,
                                 'You have successfully added a review')
                return redirect('product_detail', product.id)
        else:
            form = ReviewForm()
        return render(request, 'products/product_detail.html', {"form": form})
    else:
        messages.error(request, 'Please sign in to leave a review')
        return redirect('account_login')


@login_required
def edit_review(request, product_id, review_id):
    '''
    got a hand with the review function here:
    https://www.youtube.com/watch?v=2av1F3BJHUc&t=295s
    '''
    """ edits a review on the site """
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        review = get_object_or_404(Review, product=product, pk=review_id)

        if request.user == review.user or request.user.is_superuser:
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    messages.success(request,
                                     'You have successfully \
                                     edited this review')
                    return redirect('product_details', product_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'reviews/edit_review.html', {'form': form})
        else:
            messages.error(request,
                           'You do not have permission to edit this review')
            return redirect('product_details', product_id)
    else:
        return redirect('account_login')


@login_required
def delete_review(request, product_id, review_id):
    '''
        got a hand with the review function here:
        https://www.youtube.com/watch?v=d4Pa6E2d2GA
    '''
    """ deletes a review on the site """
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        review = get_object_or_404(Review, product=product, pk=review_id)

        if request.user == review.user:
            # permission to delete
            review.delete()
            messages.success(request,
                             'You have successfully deleted this review')
        return redirect('product_details', product_id)
    else:
        return redirect('account_login')