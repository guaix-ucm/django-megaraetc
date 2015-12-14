from django.shortcuts import render
from .models import SpectralTemplate, VPHSetup
from .models import PhotometricFilter

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import HttpResponse

from .forms import TargetForm, InstrumentForm
from .forms import AtmosphericConditionsForm, ObservationalSetupForm
# from numeric import thisisatest
from numeric import mag2flux
from numeric import *
from tkgui import *
# from tkgui import outtextinp
from tkgui import main
import tkgui

from justcalc import calc
from plot1 import plot_and_save


def compute5(request):
    sourcet_val = request.GET['stype']
    if sourcet_val == "P":
        size_val = 1.0
    else:
        size_val = request.GET['size']

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
    # else:
    #     resolvedline_val = "N"
    #     fline_val = 1e-13
    #     wline_val = 6562.8
    #     fwhmline_val = 6
    #     nfwhmline_val = 1.0
    #     cnfwhmline_val = 1.0



    pfilter = request.GET['pfilter']
    querybandc = PhotometricFilter.objects.filter(pk=pfilter).values()  # get row with the values at primary key
    bandc_val = querybandc[0]['name']
    entry_filter_cwl = querybandc[0]['cwl']
    entry_filter_width = querybandc[0]['path']

    # filtercdat = [entry_filter_cwl,entry_filter_width]
    # entry_filter_lambda_b = querybandc[0]['lambda_b']
    # entry_filter_lambda_e = querybandc[0]['lambda_e']
    # filtercar1 = ["0","0",entry_filter_lambda_b,entry_filter_lambda_e]


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
        exptime_val = float(request.GET['exptime'])
        nsbundles_val = int(request.GET['nfibers'])

        outputofcalc = calc(sourcet_val,inputcontt_val,mag_val,fc_val,size_val,fluxt_val,\
                            fline_val,wline_val,nfwhmline_val,cnfwhmline_val,
                            fwhmline_val,resolvedline_val,spect_val,bandc_val,\
                            om_val,vph_val,moon_val,airmass_val,seeing_val,exptime_val,nsbundles_val)


    # cleanstring = string1.replace("\'", '\n')
    # cleanstring = cleanstring.replace(",", ' ')
    # cleanstring = cleanstring.replace("u\n", '\n')
    # cleanstring = cleanstring[1:].replace("(", '\n')
    # cleanstring = cleanstring[:-1].replace("(", '\n')

    # cleanstring = [outtextstring,inputstring,coutputstring,loutputstring]

    return outputofcalc



### This is the working example ###
# def compute0(request):
#     # getvalue=request.GET['contmagval']
#     cleanvalue=float(getvalue)
#     return thisisatest(cleanvalue)

### LOGS OUTPUT
# def compute1(request):
#     om_val = request.GET['om_val']
#     sourcet_val = request.GET['stype']
#     # mag_val = float(request.GET['contmagval'])
#     netflux = 0
#     size_val = 0
#     seeingx = float(request.GET['seeing'])
#     pi = 3.14
#     fluxt_val = request.GET['iflux']
#     wline_val = float(request.GET['linewave'])
#     fline_val = float(request.GET['lineflux'])
#     fwhmline_val = float(request.GET['linefwhm'])
#
#     #
#     vph = request.GET['vph']
#     queryvph = VPHSetup.objects.filter(pk=vph).values()
#     vph_val = queryvph[0]['name']
#     #
#     #
#     pfilter = request.GET['pfilter']
#     queryfilter = PhotometricFilter.objects.filter(pk=pfilter).values()  # get row with the values at primary key
#     bandc_val = queryfilter[0]['name']   #get field value        return queryset
#     #
#     moon_val = request.GET['moonph']
#     airmass_val = float(request.GET['airmass'])
#     seeing_zenith = 10
#     fsky = 0
#     exptime_val = float(request.GET['exptime'])
#     npdark_val = 65500
#     nsbundles_val=int(request.GET['nfibers'])
#     nfwhmline_val=0
#     cnfwhmline_val=0
#     resolvedline_val = request.GET['rline']
#     bandsky=0
#
#     output1 = outtextinp(om_val, bandc_val,sourcet_val,mag_val,netflux,size_val,
#                       seeingx,pi,fluxt_val,wline_val, fline_val,fwhmline_val,
#                       vph_val,moon_val, airmass_val, seeing_zenith,fsky,
#                       exptime_val, npdark_val, nsbundles_val,nfwhmline_val,
#                       cnfwhmline_val,resolvedline_val, bandsky)
#     return output1
#
#
# def compute2(request):
#     sourcet_val = request.GET['stype']
#     fluxt_val = request.GET['iflux']
#
#     snline_all = 0
#     snline_fibre = 0
#     snline_pspp = 0
#     snline_1_aa = 0
#     snline_seeing = 0
#     snline_1 = 0
#     snline_spaxel = 0
#     snline_fibre1aa = 0
#     output2 = outtextoutl(fluxt_val,snline_all,snline_fibre,snline_pspp,snline_1_aa,sourcet_val,snline_seeing,snline_1,
#     snline_spaxel,snline_fibre1aa)
#
#     return output2
#
# def compute3(request):
#     sourcet_val = request.GET['stype']
#
#     nfibres = 0
#     nfib = 0
#     nfib1 = 0
#     sncont_p2sp_all = 0
#     sncont_1aa_all = 0
#     sncont_band_all = 0
#     sncont_p2sp_fibre = 0
#     sncont_1aa_fibre = 0
#     sncont_band_fibre = 0
#     sncont_p2sp_seeing = 0
#     sncont_1aa_seeing = 0
#     sncont_band_seeing = 0
#     sncont_p2sp_1 = 0
#     sncont_1aa_1 = 0
#     sncont_band_1 = 0
#     sncont_psp_pspp = 0
#     output3 = outtextoutc(sourcet_val,nfibres, nfib, nfib1, sncont_p2sp_all, \
#                           sncont_1aa_all,sncont_band_all,sncont_p2sp_fibre,\
#                           sncont_1aa_fibre,sncont_band_fibre,sncont_p2sp_seeing,\
#                           sncont_1aa_seeing, sncont_band_seeing,sncont_p2sp_1,\
#                           sncont_1aa_1,sncont_band_1,sncont_psp_pspp)
#
#     return output3

