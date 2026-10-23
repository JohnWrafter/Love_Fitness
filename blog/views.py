"""
Views for blog app
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class AddBlogView(LoginRequiredMixin, CreateView):
    """
    A view to render the add blog page
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/add_blog.html'
    success_url = reverse_lazy('blog')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostAuthorOrStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        return (
            post.author_id == self.request.user.id
            or self.request.user.is_staff
        )


class UpdateBlogView(PostAuthorOrStaffMixin, UpdateView):
    """
    A view to render the update blog page
    """
    model = Post
    form_class = EditForm
    template_name = 'blog/update_blog.html'
    success_url = reverse_lazy('blog')


class DeleteBlogView(PostAuthorOrStaffMixin, DeleteView):
    """
    A view to delete a blog
    """
    model = Post
    template_name = 'blog/delete_blog.html'
    success_url = reverse_lazy('home')
