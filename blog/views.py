from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import CommentForm, PostForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def blog(request):
    """ This view returns the blog page"""
    posts = Post.objects.all().order_by('timestamp')

    posts_paginator = Paginator(posts, 5)
    page_num = request.GET.get('page')
    page = posts_paginator.get_page(page_num)

    template = 'blog/blog.html'
    context = {
        'page': page,
        'posts': posts,
    }

    return render(request, template, context)


def blog_post(request, slug):
    """ This view returns individual blog posts"""
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('blog_post', slug=post.slug)
    else:
        form = CommentForm()

    template = 'blog/blog_post.html'
    context = {
        'post': post,
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_blog_post(request):
    """ Adds a blog post to the store """
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry, only store admin can do add a blog post')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            form.save()
            messages.success(request, 'Successfully added Blog Post!')
            return redirect(reverse('blog_post', args=[post.slug]))
        else:
            messages.error(request,
                           'Could not add post to site. \
                           Please ensure form is valid!')
    else:
        form = PostForm()

    template = 'blog/add_blog.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_blog_post(request, post_id):
    """ edits a blog post on the store """
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry, only store admin can do update a blog post')
        return redirect(reverse('home'))

    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            form.save()
            messages.success(request, 'Successfully Updated Blog Post!')
            return redirect(reverse('blog_post', args=[post.slug]))
        else:
            messages.error(request,
                           'Could not add post to site. \
                           Please ensure form is valid!')
    else:
        form = PostForm(instance=post)
        messages.info(request, f'You are editing {post.title}')

    template = 'blog/edit_blog.html'
    context = {
        'form': form,
        'post': post,
    }

    return render(request, template, context)


@login_required
def delete_blog_post(request, post_id):
    """ deletes a blog post on the site """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    blog_post = get_object_or_404(Post, pk=post_id)
    blog_post.delete()
    messages.success(request, 'Blog Post deleted!')

    return redirect(reverse('blog'))


@login_required
def delete_comment(request, comment_id):
    """ deletes a users comment on the site """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    messages.success(request, 'Comment successfully deleted!')

    return redirect(reverse('blog'))