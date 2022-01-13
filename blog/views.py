from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm, EditForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


class BlogView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    ordering = ['-post_date']


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BlogDetailView, self).get_context_data()
        likes = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = likes.total_likes()
        context['total_likes'] = 'total_likes'
        return context


class AddBlogView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_blog.html'


class UpdateBlogView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog/update_blog.html'


class DeleteBlogView(DeleteView):
    model = Post
    template_name = 'blog/delete_blog.html'
    success_url = reverse_lazy('home')