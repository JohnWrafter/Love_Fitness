from django.shortcuts import render, get_object_or_404

from .models import UserProfile


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user)

    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)
