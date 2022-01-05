""" Import Render function to render HTML pages """
from django.shortcuts import render

# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')

def contact(request):
    """ A view that returns a contact us page """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid:
            form.subject = request.POST['subject'],
            form.message = request.POST['message'],
            form.email = request.POST['email'],
            form.save()
            user_email = ''.join(form.email)
            messages.success(request,
                             f"Thanks { user_email }, Your message has been sent.\
                             We will be in touch shortly.")
            return redirect("home")
        else:
            messages.error(request,
                           'Error: something has gone wrong \
                            please try again later.')
            return redirect('home')
    else:
        form = ContactForm(request.form)

    template = 'home/contact_us.html'
    context = {
        'form': form,
    }

    return render(request,
                  template,
                  context)
