from django.http import HttpResponse
from django.shortcuts import render

from .forms import AtmosphericConditionsForm, ObservationalSetupForm
from .forms import TargetForm, InstrumentForm
from .models import PhotometricFilter
from .models import SpectralTemplate, VPHSetup

# from obsolete.tkgui import *

from justcalc import calc
from plot1 import plot_and_save, plot_and_save2

import numpy
import os
import tempfile

def compute5(request):
    sourcet_val = request.GET['stype']
    if sourcet_val == "P":
        size_val = 1.0
    else:
        size_val = request.GET['size']

    tocheck = request.GET['contmagflux']
    if tocheck:
        inputcontt_val = "M"
    else:
        inputcontt_val = request.GET['contmagflux']
    if inputcontt_val == "M":
        mag_val = request.GET['contmagval']
        fc_val = 1e-16
    else:
        mag_val = 20.0
        fc_val = request.GET['contfluxval']


    fluxt_val = request.GET['iflux']
    if fluxt_val == "C":
        resolvedline_val = "N"
        fline_val = 1e-13
        wline_val = 6562.8
        fwhmline_val = 6
        nfwhmline_val = 1.0
        cnfwhmline_val = 1.0

    elif fluxt_val == "L" and request.GET['rline'] == "N":
        resolvedline_val = "N"
        fline_val = float(request.GET['lineflux'])
        wline_val = float(request.GET['linewave'])
        fwhmline_val = 6
        nfwhmline_val = float(request.GET['lineap'])
        cnfwhmline_val = float(request.GET['contap'])

    elif fluxt_val == "L" and request.GET['rline'] == "Y":
        resolvedline_val = "Y"
        fline_val = float(request.GET['lineflux'])
        wline_val = float(request.GET['linewave'])
        fwhmline_val = float(request.GET['linefwhm'])
        nfwhmline_val = float(request.GET['lineap'])
        cnfwhmline_val = float(request.GET['contap'])

    pfilter = request.GET['pfilter']
    querybandc = PhotometricFilter.objects.filter(pk=pfilter).values()  # get row with the values at primary key
    bandc_val = querybandc[0]['name']
    entry_filter_cwl = querybandc[0]['cwl']
    entry_filter_width = querybandc[0]['path']

    om_val = request.GET['om_val']
    vph = request.GET['vph']
    queryvph = VPHSetup.objects.filter(pk=vph).values()
    vph_val = queryvph[0]['name']
    if vph_val == '-empty-':        # Deals with -empty- VPH Setup
        # vph_val = 'MR-UB'
        outtext="WARNING: VPH Setup is -empty-! Choose a VPH."
        texti=" "
        textoc=" "
        textol=" "
        outputfilename="etc/static/etc/outputcalc.txt"
        with open(outputfilename, 'w') as f:
            print >> f, outtext
            print >> f, texti
            print >> f, textoc
            print >> f, textol
        outputofcalc = ({'outtext':outtext, 'texti':texti, 'textoc':textoc, 'textol':textol})
        # return outputofcalc
    else:
        entry_vph_fwhm = queryvph[0]['fwhm']
        entry_vph_disp = queryvph[0]['dispersion']
        entry_vph_deltab = queryvph[0]['deltab']
        entry_vph_lambdac = queryvph[0]['lambdac']
        entry_vph_relatedband = queryvph[0]['relatedband']
        entry_vph_lambdab = queryvph[0]['lambda_b']
        entry_vph_lambdae = queryvph[0]['lambda_e']
        entry_vph_specconf = queryvph[0]['specconf']

        vphfeatures = [entry_vph_fwhm,entry_vph_disp,entry_vph_deltab,entry_vph_lambdac,\
                       entry_vph_relatedband,entry_vph_lambdab,entry_vph_lambdae,entry_vph_specconf]
        # filtercar2 = ["0","0",entry_vph_lambdab,entry_vph_lambdae]

        spec = request.GET['spectype']
        queryspec = SpectralTemplate.objects.filter(pk=spec).values()
        entry_spec_name = queryspec[0]['name']
        entry_spec_path = queryspec[0]['path']
        spectdat = [entry_spec_name,entry_spec_path]
        spect_val = entry_spec_name

        moon_val = request.GET['moonph']
        airmass_val = float(request.GET['airmass'])
        seeing_val = float(request.GET['seeing'])
        numframes_val = float(request.GET['numframes'])
        exptimepframe_val = float(request.GET['exptimepframe'])
        nsbundles_val = int(request.GET['nfibers'])

        outputofcalc = calc(sourcet_val,inputcontt_val,mag_val,fc_val,size_val,fluxt_val,\
                            fline_val,wline_val,nfwhmline_val,cnfwhmline_val,
                            fwhmline_val,resolvedline_val,spect_val,bandc_val,\
                            om_val,vph_val,moon_val,airmass_val,seeing_val,\
                            numframes_val,exptimepframe_val,nsbundles_val)


    # cleanstring = string1.replace("\'", '\n')
    # cleanstring = cleanstring.replace(",", ' ')
    # cleanstring = cleanstring.replace("u\n", '\n')
    # cleanstring = cleanstring[1:].replace("(", '\n')
    # cleanstring = cleanstring[:-1].replace("(", '\n')

    # cleanstring = [outtextstring,inputstring,coutputstring,loutputstring]

    return outputofcalc

