from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse

from .forms import AtmosphericConditionsForm, ObservationalSetupForm
from .forms import TargetForm, InstrumentForm
from .forms import OutputSetupForm, UploadFileForm
from .models import PhotometricFilter, SeeingTemplate
from .models import SpectralTemplate, VPHSetup
# from .models import MyModel #, Document

from justcalc import calc
# from plot1 import plot_and_save_new, plot_and_save2_new
from plot1_bokeh import bokehplot1

import numpy
# import matplotlib
# matplotlib.use('Agg')
#
# import mpld3
# from mpld3 import plugins
# /home/pica/Documents/virt_django/django_megara

import time
from time import strftime
import os

from django.conf import settings #or from my_project import settings

def compute5(request):
    print request.POST['stype']
    print '### LOG: Entered compute5'

    if request.POST['stype'] == 'P':
        isize_val = 'A'
        size_val = 1.0
        radius_val = 1.0
    else:
        if request.POST['isize'] == 'A':
            isize_val = request.POST['isize']
            size_val = request.POST['size']
            radius_val = 1.0
        else:
            isize_val = request.POST['isize']
            radius_val = float(request.POST['radius'])
            size_val = numpy.pi * (radius_val ** 2)
    mag_val = float(request.POST['contmagval']) if request.POST['contmagflux'] == 'M' else 20.0
    fc_val = 1e-16 if request.POST['contmagflux'] == 'M' else float(request.POST['contfluxval'])

    fluxt_val = request.POST['iflux']
    if fluxt_val == "C":
        resolvedline_val = "N"
        fline_val = 1e-13
        wline_val = 6562.8
        fwhmline_val = 6
        nfwhmline_val = 1.0
        cnfwhmline_val = 1.0

    else:
        fline_val = float(request.POST['lineflux'])
        wline_val = float(request.POST['linewave'])
        nfwhmline_val = float(request.POST['lineap'])
        cnfwhmline_val = float(request.POST['contap'])
        if fluxt_val == "L" and request.POST['rline'] == "N":
            resolvedline_val = "N"
            fwhmline_val = 6

        elif fluxt_val == "L" and request.POST['rline'] == "Y":
            resolvedline_val = "Y"
            fwhmline_val = float(request.POST['linefwhm'])

    querybandc = PhotometricFilter.objects.filter(pk=request.POST[
        'pfilter']).values()  # get row with the values at primary key
    bandc_val = querybandc[0]['name']
    # entry_filter_cwl = querybandc[0]['cwl']
    # entry_filter_width = querybandc[0]['path']

    queryvph = VPHSetup.objects.filter(pk=request.POST['vph']).values()
    vph_val = queryvph[0]['name']

    if vph_val == '-empty-':  # Deals with -empty- VPH Setup
        # vph_val = 'MR-UB'
        outtext = "WARNING: VPH Setup is -empty-! Choose a VPH."
        texti = " "
        textoc = " "
        textol = " "
    else:
        entry_vph_fwhm = queryvph[0]['fwhm']
        entry_vph_disp = queryvph[0]['dispersion']
        entry_vph_deltab = queryvph[0]['deltab']
        entry_vph_lambdac = queryvph[0]['lambdac']
        entry_vph_relatedband = queryvph[0]['relatedband']
        entry_vph_lambdab = queryvph[0]['lambda_b']
        entry_vph_lambdae = queryvph[0]['lambda_e']
        entry_vph_specconf = queryvph[0]['specconf']

        # vphfeatures = [entry_vph_fwhm,entry_vph_disp,entry_vph_deltab,entry_vph_lambdac,\
        #                entry_vph_relatedband,entry_vph_lambdab,entry_vph_lambdae,entry_vph_specconf]
        # filtercar2 = ["0","0",entry_vph_lambdab,entry_vph_lambdae]

        spec = request.POST['spectype']
        if fluxt_val == "L":
            if spec == '7':  # NGC1068
                spec = '47'  # NGC1068 (smooth)
            elif spec == '20':  # Orion
                spec = '48'  # Orion (smooth)
            elif spec == '21':  # PN
                spec = '49'  # PN (smooth)
            elif spec == '6':  # Sc
                spec = '50'  # Sc (smooth)
            elif spec == '9':  # Starburst1
                spec = '51'  # Starburst1 (smooth)
            elif spec == '10':  # Starburst2
                spec = '52'  # Starburst2 (smooth)
            elif spec == '11':  # Starburst3
                spec = '53'  # Starburst3 (smooth)
            elif spec == '12':  # Starburst4
                spec = '54'  # Starburst4 (smooth)
            elif spec == '13':  # Starburst5
                spec = '55'  # Starburst5 (smooth)
            elif spec == '14':  # Starburst6
                spec = '56'  # Starburst6 (smooth)
            elif spec == '19':  # Sy2
                spec = '57'  # Sy2 (smooth)
        queryspec = SpectralTemplate.objects.filter(pk=spec).values()
        entry_spec_name = queryspec[0]['name']
        spect_val = entry_spec_name

        skycond_val = request.POST['skycond']
        moon_val = request.POST['moonph']
        airmass_val = float(request.POST['airmass'])

        queryseeing = SeeingTemplate.objects.filter(pk=request.POST['seeing']).values()
        seeing_val = queryseeing[0]['name']

        numframes_val = float(request.POST['numframes'])

        # Cope for cmode variations
        cmode_val = request.POST['cmode']
        if cmode_val == 'T':
            exptimepframe_val = float(request.POST['exptimepframe'])
            snr_val = 10
        elif cmode_val == 'S':
            exptimepframe_val = 3600
            snr_val = float(request.POST['exptimepframe'])

        nsbundles_val = int(request.POST['nsbundles'])

        plotflag_val = request.POST['plotflag']

        if request.POST['stype'] == 'P' and request.POST['batchyesno']=='batchyes':
            thebatchdata = request.POST['comment']
            batchyesno_val = request.POST['batchyesno']
            print batchyesno_val
        else:
            batchyesno_val = 'batchno'
            print batchyesno_val
            thebatchdata = "empty,empty,empty,empty"


        outputofcalc = calc(request.POST['stype'],
                            request.POST['contmagflux'],
                            mag_val, fc_val,
                            isize_val,
                            size_val, radius_val,
                            fluxt_val,
                            fline_val, wline_val,
                            nfwhmline_val, cnfwhmline_val,
                            fwhmline_val, resolvedline_val,
                            spect_val, bandc_val,
                            request.POST['om_val'], vph_val,
                            skycond_val, moon_val, airmass_val, seeing_val,
                            cmode_val, snr_val,
                            numframes_val, exptimepframe_val, nsbundles_val,
                            plotflag_val, batchyesno_val, thebatchdata
                            )

    # cleanstring = string1.replace("\'", '\n')
    # cleanstring = cleanstring.replace(",", ' ')
    # cleanstring = cleanstring.replace("u\n", '\n')
    # cleanstring = cleanstring[1:].replace("(", '\n')
    # cleanstring = cleanstring[:-1].replace("(", '\n')

    # cleanstring = [outtextstring,inputstring,coutputstring,loutputstring]
    print 'LOG: About to leave compute5 and return outputofcalc'
    # print outputofcalc
    return outputofcalc


##############################################################################
##############################################################################


def basic(request):
    return render(request, 'etc/index.html')