##############################################################################################################################
##############################################################################################################################


# def compute4(request):
#     inputmag = float(request.GET['contmagval'])
#     pfilter = float(request.GET['pfilter'])
#     queryset = PhotometricFilter.objects.filter(pk=pfilter).values()  # get row with the values at primary key
#     mvega=queryset[0]['mvega']  #get field value
#     fvega=float(queryset[0]['fvega'])   #get field value
#     # other query examples:
#         # queryset = PhotometricFilter.objects.all()    # get all
#         # queryset = PhotometricFilter.objects.get(pk=1)    # get row at primary key
#         # fvega=queryset    # show all
#         # fvega = PhotometricFilter.objects.get(pk=1)
#
#
#     output4 = mag2flux(mvega,fvega,inputmag)
#     output4 = format(output4, '.3e')
#     output4string = "flux = "+str(output4)+" cgs"
#     # output4 = str(fvega)
#
#     return output4string


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

    return render(request, 'etc/webmegaraetc-0.4.1.html', {
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
    return render(request, 'etc/webmegaraetc-0.4.1.html', {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        })


# LOADS THIS AFTER PRESSING "COMPUTE" in form.html and
# OUTPUT RESULTS in test.html
# FINAL STRING CLEANSING/FILTERING HERE
#
#
def etc_do(request):
    message = 'Nothing to see here'
    if request.method == 'GET':
        outputofcalc = compute5(request)
        #
        # GET relevant data
        vph = request.GET['vph']
        queryvph = VPHSetup.objects.filter(pk=vph).values()
        vph_val = queryvph[0]['name']
        spec = request.GET['spectype']
        queryspec = SpectralTemplate.objects.filter(pk=spec).values()
        entry_spec_name = queryspec[0]['name']

        if vph_val != '-empty-':
            x = outputofcalc['lamb']
            # x = [0,1,2]
            y = outputofcalc['sourcespectrum']
            # y = [0,1,2]
            label = entry_spec_name
        else:
            x = numpy.arange(1,100,1)
            y = numpy.arange(1,100,1)
            label = "none"
        graphic = plot_and_save(x,y,label)


        #
        tocheck = str(outputofcalc['outtext'])
        if not tocheck:
            outtextstring = "No warning."
        else:
            outtextstring = tocheck
        inputstring = str(outputofcalc['texti'])
        coutputstring = str(outputofcalc['textoc'])
        loutputstring = str(outputofcalc['textol'])

        return render(request, 'etc/result.html',
            context={
                      'outtext':outtextstring,
                      'textinput':inputstring,
                      'textcout':coutputstring,
                      'textlout':loutputstring,
                        'graphic':graphic,
                     }
                      )
    return HttpResponse(message)


def etc_tab(request):
    if request.method == 'GET':
        # myresult0 = compute0(request)
        # string1 = str(compute1(request))
        # myresult1 = string1.replace('\\n', '\n')    # This gets rid of the string \n and replaces it by a 'true' linebreak (which needs to be invoked by { result1|linebreaksbr } in result.html
        # string2 = str(compute2(request))
        # myresult2 = string2.replace('\\n', '\n')
        # string3 = str(compute3(request))
        # myresult3 = string3.replace('\\n', '\n')
        # string4 = str(compute4(request))
        # myresult4 = string4.replace('\\n', '\n')
        # fvega = "bleh"
        #
        outputofcalc = compute5(request)

        tocheck = str(outputofcalc['outtext'])
        if not tocheck:
            outtextstring = "No warning."
        else:
            outtextstring = tocheck
        inputstring = str(outputofcalc['texti'])
        coutputstring = str(outputofcalc['textoc'])
        loutputstring = str(outputofcalc['textol'])
        #
        # string5 = str(compute5(request))
        # myresult5 = string5.replace('\\n', '\n')

        return render(request, 'etc/tab.html',
            context={
                    # 'result0':myresult0,
                    #  'result1':myresult1,
                    #   'result2':myresult2,
                    #   'result3':myresult3,
                    #   'result4':myresult4,
                    #   'fvega':fvega,
                    #   # 'result5':myresult5
                      'outtext':outtextstring,
                      'textinput':inputstring,
                      'textcout':coutputstring,
                      'textlout':loutputstring
                     }
                      )
