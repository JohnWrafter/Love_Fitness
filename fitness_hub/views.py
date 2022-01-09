from django.shortcuts import render

def Fitness(request):
    """ A view to return the index page """

    return render(request, 'fitness_hub/fitness_hub.html')