def get_info(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form1 = TargetForm(request.GET)
        formU = UploadFileForm(request.GET)
        form2 = InstrumentForm(request.GET)
        form3 = AtmosphericConditionsForm(request.GET)
        form4 = ObservationalSetupForm(request.GET)
        form5 = OutputSetupForm(request.GET)

    # if a GET (or any other method) we'll create a blank form
    else:
        form1 = TargetForm()
        formU = UploadFileForm()
        form2 = InstrumentForm()
        form3 = AtmosphericConditionsForm()
        form4 = ObservationalSetupForm()
        form5 = OutputSetupForm()

    return render(request, 'etc/webmegaraetc-1.0.1.html', {
        'form1': form1,
        'formU': formU,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'form5': form5,
    })


# LOADS THIS AFTER PUSHING "START" in index.html
def etc_form(request):
    form1 = TargetForm()
    formU = UploadFileForm()
    form2 = InstrumentForm()
    form3 = AtmosphericConditionsForm()
    form4 = ObservationalSetupForm()
    form5 = OutputSetupForm()

    total_formu = {'form1': form1,
                   'formU': formU,
                   'form2': form2,
                   'form3': form3,
                   'form4': form4,
                   'form5': form5,
                   }

    return render(request, 'etc/webmegaraetc-1.0.1.html', total_formu)

########################
# ON HOLD UNTIL I FIND A GOOD WAY TO UPLOAD FILES
# MIGRATING MODELS DIDN'T WORK EITHER.
#
########################
def uploadView(request):
    # phase = get_object_or_404(Phase, pk=int(phase_id))
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        form = UploadFileForm(request.POST, request.FILES)
        # print dir(request)
        formg = TargetForm(request.POST)
        print form
        print formg['pfilter']

        print settings.MEDIA_ROOT
        print ""
        print "REQUEST.POST=", request.POST
        # print request.META
        # print request.encoding
        print (form.errors)
        print ''
        print 'OK UP TO HERE'
        print request.FILES
        print 'REQUEST FILES=', request.FILES['myfile']
        print ''
        if form.is_valid():
            print 'VALID'
            # newdoc = MyModel(filename = request.FILES['myfile'])
            # newdoc.save()
            # doc_to_save = request.FILES['fileupload']
            # filename = doc_to_save._get_name()
            # fd = open('uploads/'+str(filename),'wb')
            # for chunk in doc_to_save.chunks():
            #     fd.write(chunk)
            # fd.close()
            # return HttpResponseRedirect(reverse('uploadView'))
            return HttpResponseRedirect('/success/url/')
        else:
            print 'WARNING: INVALID FORM!'
            print (form.errors)
            form = UploadFileForm()
        # documents = Document.objects.filter(phase=phase_id)

    return render(request, 'etc/upload.html', {'form': form})


##############################################
##############################################
### PERFORM CALCULATIONS.
### THIS RETURNS THE OUTPUT IN JSON FORMAT AND IS USED IN THE JS FILE
### FINAL STRING CLEANSING/FILTERING HERE
###
#
def etc_do(request):
    if request.method == 'GET':
        # import matplotlib.pyplot as plt
        # import mpld3
        # from mpld3 import plugins, utils
        #
        # plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
        # mpld3.save_html()
        return HttpResponse("<html><body>The GET method works!</body></html>")

    elif request.method == 'POST':
        print '### LOG: ETC_DO'
        start_time = time.time()
        start_time_string = time.strftime("%H:%M:%S")
        print 'Start time: ', str(start_time)
        print 'Date time: ', start_time_string

        ##############################################
        ##############################################
        ### ATTEMPT TO PRINT UPLOADED FILENAME (TEST)
        # up = uploadView(request)

        print request.body

        ##############################################
        ##############################################
        ### LAUNCH COMPUTATION
        if request.POST['stype'] == 'P' and request.POST['batchyesno']=='batchyes':
            print request.POST['batchyesno']
            print request.POST['comment']

        outputofcalc = compute5(request)
        print '### LOG: ETC_DO: OUTPUTOFCALC SUCCESSFULLY COMPUTED'

        ##############################################
        ##############################################

        tocheck = str(outputofcalc['outtext'])
        if not tocheck:
            outtextstring = ""  # No warning.
        else:
            outtextstring = tocheck

        ##############################################
        ### OUTPUT TEXT
        ##############################################
        inputstring = '<br /><p>' + str(outputofcalc['texti']) + '</p>'
        coutputstring = '<br /><p>' + str(outputofcalc['textoc']) + '</p>'
        loutputstring = '<br /><p>' + str(outputofcalc['textol']) + '</p>'
        textcalcstring = '<br /><table border=1 id="mathtextid"><tr><td>' + str(
            outputofcalc['textcalc']) + '</td></tr></table>'

        # Suck out relevant data from database
        vph = request.POST['vph']
        queryvph = VPHSetup.objects.filter(pk=vph).values()
        vph_val = queryvph[0]['name']
        vph_minval = queryvph[0]['lambda_b']
        vph_maxval = queryvph[0]['lambda_e']
        spec = request.POST['spectype']
        queryspec = SpectralTemplate.objects.filter(pk=spec).values()
        entry_spec_name = queryspec[0]['name']

        ################################################################
        ########################## GRAPHICS ############################
        ################################################################

        plotflag_val = request.POST['plotflag']

        if plotflag_val == 'yes':
            # First, prepare variables to be plotted
            # Check if computation outputs are conform
            if not tocheck:
                x = outputofcalc['lamb']
                y = outputofcalc['fc'] #+ outputofcalc['fs']
                ysky = outputofcalc['fs']
                label1 = entry_spec_name
                label2 = outputofcalc['mag_val']
                label3 = outputofcalc['bandc_val']
                lc = outputofcalc['lambdaeff']
                sourcet = outputofcalc['sourcet_val']
                fluxt = outputofcalc['fluxt_val']

                x2 = x
                x2b = x2
                x2c = x2
                x2d = x2

                if outputofcalc['fluxt_val'] == 'L':
                    y2 = outputofcalc['pframesn_pervoxel_fiber']
                    y2b = outputofcalc['allframesn_pervoxel_fiber']
                    y2c = outputofcalc['pframesn_pervoxel_all']
                    y2d = outputofcalc['allframesn_pervoxel_all']
                else:
                    y2 = outputofcalc['pframesn_pervoxel_c']
                    y2b = outputofcalc['allframesn_pervoxel_c']
                    y2c = outputofcalc['pframesn_pervoxel_cr1']
                    y2d = outputofcalc['allframesn_pervoxel_cr1']

                label2a = entry_spec_name
                label2b = vph_val
                label2c = outputofcalc['bandc_val']
            else:
                x = numpy.arange(1, 1001, 1)
                y = numpy.arange(1, 1001, 1)
                ysky = numpy.arange(1, 1001, 1)
                x2 = numpy.arange(1, 1001, 1)
                y2 = numpy.arange(1, 1001, 1)
                x2b = numpy.arange(1, 1001, 1)
                y2b = numpy.arange(1, 1001, 1)
                x2c = numpy.arange(1, 1001, 1)
                y2c = numpy.arange(1, 1001, 1)
                x2d = numpy.arange(1, 1001, 1)
                y2d = numpy.arange(1, 1001, 1)

                label1 = "none"
                label2 = 20.0  # Float
                label3 = "none"
                lc = 0
                sourcet = "none"
                fluxt = "none"

                label2a = "none"
                label2b = "none"
                label2c = "none"

            # More things to check
            if not tocheck:
                x3 = outputofcalc['wline_val']
                y3 = outputofcalc['fwhmline_val']
                z3 = outputofcalc['fline_val']
            else:
                x3 = 0
                y3 = 0
                z3 = 0

            # LEGACY CODE (MPLD3)
            # figura = plot_and_save_new('', x, y, x3, y3, z3,
            #                            vph_minval, vph_maxval,
            #                            label1, label2, label3)
            # html = mpld3.fig_to_html(figura)
            # html += mpld3.fig_to_html(figura2)
            # html = html.replace("None", "")  # No se xq introduce string None

            thescript, thediv = bokehplot1(sourcet,
                                           x, y, ysky, x3, y3, z3,
                                           vph_minval, vph_maxval,
                                           label1, label2, label3,
                                           x2, y2, x2b, y2b,
                                           x2c, y2c, x2d, y2d,
                                           label2a, label2b, label2c,
                                           fluxt,
                                           lc)
        else:
            thescript = ""
            thediv = ""

        html = ""
        ################################################################
        ################################################################
        ################################################################

        # Check variables and format them to strings
        if not tocheck:
            om_val_string = str(outputofcalc['om_val'])
            bandc_val_string = str(outputofcalc['bandc_val'])
            sourcet_val_string = str(outputofcalc['sourcet_val'])
            if sourcet_val_string == 'E':
                sourcet_val_string = 'Extended'
            else:
                sourcet_val_string = 'Point'
            mag_val_string = str('%.2f' % outputofcalc['mag_val'])
            netflux_string = '%.3e' % outputofcalc['netflux']
            size_val_string = str('%.2f' % outputofcalc['size_val'])
            radius_val_string = str('%.2f' % outputofcalc['radius_val'])
            seeingx_string = str(outputofcalc['seeingx'])
            fluxt_val_string = outputofcalc['fluxt_val']
            if fluxt_val_string == "L":
                fluxt_name_string = 'Line+Continuum'
            else:
                fluxt_name_string = 'Continuum'
            wline_val_string = str(outputofcalc['wline_val'])
            fline_val_string = str(outputofcalc['fline_val'])
            fwhmline_val_string = str(outputofcalc['fwhmline_val'])
            vph_val_string = str(outputofcalc['vph_val'])
            skycond_val_string = str(outputofcalc['skycond_val'])
            moon_val_string = str(outputofcalc['moon_val'])
            airmass_val_string = str(outputofcalc['airmass_val'])
            seeing_zenith_string = str(outputofcalc['seeing_zenith'])
            fcont_string = '%.3e' % outputofcalc['fcont']
            fsky_string = '%.3e' % outputofcalc['fsky']
            numframe_val = outputofcalc['numframe_val']
            numframe_val_string = "{0:.0f}".format(float(numframe_val))
            exptimepframe_val_string = str(outputofcalc['exptimepframe_val'])
            exptime_val_string = str(outputofcalc['exptime_val'])
            npdark_val_string = str(outputofcalc['npdark_val'])
            nsbundles_val_string = str(outputofcalc['nsbundles_val'])
            nfwhmline_val_string = str(outputofcalc['nfwhmline_val'])
            cnfwhmline_val_string = str(outputofcalc['cnfwhmline_val'])
            resolvedline_val_string = str(outputofcalc['resolvedline_val'])
            bandsky_string = str(outputofcalc['bandsky'])

            sourcespectrum_string = str(outputofcalc['sourcespectrum'])
            lamb_string = str(outputofcalc['lamb'])
            spect_val_string = str(outputofcalc['spect_val'])
            fc_string = str(outputofcalc['fc'])
            # pframesn_psp_asp_string = str(outputofcalc['pframesn_psp_asp'])
            # allframesn_psp_asp_string = str(outputofcalc['pframesn_psp_asp'])
            # pframesn_psp_asp_all_string = str(outputofcalc['pframesn_psp_asp_all'])
            # allframesn_psp_asp_all_string = str(outputofcalc['allframesn_psp_asp_all'])

            nfibres_string = str(outputofcalc['nfibres'])
            nfib_string = str(outputofcalc['nfib'])
            nfib1def_string = str(outputofcalc['nfib1def'])
            sncont_p2sp_all_string = "{0:.2f}".format(
                float(outputofcalc['sncont_p2sp_all']) / 2)
            tsncont_p2sp_all_val = float(outputofcalc['tsncont_p2sp_all'] / 2)
            tsncont_p2sp_all_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_p2sp_all']) / 2)
            sncont_pspfwhm_all_string = "{0:.2f}".format(
                float(outputofcalc['sncont_p2sp_all']))
            tsncont_pspfwhm_all_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_p2sp_all']))
            sncont_1aa_all_string = "{0:.2f}".format(
                float(outputofcalc['sncont_1aa_all']))
            tsncont_1aa_all_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_1aa_all']))
            sncont_band_all_string = "{0:.2f}".format(
                float(outputofcalc['sncont_band_all']))
            tsncont_band_all_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_band_all']))
            sncont_p2sp_fibre_string = "{0:.2f}".format(
                float(outputofcalc['sncont_p2sp_fibre']))
            tsncont_p2sp_fibre_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_p2sp_fibre']))
            sncont_1aa_fibre_string = "{0:.2f}".format(
                float(outputofcalc['sncont_1aa_fibre']))
            tsncont_1aa_fibre_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_1aa_fibre']))
            sncont_band_fibre_string = str(outputofcalc['sncont_band_fibre'])
            tsncont_band_fibre_string = str(outputofcalc['tsncont_band_fibre'])
            sncont_p2sp_seeing_string = "{0:.2f}".format(
                float(outputofcalc['sncont_p2sp_seeing']))
            tsncont_p2sp_seeing_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_p2sp_seeing']))
            sncont_1aa_seeing_string = "{0:.2f}".format(
                float(outputofcalc['sncont_1aa_seeing']))
            tsncont_1aa_seeing_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_1aa_seeing']))
            sncont_band_seeing_string = "{0:.2f}".format(
                float(outputofcalc['sncont_band_seeing']))
            tsncont_band_seeing_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_band_seeing']))
            sncont_p2sp_1_string = "{0:.2f}".format(
                float(outputofcalc['sncont_p2sp_1']))
            tsncont_p2sp_1_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_p2sp_1']))
            sncont_1aa_1_string = "{0:.2f}".format(
                float(outputofcalc['sncont_1aa_1']))
            tsncont_1aa_1_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_1aa_1']))
            sncont_band_1_string = "{0:.2f}".format(
                float(outputofcalc['sncont_band_1']))
            tsncont_band_1_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_band_1']))
            sncont_psp_pspp_string = "{0:.2f}".format(
                float(outputofcalc['sncont_psp_pspp']))
            tsncont_psp_pspp_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_psp_pspp']))
            sncont_psp_pspp2_string = "{0:.2f}".format(
                float(outputofcalc['sncont_psp_pspp'] * 2))
            tsncont_psp_pspp2_string = "{0:.2f}".format(
                float(outputofcalc['tsncont_psp_pspp'] * 2))
            lambdaeff_string = str(outputofcalc['lambdaeff'])

            snline_all_string = "{0:.2f}".format(
                float(outputofcalc['snline_all']))
            tsnline_all_string = "{0:.2f}".format(
                float(outputofcalc['tsnline_all']))
            snline_fibre_string = "{0:.2f}".format(
                float(outputofcalc['snline_fibre']))
            tsnline_fibre_string = "{0:.2f}".format(
                float(outputofcalc['tsnline_fibre']))
            snline_pspp_string = "{0:.2f}".format(
                float(outputofcalc['snline_pspp']))
            tsnline_pspp_string = "{0:.2f}".format(
                float(outputofcalc['tsnline_pspp']))
            snline_1_aa_string = "{0:.2f}".format(
                float(outputofcalc['snline_1_aa']))
            tsnline_1_aa_string = "{0:.2f}".format(
                float(outputofcalc['tsnline_1_aa']))
            snline_seeing_string = str(outputofcalc['snline_seeing'])
            tsnline_seeing_string = "{0:.2f}".format(
                float(outputofcalc['tsnline_seeing']))
            snline_1_string = str(outputofcalc['snline_1'])
            tsnline_1_string = "{0:.2f}".format(
                float(outputofcalc['tsnline_1']))
            snline_voxel_string = "{0:.2f}".format(
                float(outputofcalc['snline_voxel']))
            tsnline_voxel_string = "{0:.2f}".format(
                float(outputofcalc['tsnline_voxel']))
            snline_fibre1aa_string = "{0:.2f}".format(
                float(outputofcalc['snline_fibre1aa']))
            tsnline_fibre1aa_string = "{0:.2f}".format(
                float(outputofcalc['tsnline_fibre1aa']))

            seeing_centermean_val = outputofcalc['seeing_centermean']
            seeing_centermean_string = str(seeing_centermean_val)
            seeing_ring1mean_val = outputofcalc['seeing_ring1mean']
            seeing_ring1mean_string = str(seeing_ring1mean_val)
            seeing_ring2mean_val = outputofcalc['seeing_ring2mean']
            seeing_ring2mean_string = str(seeing_ring2mean_val)
            seeing_total_val = outputofcalc['seeing_total']
            seeing_total_string = str(seeing_total_val)

            seeing_cr1_val = seeing_centermean_val + seeing_ring1mean_val
            seeing_cr1_string = "{0:.2f}".format(seeing_cr1_val)
            seeing_cr1r2_val = seeing_centermean_val + seeing_ring1mean_val + seeing_ring2mean_val
            seeing_cr1r2_string = "{0:.2f}".format(round(seeing_cr1r2_val))

            tsncont_centermean = "{0:.2f}".format(
                (seeing_centermean_val / 100) * tsncont_p2sp_all_val)
            tsncont_ring1mean = "{0:.2f}".format(
                (seeing_ring1mean_val / 100) * tsncont_p2sp_all_val)
            tsncont_ring2mean = "{0:.2f}".format(
                (seeing_ring2mean_val / 100) * tsncont_p2sp_all_val)
            tsncont_total = "{0:.2f}".format(
                (seeing_total_val / 100) * tsncont_p2sp_all_val)

            sncont_centerspaxel_voxel_val = outputofcalc[
                'sncont_centerspaxel_voxel']
            sncont_centerspaxel_voxel_string = "{0:.2f}".format(
                float(sncont_centerspaxel_voxel_val))
            sncont_r1spaxel_voxel_val = outputofcalc['sncont_r1spaxel_voxel']
            sncont_r1spaxel_voxel_string = "{0:.2f}".format(
                float(sncont_r1spaxel_voxel_val))
            sncont_r2spaxel_voxel_val = outputofcalc['sncont_r2spaxel_voxel']
            sncont_r2spaxel_voxel_string = "{0:.2f}".format(
                float(sncont_r2spaxel_voxel_val))

            sncont_cr1spaxels_voxel_val = outputofcalc[
                'sncont_cr1spaxels_voxel']
            sncont_cr1spaxels_voxel_string = "{0:.2f}".format(
                float(sncont_cr1spaxels_voxel_val))
            sncont_cr1r2spaxels_voxel_val = outputofcalc[
                'sncont_cr1r2spaxels_voxel']
            sncont_cr1r2spaxels_voxel_string = "{0:.2f}".format(
                float(sncont_cr1r2spaxels_voxel_val))
            #
            tsncont_centerspaxel_voxel_val = outputofcalc[
                'tsncont_centerspaxel_voxel']
            tsncont_centerspaxel_voxel_string = "{0:.2f}".format(
                float(tsncont_centerspaxel_voxel_val))
            tsncont_cr1spaxels_voxel_val = outputofcalc[
                'tsncont_cr1spaxels_voxel']
            tsncont_cr1spaxels_voxel_string = "{0:.2f}".format(
                float(tsncont_cr1spaxels_voxel_val))
            tsncont_cr1r2spaxels_voxel_val = outputofcalc[
                'tsncont_cr1r2spaxels_voxel']
            tsncont_cr1r2spaxels_voxel_string = "{0:.2f}".format(
                float(tsncont_cr1r2spaxels_voxel_val))

            sncont_centerspaxel_aa_val = outputofcalc['sncont_centerspaxel_aa']
            sncont_centerspaxel_aa_string = "{0:.2f}".format(
                float(sncont_centerspaxel_aa_val))
            sncont_cr1spaxels_aa_val = outputofcalc['sncont_cr1spaxels_aa']
            sncont_cr1spaxels_aa_string = "{0:.2f}".format(
                float(sncont_cr1spaxels_aa_val))
            sncont_cr1r2spaxels_aa_val = outputofcalc['sncont_cr1r2spaxels_aa']
            sncont_cr1r2spaxels_aa_string = "{0:.2f}".format(
                float(sncont_cr1r2spaxels_aa_val))
            #
            tsncont_centerspaxel_aa_val = outputofcalc[
                'tsncont_centerspaxel_aa']
            tsncont_centerspaxel_aa_string = "{0:.2f}".format(
                float(tsncont_centerspaxel_aa_val))
            tsncont_cr1spaxels_aa_val = outputofcalc['tsncont_cr1spaxels_aa']
            tsncont_cr1spaxels_aa_string = "{0:.2f}".format(
                float(tsncont_cr1spaxels_aa_val))
            tsncont_cr1r2spaxels_aa_val = outputofcalc[
                'tsncont_cr1r2spaxels_aa']
            tsncont_cr1r2spaxels_aa_string = "{0:.2f}".format(
                float(tsncont_cr1r2spaxels_aa_val))

            sncont_centerspaxel_all_val = outputofcalc[
                'sncont_centerspaxel_all']
            sncont_centerspaxel_all_string = "{0:.2f}".format(
                float(sncont_centerspaxel_all_val))
            sncont_cr1spaxels_all_val = outputofcalc['sncont_cr1spaxels_all']
            sncont_cr1spaxels_all_string = "{0:.2f}".format(
                float(sncont_cr1spaxels_all_val))
            sncont_cr1r2spaxels_all_val = outputofcalc[
                'sncont_cr1r2spaxels_all']
            sncont_cr1r2spaxels_all_string = "{0:.2f}".format(
                float(sncont_cr1r2spaxels_all_val))
            #
            tsncont_centerspaxel_all_val = outputofcalc[
                'tsncont_centerspaxel_all']
            tsncont_centerspaxel_all_string = "{0:.2f}".format(
                float(tsncont_centerspaxel_all_val))
            tsncont_cr1spaxels_all_val = outputofcalc['tsncont_cr1spaxels_all']
            tsncont_cr1spaxels_all_string = "{0:.2f}".format(
                float(tsncont_cr1spaxels_all_val))
            tsncont_cr1r2spaxels_all_val = outputofcalc[
                'tsncont_cr1r2spaxels_all']
            tsncont_cr1r2spaxels_all_string = "{0:.2f}".format(
                float(tsncont_cr1r2spaxels_all_val))

            npixx_p2sp_all_val = outputofcalc['npixx_p2sp_all']
            npixx_p2sp_all_string = "{0:.2f}".format(npixx_p2sp_all_val)
            npixy_p2sp_all_val = outputofcalc['npixy_p2sp_all']
            npixy_p2sp_all_string = "{0:.2f}".format(npixy_p2sp_all_val)
            npixx_1aa_all_val = outputofcalc['npixx_1aa_all']
            npixx_1aa_all_string = "{0:.2f}".format(npixx_1aa_all_val)
            npixy_1aa_all_val = outputofcalc['npixy_1aa_all']
            npixy_1aa_all_string = "{0:.2f}".format(npixy_1aa_all_val)
            npixx_band_all_val = outputofcalc['npixx_band_all']
            npixx_band_all_string = "{0:.2f}".format(npixx_band_all_val)
            npixy_band_all_val = outputofcalc['npixy_band_all']
            npixy_band_all_string = "{0:.2f}".format(npixy_band_all_val)
            npixx_p2sp_fibre_val = outputofcalc['npixx_p2sp_fibre']
            npixx_p2sp_fibre_string = "{0:.2f}".format(npixx_p2sp_fibre_val)
            npixy_p2sp_fibre_val = outputofcalc['npixy_p2sp_fibre']
            npixy_p2sp_fibre_string = "{0:.2f}".format(npixy_p2sp_fibre_val)
            npixx_1aa_fibre_val = outputofcalc['npixx_1aa_fibre']
            npixx_1aa_fibre_string = "{0:.2f}".format(npixx_1aa_fibre_val)
            npixy_1aa_fibre_val = outputofcalc['npixy_1aa_fibre']
            npixy_1aa_fibre_string = "{0:.2f}".format(npixy_1aa_fibre_val)
            npixx_band_fibre_val = outputofcalc['npixx_band_fibre']
            npixx_band_fibre_string = "{0:.2f}".format(npixx_band_fibre_val)
            npixy_band_fibre_val = outputofcalc['npixy_band_fibre']
            npixy_band_fibre_string = "{0:.2f}".format(npixy_band_fibre_val)
            npixx_p2sp_seeing_val = outputofcalc['npixx_p2sp_seeing']
            npixx_p2sp_seeing_string = "{0:.2f}".format(npixx_p2sp_seeing_val)
            npixy_p2sp_seeing_val = outputofcalc['npixy_p2sp_seeing']
            npixy_p2sp_seeing_string = "{0:.2f}".format(npixy_p2sp_seeing_val)
            npixx_1aa_seeing_val = outputofcalc['npixx_1aa_seeing']
            npixx_1aa_seeing_string = "{0:.2f}".format(npixx_1aa_seeing_val)
            npixy_1aa_seeing_val = outputofcalc['npixy_1aa_seeing']
            npixy_1aa_seeing_string = "{0:.2f}".format(npixy_1aa_seeing_val)
            npixx_band_seeing_val = outputofcalc['npixx_band_seeing']
            npixx_band_seeing_string = "{0:.2f}".format(npixx_band_seeing_val)
            npixy_band_seeing_val = outputofcalc['npixy_band_seeing']
            npixy_band_seeing_string = "{0:.2f}".format(npixy_band_seeing_val)
            npixx_p2sp_1_val = outputofcalc['npixx_p2sp_1']
            npixx_p2sp_1_string = "{0:.2f}".format(npixx_p2sp_1_val)
            npixy_p2sp_1_val = outputofcalc['npixy_p2sp_1']
            npixy_p2sp_1_string = "{0:.2f}".format(npixy_p2sp_1_val)
            npixx_1aa_1_val = outputofcalc['npixx_1aa_1']
            npixx_1aa_1_string = "{0:.2f}".format(npixx_1aa_1_val)
            npixy_1aa_1_val = outputofcalc['npixy_1aa_1']
            npixy_1aa_1_string = "{0:.2f}".format(npixy_1aa_1_val)
            npixx_band_1_val = outputofcalc['npixx_band_1']
            npixx_band_1_string = "{0:.2f}".format(npixx_band_1_val)
            npixy_band_1_val = outputofcalc['npixy_band_1']
            npixy_band_1_string = "{0:.2f}".format(npixy_band_1_val)
            npixx_psp_pspp_val = outputofcalc['npixx_psp_pspp']
            npixx_psp_pspp_string = "{0:.2f}".format(npixx_psp_pspp_val)
            npixy_psp_pspp_val = outputofcalc['npixy_psp_pspp']
            npixy_psp_pspp_string = "{0:.2f}".format(npixy_psp_pspp_val)

            sncont_pdp_fibre_val = outputofcalc['sncont_pdp_fibre']
            sncont_pdp_fibre_string = "{0:.2f}".format(
                float(sncont_pdp_fibre_val))
            tsncont_pdp_fibre_val = outputofcalc['tsncont_pdp_fibre']
            tsncont_pdp_fibre_string = "{0:.2f}".format(
                float(tsncont_pdp_fibre_val))
            npixx_pdp_fibre_val = outputofcalc['npixx_pdp_fibre']
            npixx_pdp_fibre_string = "{0:.2f}".format(
                float(npixx_pdp_fibre_val))
            npixy_pdp_fibre_val = outputofcalc['npixy_pdp_fibre']
            npixy_pdp_fibre_string = "{0:.2f}".format(
                float(npixy_pdp_fibre_val))

            sncont_psp_fibre_val = outputofcalc['sncont_psp_fibre']
            sncont_psp_fibre_string = "{0:.2f}".format(
                float(sncont_psp_fibre_val))
            tsncont_psp_fibre_val = outputofcalc['tsncont_psp_fibre']
            tsncont_psp_fibre_string = "{0:.2f}".format(
                float(tsncont_psp_fibre_val))
            npixx_psp_fibre_val = outputofcalc['npixx_psp_fibre']
            npixx_psp_fibre_string = "{0:.2f}".format(
                float(npixx_psp_fibre_val))
            npixy_psp_fibre_val = outputofcalc['npixy_psp_fibre']
            npixy_psp_fibre_string = "{0:.2f}".format(
                float(npixy_psp_fibre_val))

            sncont_psp_all_val = outputofcalc['sncont_psp_all']
            sncont_psp_all_string = "{0:.2f}".format(float(sncont_psp_all_val))
            tsncont_psp_all_val = outputofcalc['tsncont_psp_all']
            tsncont_psp_all_string = "{0:.2f}".format(
                float(tsncont_psp_all_val))
            npixx_psp_all_val = outputofcalc['npixx_psp_all']
            npixx_psp_all_string = "{0:.2f}".format(float(npixx_psp_all_val))
            npixy_psp_all_val = outputofcalc['npixy_psp_all']
            npixy_psp_all_string = "{0:.2f}".format(float(npixy_psp_all_val))

            cmode = outputofcalc['cmode_val']

            snr_val = outputofcalc['snr_val']
            snr_string = "{0:.2f}".format(snr_val)
            print "SNR = ", snr_string
            # snrpframe_val = snr_val / numpy.sqrt(numframe_val)
            snrpframe_val = outputofcalc['snrpframe_val']
            snrpframe_string = "{0:.2f}".format(snrpframe_val)

            etpframe_c_voxel_val = outputofcalc['etpframe_c_voxel_val']
            if etpframe_c_voxel_val < 1:
                etpframe_c_voxel_string = "< 1"
                # etpframe_c_voxel_string = "{0:.2f}".format(etpframe_c_voxel_val)
            else:
                etpframe_c_voxel_string = "{0:.0f}".format(etpframe_c_voxel_val)

            etallframe_c_voxel_val = outputofcalc['etallframe_c_voxel_val']
            if etallframe_c_voxel_val < 1:
                etallframe_c_voxel_string = "< 1"
                # etallframe_c_voxel_string = "{0:.2f}".format(etallframe_c_voxel_val)
            else:
                etallframe_c_voxel_string = "{0:.0f}".format(etallframe_c_voxel_val)

            etpframe_cr1_voxel_val = outputofcalc['etpframe_cr1_voxel_val']
            if etpframe_cr1_voxel_val < 1:
                etpframe_cr1_voxel_string = "< 1"
                # etpframe_cr1_voxel_string = "{0:.2f}".format(etpframe_cr1_voxel_val)
            else:
                etpframe_cr1_voxel_string = "{0:.0f}".format(etpframe_cr1_voxel_val)

            etallframe_cr1_voxel_val = outputofcalc['etallframe_cr1_voxel_val']
            if etallframe_cr1_voxel_val < 1:
                etallframe_cr1_voxel_string = "< 1"
                # etallframe_cr1_voxel_string = "{0:.2f}".format(etallframe_cr1_voxel_val)
            else:
                etallframe_cr1_voxel_string = "{0:.0f}".format(etallframe_cr1_voxel_val)

            etpframe_cr1r2_voxel_val = outputofcalc['etpframe_cr1r2_voxel_val']
            if etpframe_cr1r2_voxel_val < 1:
                etpframe_cr1r2_voxel_string = "< 1"
                # etpframe_cr1r2_voxel_string = "{0:.2f}".format(etpframe_cr1r2_voxel_val)
            else:
                etpframe_cr1r2_voxel_string = "{0:.0f}".format(etpframe_cr1r2_voxel_val)

            etallframe_cr1r2_voxel_val = outputofcalc['etallframe_cr1r2_voxel_val']
            if etallframe_cr1r2_voxel_val < 1:
                etallframe_cr1r2_voxel_string = "< 1"
                # etallframe_cr1r2_voxel_string = "{0:.2f}".format(etallframe_cr1r2_voxel_val)
            else:
                etallframe_cr1r2_voxel_string = "{0:.0f}".format(etallframe_cr1r2_voxel_val)

            etpframe_c_aa_val = outputofcalc['etpframe_c_aa_val']
            if etpframe_c_aa_val < 1:
                etpframe_c_aa_string = "< 1"
                # etpframe_c_aa_string = "{0:.2f}".format(etpframe_c_aa_val)
            else:
                etpframe_c_aa_string = "{0:.0f}".format(etpframe_c_aa_val)

            etallframe_c_aa_val = outputofcalc['etallframe_c_aa_val']
            if etallframe_c_aa_val < 1:
                etallframe_c_aa_string = "< 1"
                # etallframe_c_aa_string = "{0:.2f}".format(etallframe_c_aa_val)
            else:
                etallframe_c_aa_string = "{0:.0f}".format(etallframe_c_aa_val)

            etpframe_cr1_aa_val = outputofcalc['etpframe_cr1_aa_val']
            if etpframe_cr1_aa_val < 1:
                etpframe_cr1_aa_string = "< 1"
                # etpframe_cr1_aa_string = "{0:.2f}".format(etpframe_cr1_aa_val)
            else:
                etpframe_cr1_aa_string = "{0:.0f}".format(etpframe_cr1_aa_val)

            etallframe_cr1_aa_val = outputofcalc['etallframe_cr1_aa_val']
            if etallframe_cr1_aa_val < 1:
                etallframe_cr1_aa_string = "< 1"
                # etallframe_cr1_aa_string = "{0:.2f}".format(etallframe_cr1_aa_val)
            else:
                etallframe_cr1_aa_string = "{0:.0f}".format(etallframe_cr1_aa_val)

            etpframe_cr1r2_aa_val = outputofcalc['etpframe_cr1r2_aa_val']
            if etpframe_cr1r2_aa_val < 1:
                etpframe_cr1r2_aa_string = "< 1"
                # etpframe_cr1r2_aa_string = "{0:.2f}".format(etpframe_cr1r2_aa_val)
            else:
                etpframe_cr1r2_aa_string = "{0:.0f}".format(etpframe_cr1r2_aa_val)

            etallframe_cr1r2_aa_val = outputofcalc['etallframe_cr1r2_aa_val']
            if etallframe_cr1r2_aa_val <1:
                etallframe_cr1r2_aa_string = "< 1"
                # etallframe_cr1r2_aa_string = "{0:.2f}".format(etallframe_cr1r2_aa_val)
            else:
                etallframe_cr1r2_aa_string = "{0:.0f}".format(etallframe_cr1r2_aa_val)

            etpframe_c_all_val = outputofcalc['etpframe_c_all_val']
            if etpframe_c_all_val < 1:
                etpframe_c_all_string = "< 1"
                # etpframe_c_all_string = "{0:.2f}".format(etpframe_c_all_val)
            else:
                etpframe_c_all_string = "{0:.0f}".format(etpframe_c_all_val)

            etallframe_c_all_val = outputofcalc['etallframe_c_all_val']
            if etallframe_c_all_val < 1:
                etallframe_c_all_string = "< 1"
                # etallframe_c_all_string = "{0:.2f}".format(etallframe_c_all_val)
            else:
                etallframe_c_all_string = "{0:.0f}".format(etallframe_c_all_val)

            etpframe_cr1_all_val = outputofcalc['etpframe_cr1_all_val']
            if etpframe_cr1_all_val < 1:
                etpframe_cr1_all_string = "< 1"
                # etpframe_cr1_all_string = "{0:.2f}".format(etpframe_cr1_all_val)
            else:
                etpframe_cr1_all_string = "{0:.0f}".format(etpframe_cr1_all_val)

            etallframe_cr1_all_val = outputofcalc['etallframe_cr1_all_val']
            if etallframe_cr1_all_val < 1:
                etallframe_cr1_all_string = "< 1"
                # etallframe_cr1_all_string = "{0:.2f}".format(etallframe_cr1_all_val)
            else:
                etallframe_cr1_all_string = "{0:.0f}".format(etallframe_cr1_all_val)

            etpframe_cr1r2_all_val = outputofcalc['etpframe_cr1r2_all_val']
            if etpframe_cr1r2_all_val < 1:
                etpframe_cr1r2_all_string = "< 1"
                # etpframe_cr1r2_all_string = "{0:.2f}".format(etpframe_cr1r2_all_val)
            else:
                etpframe_cr1r2_all_string = "{0:.0f}".format(etpframe_cr1r2_all_val)

            etallframe_cr1r2_all_val = outputofcalc['etallframe_cr1r2_all_val']
            if etallframe_cr1r2_all_val < 1:
                etallframe_cr1r2_all_string = "< 1"
                # etallframe_cr1r2_all_string = "{0:.2f}".format(etallframe_cr1r2_all_val)
            else:
                etallframe_cr1r2_all_string = "{0:.0f}".format(etallframe_cr1r2_all_val)


                # etallframe_c_voxel_val = outputofcalc['etallframe_c_voxel_val']
                # etallframe_c_voxel_string = "{0:.0f}".format(etallframe_c_voxel_val)
                # etpframe_cr1_voxel_val = outputofcalc['etpframe_cr1_voxel_val']
                # etpframe_cr1_voxel_string = "{0:.0f}".format(etpframe_cr1_voxel_val)
                # etallframe_cr1_voxel_val = outputofcalc['etallframe_cr1_voxel_val']
                # etallframe_cr1_voxel_string = "{0:.0f}".format(etallframe_cr1_voxel_val)
                # etpframe_cr1r2_voxel_val = outputofcalc['etpframe_cr1r2_voxel_val']
                # etpframe_cr1r2_voxel_string = "{0:.0f}".format(etpframe_cr1r2_voxel_val)
                # etallframe_cr1r2_voxel_val = outputofcalc['etallframe_cr1r2_voxel_val']
                # etallframe_cr1r2_voxel_string = "{0:.0f}".format(etallframe_cr1r2_voxel_val)
                #
                # etpframe_c_aa_val = outputofcalc['etpframe_c_aa_val']
                # etpframe_c_aa_string = "{0:.0f}".format(etpframe_c_aa_val)
                # etallframe_c_aa_val = outputofcalc['etallframe_c_aa_val']
                # etallframe_c_aa_string = "{0:.0f}".format(etallframe_c_aa_val)
                # etpframe_cr1_aa_val = outputofcalc['etpframe_cr1_aa_val']
                # etpframe_cr1_aa_string = "{0:.0f}".format(etpframe_cr1_aa_val)
                # etallframe_cr1_aa_val = outputofcalc['etallframe_cr1_aa_val']
                # etallframe_cr1_aa_string = "{0:.0f}".format(etallframe_cr1_aa_val)
                # etpframe_cr1r2_aa_val = outputofcalc['etpframe_cr1r2_aa_val']
                # etpframe_cr1r2_aa_string = "{0:.0f}".format(etpframe_cr1r2_aa_val)
                # etallframe_cr1r2_aa_val = outputofcalc['etallframe_cr1r2_aa_val']
                # etallframe_cr1r2_aa_string = "{0:.0f}".format(etallframe_cr1r2_aa_val)
    
                # etpframe_c_all_val = outputofcalc['etpframe_c_all_val']
                # etpframe_c_all_string = "{0:.0f}".format(etpframe_c_all_val)
                # etallframe_c_all_val = outputofcalc['etallframe_c_all_val']
                # etallframe_c_all_string = "{0:.0f}".format(etallframe_c_all_val)
                # etpframe_cr1_all_val = outputofcalc['etpframe_cr1_all_val']
                # etpframe_cr1_all_string = "{0:.0f}".format(etpframe_cr1_all_val)
                # etallframe_cr1_all_val = outputofcalc['etallframe_cr1_all_val']
                # etallframe_cr1_all_string = "{0:.0f}".format(etallframe_cr1_all_val)
                # etpframe_cr1r2_all_val = outputofcalc['etpframe_cr1r2_all_val']
                # etpframe_cr1r2_all_string = "{0:.0f}".format(etpframe_cr1r2_all_val)
                # etallframe_cr1r2_all_val = outputofcalc['etallframe_cr1r2_all_val']
                # etallframe_cr1r2_all_string = "{0:.0f}".format(etallframe_cr1r2_all_val)
            
            if cmode == 'S':
                cmode_string = 'SNR to exposure time'

            elif cmode == 'T':
                cmode_string = 'Exposure time to SNR'

            outhead1string = '<hr /><span class="boldlarge">Calculation Mode: ' + cmode_string + '<br>Observing Mode: ' + om_val_string + ', VPH: ' + vph_val_string + ', Source Type: ' + sourcet_val_string + ' </span>' + \
                             '<br /><span class="italicsmall"> Computation time: ' + "{0:.1f}".format((time.time() - start_time)) + ' seconds; </span>'

            tablecoutstring = ''

            if fluxt_val_string == 'L':
                from output_tablelout import tablelout
                tableloutstring = tablelout(fluxt_val_string, wline_val_string,
                                            snline_pspp_string,
                                            tsnline_pspp_string,
                                            snline_voxel_string,
                                            tsnline_voxel_string,
                                            snline_fibre1aa_string,
                                            tsnline_fibre1aa_string,
                                            snline_fibre_string,
                                            tsnline_fibre_string,
                                            snline_all_string,
                                            tsnline_all_string)
            else:
                tableloutstring = '<hr />' + \
                                  'No line input<br /><br />'


            if sourcet_val_string == 'Point':
                inputfluxstring = '<tr><td>Input flux:</td><td>' + netflux_string + ' erg/s/cm$^{2}$/$\mathrm{\mathring A}$</td></tr>'
                resultfluxstring = '<tr><td>Continuum flux per arcsec$^{2}$ <br />within the seeing disk:"</td><td>' + fcont_string + ' erg/s/cm$^{2}$/$\mathrm{\mathring A}$/arcsec$^{2}$</td></tr>'
            else:
                inputfluxstring = '<tr><td>Input flux:</td><td>' + netflux_string + ' erg/s/cm$^{2}$/$\mathrm{\mathring A}$/arcsec$^{2}$</td></tr>'
                resultfluxstring = ''


            if om_val_string == 'MOS':
                switchstring = 'Sky-bundles:'
            elif om_val_string == 'LCB':
                switchstring = 'Sky-fibers:'

            if fluxt_val_string == 'L':
                addlinestring = '<tr><td>Resolved line?:</td><td>' + resolvedline_val_string + '</td></tr>' + \
                               '<tr><td>Line wavelength:</td><td>' + wline_val_string + ' AA</td></tr>' + \
                               '<tr><td>Line flux (integrated):</td><td>' + fline_val_string + ' erg/s/cm$^{2}$</td></tr>' + \
                               '<tr><td>Line FWHM:</td><td>' + fwhmline_val_string + ' AA</td></tr>'
            elif fluxt_val_string == 'C':
                addlinestring = ''

            if cmode == 'T':
                addstring0 = '<tr><td>Exptime per frame:</td><td>' + exptimepframe_val_string + ' s</td></tr>'
                addstringT = '<tr><td>Total exptime:</td><td>' + exptime_val_string + ' s</td></tr>'
                addstringS = ''
            elif cmode == 'S':
                addstring0 = ''
                addstringT = ''
                addstringS = '<tr><td>Total SNR:</td><td>' + snr_string + '</td></tr>'

            tableinputstring = '<table border=1>' + \
                               '<tr><td>INPUT PARAMETERS:</td><td></td></tr>' + \
                               '<tr><td>Calculation mode:</td><td>' + cmode_string + '</td></tr>' + \
                               '<tr><td>Source type:</td><td>' + sourcet_val_string + '</td></tr>' + \
                               '<tr><td>Area:</td><td>' + size_val_string + ' arcsec$^{2}$</td></tr>' + \
                               '<tr><td>Observing mode:</td><td>' + om_val_string + '</td></tr>' + \
                               '<tr><td>VPH:</td><td>' + vph_val_string + '</td></tr>' + \
                               '<tr><td>Input flux type:</td><td>' + fluxt_name_string + '</td></tr>' + \
                               '<tr><td>Source spectrum:</td><td>' + spect_val_string + '</td></tr>' + \
                               '<tr><td>Input continuum:</td><td>' + bandc_val_string + ' = ' + mag_val_string + 'mag</td></tr>' + \
                               inputfluxstring + \
                               resultfluxstring + \
                               addlinestring + \
                               '<tr><td>*Sky Condition:</td><td>' + skycond_val_string + '</td></tr>' + \
                               '<tr><td>Moon:</td><td>' + moon_val_string + '</td></tr>' + \
                               '<tr><td>Airmass: X=</td><td>' + airmass_val_string + '</td></tr>' + \
                               '<tr><td>Seeing(@X=1):</td><td>' + seeing_zenith_string + ' arcsec</td></tr>' + \
                               '<tr><td>Sky-flux(R,@X):</td><td>' + fsky_string + ' erg/s/cm$^{2}$/$\mathrm{\mathring A}$/arcsec$^{2}$</td></tr>' + \
                               '<tr><td>Seeing(@X):</td><td>' + seeingx_string + ' arcsec</td></tr>' + \
                               '<tr><td>*Observation:</td></td><td></tr>' + \
                               '<tr><td>Number of frames:</td><td>' + numframe_val_string + '</td></tr>' + \
                               addstring0 + \
                               addstringT + \
                               addstringS + \
                               '<tr><td>NP_Dark:</td><td>' + npdark_val_string + '</td></tr>' + \
                               '<tr><td>' + switchstring + '</td><td>' + nsbundles_val_string + '</td></tr>' + \
                               '</table><br />'

            # NOT USED BUT KEEP FOR TESTING
            tablecalcstring = '<br /><br />' + \
                              '<p id="mathid">Details of calculations (TEST):<br />' + \
                              '$$\\textrm{Radius of source, } R_{source} = ' + radius_val_string + '\\textrm{ arcsec}$$' + \
                              '$$\\textrm{Area of source, } \Omega_{source} = \pi \\times ' + radius_val_string + '^{2} = ' + size_val_string + '\\textrm{ arcsec}^{2}$$' + \
                              '$$\\textrm{Radius of one fiber, } R_{fiber} = 0.31 \\textrm{ arcsec}$$' + \
                              '$$\\textrm{Area of one fiber, } \Omega_{fiber} =  3\sqrt{3} \left( \\frac{R_{fiber}^{2}}{2} \\right)$$' + \
                              '$$\\textrm{Number of fibers used to measure sky} = \\frac{\Omega_{source}}{\Omega_{fiber}} = ' + nfibres_string + '$$' + \
                              '$$\\textrm{Area in which sky has been measured, } \Omega_{sky} = ' + nfibres_string + '\\times \Omega_{fiber}$$' + \
                              '</p>' + \
                              '<br /><br />'
            # print om_val_string
            # print 'PID = ', os.getpid()

            # NEW OUTPUT CONTINUUM TABLE FOR MOS AND LCB

            if cmode == 'T':
                if om_val_string == 'MOS' and sourcet_val_string == 'Point':
                    from output_table_MOS_P_T import tablenewpsfMPT
                    tablenewpsfstring = tablenewpsfMPT(lambdaeff_string,
                                                       seeingx_string,
                                                       exptimepframe_val_string,
                                                       exptime_val_string,
                                                       numframe_val_string,
                                                       seeing_centermean_string,
                                                       seeing_cr1_string,
                                                       sncont_centerspaxel_voxel_string,
                                                       sncont_cr1spaxels_voxel_string,
                                                       tsncont_centerspaxel_voxel_string,
                                                       tsncont_cr1spaxels_voxel_string,
                                                       sncont_centerspaxel_aa_string,
                                                       sncont_cr1spaxels_aa_string,
                                                       tsncont_centerspaxel_aa_string,
                                                       tsncont_cr1spaxels_aa_string,
                                                       sncont_centerspaxel_all_string,
                                                       sncont_cr1spaxels_all_string,
                                                       tsncont_centerspaxel_all_string,
                                                       tsncont_cr1spaxels_all_string
                                                       )

                elif om_val_string == 'MOS' and sourcet_val_string == 'Extended':
                    from output_table_MOS_E_T import tablenewpsfMET
                    tablenewpsfstring = tablenewpsfMET(lambdaeff_string,
                                                       seeingx_string,
                                                       exptimepframe_val_string,
                                                       exptime_val_string,
                                                       numframe_val_string,
                                                       nfibres_string,
                                                       sncont_centerspaxel_voxel_string,
                                                       sncont_cr1spaxels_voxel_string,
                                                       sncont_pspfwhm_all_string,
                                                       tsncont_centerspaxel_voxel_string,
                                                       tsncont_cr1spaxels_voxel_string,
                                                       tsncont_pspfwhm_all_string,
                                                       sncont_centerspaxel_aa_string,
                                                       sncont_cr1spaxels_aa_string,
                                                       sncont_1aa_all_string,
                                                       tsncont_centerspaxel_aa_string,
                                                       tsncont_cr1spaxels_aa_string,
                                                       tsncont_1aa_all_string,
                                                       sncont_centerspaxel_all_string,
                                                       sncont_cr1spaxels_all_string,
                                                       sncont_band_all_string,
                                                       tsncont_centerspaxel_all_string,
                                                       tsncont_cr1spaxels_all_string,
                                                       tsncont_band_all_string)

                elif om_val_string == 'LCB' and sourcet_val_string == 'Point':
                    from output_table_LCB_P_T import tablenewpsfLPT
                    tablenewpsfstring = tablenewpsfLPT(lambdaeff_string,
                                                       seeingx_string,
                                                       exptimepframe_val_string,
                                                       exptime_val_string,
                                                       numframe_val_string,
                                                       seeing_centermean_string,
                                                       seeing_cr1_string,
                                                       seeing_cr1r2_string,
                                                       sncont_centerspaxel_voxel_string,
                                                       sncont_cr1spaxels_voxel_string,
                                                       sncont_cr1r2spaxels_voxel_string,
                                                       tsncont_centerspaxel_voxel_string,
                                                       tsncont_cr1spaxels_voxel_string,
                                                       tsncont_cr1r2spaxels_voxel_string,
                                                       sncont_centerspaxel_aa_string,
                                                       sncont_cr1spaxels_aa_string,
                                                       sncont_cr1r2spaxels_aa_string,
                                                       tsncont_centerspaxel_aa_string,
                                                       tsncont_cr1spaxels_aa_string,
                                                       tsncont_cr1r2spaxels_aa_string,
                                                       sncont_centerspaxel_all_string,
                                                       sncont_cr1spaxels_all_string,
                                                       sncont_cr1r2spaxels_all_string,
                                                       tsncont_centerspaxel_all_string,
                                                       tsncont_cr1spaxels_all_string,
                                                       tsncont_cr1r2spaxels_all_string)

                elif om_val_string == 'LCB' and sourcet_val_string == 'Extended':
                    from output_table_LCB_E_T import tablenewpsfLET
                    tablenewpsfstring = tablenewpsfLET(lambdaeff_string,
                                                       seeingx_string,
                                                       exptimepframe_val_string,
                                                       exptime_val_string,
                                                       numframe_val_string,
                                                       sncont_centerspaxel_voxel_string,
                                                       sncont_cr1spaxels_voxel_string,
                                                       sncont_cr1r2spaxels_voxel_string,
                                                       tsncont_centerspaxel_voxel_string,
                                                       tsncont_cr1spaxels_voxel_string,
                                                       tsncont_cr1r2spaxels_voxel_string,
                                                       sncont_centerspaxel_aa_string,
                                                       sncont_cr1spaxels_aa_string,
                                                       sncont_cr1r2spaxels_aa_string,
                                                       tsncont_centerspaxel_aa_string,
                                                       tsncont_cr1spaxels_aa_string,
                                                       tsncont_cr1r2spaxels_aa_string,
                                                       sncont_centerspaxel_all_string,
                                                       sncont_cr1spaxels_all_string,
                                                       sncont_cr1r2spaxels_all_string,
                                                       tsncont_centerspaxel_all_string,
                                                       tsncont_cr1spaxels_all_string,
                                                       tsncont_cr1r2spaxels_all_string)

                else:
                    tablenewpsfstring = ''
            elif cmode == 'S':
                if om_val_string == 'MOS' and sourcet_val_string == 'Point':
                    from output_table_MOS_P_S import tablenewpsfMPS
                    tablenewpsfstring = tablenewpsfMPS(snr_string,
                                                       numframe_val_string,
                                                       snrpframe_string,
                                                       exptimepframe_val_string,
                                                       exptime_val_string,
                                                       etpframe_c_voxel_string,
                                                       etallframe_c_voxel_string,
                                                       etpframe_cr1_voxel_string,
                                                       etallframe_cr1_voxel_string,
                                                       etpframe_cr1r2_voxel_string,
                                                       etallframe_cr1r2_voxel_string,
                                                       etpframe_c_aa_string,
                                                       etallframe_c_aa_string,
                                                       etpframe_cr1_aa_string,
                                                       etallframe_cr1_aa_string,
                                                       etpframe_cr1r2_aa_string,
                                                       etallframe_cr1r2_aa_string,
                                                       etpframe_c_all_string,
                                                       etallframe_c_all_string,
                                                       etpframe_cr1_all_string,
                                                       etallframe_cr1_all_string,
                                                       etpframe_cr1r2_all_string,
                                                       etallframe_cr1r2_all_string,
                                                       lambdaeff_string,
                                                       seeingx_string,
                                                       sncont_centerspaxel_voxel_string,
                                                       sncont_cr1spaxels_voxel_string,
                                                       sncont_cr1r2spaxels_voxel_string,
                                                       tsncont_centerspaxel_voxel_string,
                                                       tsncont_cr1spaxels_voxel_string,
                                                       tsncont_cr1r2spaxels_voxel_string,
                                                       sncont_centerspaxel_aa_string,
                                                       sncont_cr1spaxels_aa_string,
                                                       sncont_cr1r2spaxels_aa_string,
                                                       tsncont_centerspaxel_aa_string,
                                                       tsncont_cr1spaxels_aa_string,
                                                       tsncont_cr1r2spaxels_aa_string,
                                                       sncont_centerspaxel_all_string,
                                                       sncont_cr1spaxels_all_string,
                                                       )
                elif om_val_string == 'MOS' and sourcet_val_string == 'Extended':
                    from output_table_MOS_E_S import tablenewpsfMES
                    tablenewpsfstring = tablenewpsfMES(snr_string,
                                                       numframe_val_string,
                                                       snrpframe_string,
                                                       exptimepframe_val_string,
                                                       exptime_val_string,
                                                       etpframe_c_voxel_string,
                                                       etallframe_c_voxel_string,
                                                       etpframe_cr1_voxel_string,
                                                       etallframe_cr1_voxel_string,
                                                       etpframe_cr1r2_voxel_string,
                                                       etallframe_cr1r2_voxel_string,
                                                       etpframe_c_aa_string,
                                                       etallframe_c_aa_string,
                                                       etpframe_cr1_aa_string,
                                                       etallframe_cr1_aa_string,
                                                       etpframe_cr1r2_aa_string,
                                                       etallframe_cr1r2_aa_string,
                                                       etpframe_c_all_string,
                                                       etallframe_c_all_string,
                                                       etpframe_cr1_all_string,
                                                       etallframe_cr1_all_string,
                                                       etpframe_cr1r2_all_string,
                                                       etallframe_cr1r2_all_string,
                                                       lambdaeff_string, seeingx_string,
                                                       nfibres_string,
                                                       sncont_centerspaxel_voxel_string,
                                                       sncont_cr1spaxels_voxel_string,
                                                       sncont_pspfwhm_all_string,
                                                       tsncont_centerspaxel_voxel_string,
                                                       tsncont_cr1spaxels_voxel_string,
                                                       tsncont_pspfwhm_all_string,
                                                       sncont_centerspaxel_aa_string,
                                                       sncont_cr1spaxels_aa_string,
                                                       sncont_1aa_all_string,
                                                       tsncont_centerspaxel_aa_string,
                                                       tsncont_cr1spaxels_aa_string,
                                                       tsncont_1aa_all_string,
                                                       sncont_centerspaxel_all_string,
                                                       sncont_cr1spaxels_all_string,
                                                       sncont_band_all_string,
                                                       tsncont_centerspaxel_all_string,
                                                       tsncont_cr1spaxels_all_string,
                                                       tsncont_band_all_string,
                                                       )

                elif om_val_string == 'LCB' and sourcet_val_string == 'Extended':
                    from output_table_LCB_E_S import tablenewpsfLES
                    tablenewpsfstring = tablenewpsfLES(snr_string,
                                                       numframe_val_string,
                                                       snrpframe_string,
                                                       exptimepframe_val_string,
                                                       exptime_val_string,
                                                       etpframe_c_voxel_string,
                                                       etallframe_c_voxel_string,
                                                       etpframe_cr1_voxel_string,
                                                       etallframe_cr1_voxel_string,
                                                       etpframe_cr1r2_voxel_string,
                                                       etallframe_cr1r2_voxel_string,
                                                       etpframe_c_aa_string,
                                                       etallframe_c_aa_string,
                                                       etpframe_cr1_aa_string,
                                                       etallframe_cr1_aa_string,
                                                       etpframe_cr1r2_aa_string,
                                                       etallframe_cr1r2_aa_string,
                                                       etpframe_c_all_string,
                                                       etallframe_c_all_string,
                                                       etpframe_cr1_all_string,
                                                       etallframe_cr1_all_string,
                                                       etpframe_cr1r2_all_string,
                                                       etallframe_cr1r2_all_string,
                                                       lambdaeff_string,
                                                       seeingx_string,
                                                       sncont_centerspaxel_voxel_string,
                                                       sncont_cr1spaxels_voxel_string,
                                                       sncont_cr1r2spaxels_voxel_string,
                                                       tsncont_centerspaxel_voxel_string,
                                                       tsncont_cr1spaxels_voxel_string,
                                                       tsncont_cr1r2spaxels_voxel_string,
                                                       sncont_centerspaxel_aa_string,
                                                       sncont_cr1spaxels_aa_string,
                                                       sncont_cr1r2spaxels_aa_string,
                                                       tsncont_centerspaxel_aa_string,
                                                       tsncont_cr1spaxels_aa_string,
                                                       tsncont_cr1r2spaxels_aa_string,
                                                       sncont_centerspaxel_all_string,
                                                       sncont_cr1spaxels_all_string,
                                                       sncont_cr1r2spaxels_all_string,
                                                       tsncont_centerspaxel_all_string,
                                                       tsncont_cr1spaxels_all_string,
                                                       tsncont_cr1r2spaxels_all_string)
                elif om_val_string == 'LCB' and sourcet_val_string == 'Point':
                    from output_table_LCB_P_S import tablenewpsfLPS
                    tablenewpsfstring = tablenewpsfLPS(snr_string,
                                                       numframe_val_string,
                                                       snrpframe_string,
                                                       exptimepframe_val_string,
                                                       exptime_val_string,
                                                       etpframe_c_voxel_string,
                                                       etallframe_c_voxel_string,
                                                       etpframe_cr1_voxel_string,
                                                       etallframe_cr1_voxel_string,
                                                       etpframe_cr1r2_voxel_string,
                                                       etallframe_cr1r2_voxel_string,
                                                       etpframe_c_aa_string,
                                                       etallframe_c_aa_string,
                                                       etpframe_cr1_aa_string,
                                                       etallframe_cr1_aa_string,
                                                       etpframe_cr1r2_aa_string,
                                                       etallframe_cr1r2_aa_string,
                                                       etpframe_c_all_string,
                                                       etallframe_c_all_string,
                                                       etpframe_cr1_all_string,
                                                       etallframe_cr1_all_string,
                                                       etpframe_cr1r2_all_string,
                                                       etallframe_cr1r2_all_string,
                                                       lambdaeff_string,
                                                       seeingx_string,
                                                       sncont_centerspaxel_voxel_string,
                                                       sncont_cr1spaxels_voxel_string,
                                                       sncont_cr1r2spaxels_voxel_string,
                                                       tsncont_centerspaxel_voxel_string,
                                                       tsncont_cr1spaxels_voxel_string,
                                                       tsncont_cr1r2spaxels_voxel_string,
                                                       sncont_centerspaxel_aa_string,
                                                       sncont_cr1spaxels_aa_string,
                                                       sncont_cr1r2spaxels_aa_string,
                                                       tsncont_centerspaxel_aa_string,
                                                       tsncont_cr1spaxels_aa_string,
                                                       tsncont_cr1r2spaxels_aa_string,
                                                       sncont_centerspaxel_all_string,
                                                       sncont_cr1spaxels_all_string,
                                                       sncont_cr1r2spaxels_all_string,
                                                       tsncont_centerspaxel_all_string,
                                                       tsncont_cr1spaxels_all_string,
                                                       tsncont_cr1r2spaxels_all_string)
                else:
                    tablenewpsfstring = ''

            # NOT WORKING YET SO SETTING TO EMPTY
            tablenewpsflinestring = ''

            # FOR DOWNLOADABLE FILES
            forfileoutputstring = outputofcalc['forfileoutput']
            forfileoutput2string = outputofcalc['forfileoutput2']
            forfileoutput3string = outputofcalc['forfileoutput3']

            # EXTRA FOOTER
            footerstring = '<span class="italicsmall">Time of request: ' + start_time_string + ' ; End of request: ' + time.strftime(
                "%H:%M:%S") + '</span>'

        else:
            outhead1string = ''
            tablecoutstring = ''
            tableloutstring = ''
            tableinputstring = ''
            tablecalcstring = ''
            tablenewpsfstring = ''
            tablenewpsflinestring = ''
            forfileoutputstring = ''
            forfileoutput2string = ''
            forfileoutput3string = ''
            footerstring = ''

        print "### LOG: ABOUT TO QUIT ETC_DO; JSON OUTPUT TO JAVASCRIPT."
        from django.http import JsonResponse
        return JsonResponse({'outtext': outtextstring,
                             'textinput': inputstring,
                             'textcout': coutputstring,
                             'textlout': loutputstring,
                             'textcalc': textcalcstring,
                             'tablecout': tablecoutstring,
                             'tablelout': tableloutstring,
                             'tableinput': tableinputstring,
                             'tablecalc': tablecalcstring,
                             'tablenewpsf': tablenewpsfstring,
                             'tablenewpsfline': tablenewpsflinestring,
                             'thescript': thescript,
                             'thediv': thediv,
                             'outhead1': outhead1string,
                             'forfile': forfileoutputstring,
                             'forfile2': forfileoutput2string,
                             'forfile3': forfileoutput3string,
                             'footerstring': footerstring,
                             })
