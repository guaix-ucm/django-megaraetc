from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import HttpResponse

from .forms import TargetForm, InstrumentForm
from .forms import AtmosphericConditionsForm, ObservationalSetupForm

def compute():
    return 320

def basic(request):
    return render(request, 'etc/index.html')

def get_info(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form1 = TargetForm(request.POST)
        form2 = InstrumentForm(request.POST)
        form3 = AtmosphericConditionsForm(request.POST)
        form4 = ObservationalSetupForm(request.POST)
        # check whether it's valid:
        if form1.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            res = compute()
            #return HttpResponseRedirect(reverse('etc:result', args=(res,)))
            return HttpResponse("Hello, world. %s" % (res, ))
            #return HttpResponseRedirect("/etc/result")
    


    # if a GET (or any other method) we'll create a blank form
    else:
        form1 = TargetForm()
        form2 = InstrumentForm()
        form3 = AtmosphericConditionsForm()
        form4 = ObservationalSetupForm()

    return render(request, 'etc/form.html', {'form1': form1, 
                                             'form2': form2,
                                             'form3': form3,
                                             'form4': form4,
                                             })

def etc_form(request):

    form1 = TargetForm()
    form2 = InstrumentForm()
    form3 = AtmosphericConditionsForm()
    form4 = ObservationalSetupForm()

    return render(request, 'etc/form.html', {'form1': form1, 
                                             'form2': form2,
                                             'form3': form3,
                                             'form4': form4,
                                             })


def etc_do(request):
    message = 'Nothing to see here'
    if request.method == 'GET':
        return render(request, 'etc/result.html')
    return HttpResponse(message)


