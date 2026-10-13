"""
Views for home page
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render

# Internal:
from blog.models import Post
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def index(request):
    """
    A view to return the index page
    """
    recent_posts = Post.objects.order_by('-post_date')[:3]

    return render(request, 'home/index.html', {'recent_posts': recent_posts})
