from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import Exercise, Nutrition

# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'plans/plans.html')


def plans_detail(request, plan_id):
    """ A view to show individual plan details """

    plan = get_object_or_404(Plan, pk=plan_id)

    context = {
        'plan': plan,
    }

    return render(request, 'plans/plans_detail.html', context)