##############################################################################################################################
##############################################################################################################################
def basic(request):
    return render(request, 'etc/index.html')

def get_info(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form1 = TargetForm(request.GET)
        form2 = InstrumentForm(request.GET)
        form3 = AtmosphericConditionsForm(request.GET)
        form4 = ObservationalSetupForm(request.GET)
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

    return render(request, 'etc/webmegaraetc-0.4.2.html', {
                                             'form1': form1,
                                             'form2': form2,
                                             'form3': form3,
                                             'form4': form4,
                                             })

# LOAD THIS AFTER PUSHING "START" in index.html
def etc_form(request):
    form1 = TargetForm()
    form2 = InstrumentForm()
    form3 = AtmosphericConditionsForm()
    form4 = ObservationalSetupForm()
    return render(request, 'etc/webmegaraetc-0.4.2.html', {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        })


# LOADS THIS AFTER PRESSING "COMPUTE" webmegaraetc.html and
# OUTPUT RESULTS in result.html
# FINAL STRING CLEANSING/FILTERING HERE
#
#
def etc_do(request):
    message = 'Nothing to see here'
    if request.method == 'GET':
        outputofcalc = compute5(request)
        #
        #
        tocheck = str(outputofcalc['outtext'])
        if not tocheck:
            outtextstring = ""  #No warning.
        else:
            outtextstring = tocheck

        # GET relevant data
        vph = request.GET['vph']
        queryvph = VPHSetup.objects.filter(pk=vph).values()
        vph_val = queryvph[0]['name']
        spec = request.GET['spectype']
        queryspec = SpectralTemplate.objects.filter(pk=spec).values()
        entry_spec_name = queryspec[0]['name']

        if not tocheck:
            x = outputofcalc['lamb']
            y = outputofcalc['fc']
            label1 = entry_spec_name
            label2 = outputofcalc['mag_val']
            label3 = outputofcalc['bandc_val']

            x2 = outputofcalc['lamb']
            y2 = outputofcalc['pframesn_psp_asp']
            x2b = x2
            y2b = outputofcalc['allframesn_psp_asp']
            x2c = x2
            y2c = outputofcalc['pframesn_psp_asp_all']
            x2d = x2
            y2d = outputofcalc['allframesn_psp_asp_all']


            label2a = entry_spec_name
            label2b = vph_val
            label2c = outputofcalc['bandc_val']
        else:
            x = numpy.arange(1, 100, 1)
            y = numpy.arange(1, 100, 1)
            x2 = numpy.arange(1, 100, 1)
            y2 = numpy.arange(1, 100, 1)
            x2b = numpy.arange(1, 100, 1)
            y2b = numpy.arange(1, 100, 1)
            x2c = numpy.arange(1, 100, 1)
            y2c = numpy.arange(1, 100, 1)
            x2d = numpy.arange(1, 100, 1)
            y2d = numpy.arange(1, 100, 1)



            label1 = "none"
            label2 = 20.0   # Float
            label3 = "none"
            label2a = "none"
            label2b = "none"
            label2c = "none"
        # CREATE TEMPORARY FILE
        temp = tempfile.NamedTemporaryFile(suffix=".png", prefix="temp", dir="etc/static/etc/tmp/", delete=False)
        graphic = plot_and_save(temp.name, x, y, label1, label2, label3)
        temp2 = tempfile.NamedTemporaryFile(suffix=".png", prefix="temp", dir="etc/static/etc/tmp/", delete=False)
        graphic2 = plot_and_save2(temp2.name, x2, y2, x2b, y2b, x2c, y2c, x2d, y2d, label2a, label2b, label2c)

        # RENAME FILE PATH
        dirname, basename = os.path.split(graphic)
        newpath = '/static/etc/tmp/'
        graphic = os.path.join(newpath, basename)

        dirname2, basename2 = os.path.split(graphic2)
        newpath2 = '/static/etc/tmp/'
        graphic2 = os.path.join(newpath2, basename2)

        inputstring = str(outputofcalc['texti'])
        coutputstring = str(outputofcalc['textoc'])
        loutputstring = str(outputofcalc['textol'])

        return render(request, 'etc/result.html',
            context={
                      'outtext' : outtextstring,
                      'textinput' : inputstring,
                      'textcout' : coutputstring,
                      'textlout' : loutputstring,
                        'graphic' : graphic,
                        'graphic2' : graphic2
                     }
                      )
    return HttpResponse(message)


def etc_tab(request):
    if request.method == 'GET':
        outputofcalc = compute5(request)

        tocheck = str(outputofcalc['outtext'])
        if not tocheck:
            outtextstring = "No warning."
        else:
            outtextstring = tocheck
        inputstring = str(outputofcalc['texti'])
        coutputstring = str(outputofcalc['textoc'])
        loutputstring = str(outputofcalc['textol'])

        return render(request, 'etc/tab.html',
            context={
                      'outtext':outtextstring,
                      'textinput':inputstring,
                      'textcout':coutputstring,
                      'textlout':loutputstring
                     }
                      )
