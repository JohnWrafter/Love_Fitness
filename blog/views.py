"""
Views for blog app
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.http import HttpResponseRedirect

# Internal:
from .models import Post
from .forms import PostForm, EditForm

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class BlogView(ListView):
    """
    A view to rnder the blog page
    """
    model = Post
    template_name = 'blog/blog.html'
    ordering = ['-post_date']


class BlogDetailView(DetailView):
    """
    A view to render the blog details page
    """
    model = Post
    template_name = 'blog/blog_detail.html'


class AddBlogView(CreateView):
    """
    A view to render the add blog page
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/add_blog.html'
    success_url = reverse_lazy('blog')
    success_message = reverse_lazy('Blog Added Successfully')


class UpdateBlogView(UpdateView):
    """
    A view to render the update blog page
    """
    model = Post
    form_class = EditForm
    template_name = 'blog/update_blog.html'


class DeleteBlogView(DeleteView):
    """
    A view to delete a blog
    """
    model = Post
    template_name = 'blog/delete_blog.html'
    success_url = reverse_lazy('home')
