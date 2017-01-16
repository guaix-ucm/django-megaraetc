from django.http import HttpResponse
from django.shortcuts import render
from .forms import AtmosphericConditionsForm, ObservationalSetupForm
from .forms import TargetForm, InstrumentForm
from .forms import OutputSetupForm
from .models import PhotometricFilter, SeeingTemplate
from .models import SpectralTemplate, VPHSetup

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
            size_val = numpy.pi * (radius_val**2)
    mag_val = float(request.POST['contmagval']) if request.POST[
                                                       'contmagflux'] == 'M' else 20.0
    fc_val = 1e-16 if request.POST['contmagflux'] == 'M' else float(
        request.POST['contfluxval'])

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
        exptimepframe_val = float(request.POST['exptimepframe'])
        nsbundles_val = int(request.POST['nsbundles'])

        plotflag_val = request.POST['plotflag']

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
                            numframes_val, exptimepframe_val, nsbundles_val,
                            plotflag_val
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
        form2 = InstrumentForm(request.GET)
        form3 = AtmosphericConditionsForm(request.GET)
        form4 = ObservationalSetupForm(request.GET)
        form5 = OutputSetupForm(request.GET)

    # if a GET (or any other method) we'll create a blank form
    else:
        form1 = TargetForm()
        form2 = InstrumentForm()
        form3 = AtmosphericConditionsForm()
        form4 = ObservationalSetupForm()
        form5 = OutputSetupForm()

    return render(request, 'etc/webmegaraetc-0.8.0.html', {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'form5': form5,
    })


# LOADS THIS AFTER PUSHING "START" in index.html
def etc_form(request):
    form1 = TargetForm()
    form2 = InstrumentForm()
    form3 = AtmosphericConditionsForm()
    form4 = ObservationalSetupForm()
    form5 = OutputSetupForm()

    total_formu = {'form1': form1,
                   'form2': form2,
                   'form3': form3,
                   'form4': form4,
                   'form5': form5,
                   }

    return render(request, 'etc/webmegaraetc-0.8.0.html', total_formu)


# LOADS THIS AFTER PRESSING "SUBMIT" webmegaraetc.html and
# OUTPUT RESULTS in JSON HTTP Response directly into html page
# FINAL STRING CLEANSING/FILTERING HERE
#
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
        outputofcalc = compute5(request)
        print '### LOG: ETC_DO: OUTPUTOFCALC SUCCESSFULLY COMPUTED'
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
        textcalcstring = '<br /><table border=1 id="mathtextid"><tr><td>' + str(outputofcalc['textcalc']) + '</td></tr></table>'

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
                y = outputofcalc['fc']
                label1 = entry_spec_name
                label2 = outputofcalc['mag_val']
                label3 = outputofcalc['bandc_val']

                x2 = x
                y2 = outputofcalc['pframesn_pervoxel_fiber']
                x2b = x2
                y2b = outputofcalc['allframesn_pervoxel_fiber']
                x2c = x2
                y2c = outputofcalc['pframesn_pervoxel_all']
                x2d = x2
                y2d = outputofcalc['allframesn_pervoxel_all']

                label2a = entry_spec_name
                label2b = vph_val
                label2c = outputofcalc['bandc_val']
            else:
                x = numpy.arange(1, 1001, 1)
                y = numpy.arange(1, 1001, 1)
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
                label2a = "none"
                label2b = "none"
                label2c = "none"

            # More things to check
            if not tocheck:
                x3 = outputofcalc['wline_val']
                y3 = outputofcalc['fwhmline_val']
                z3 = outputofcalc['fline_val']
            else:
                x3 = numpy.arange(1, 1001, 1)
                y3 = numpy.arange(1, 1001, 1)
                z3 = numpy.arange(1, 1001, 1)

            # LEGACY CODE (MPLD3)
            # figura = plot_and_save_new('', x, y, x3, y3, z3,
            #                            vph_minval, vph_maxval,
            #                            label1, label2, label3)
            # html = mpld3.fig_to_html(figura)
            # html += mpld3.fig_to_html(figura2)
            # html = html.replace("None", "")  # No se xq introduce string None

            thescript, thediv = bokehplot1(x, y, x3, y3, z3,
                                           vph_minval, vph_maxval,
                                           label1, label2, label3,
                                           x2, y2, x2b, y2b,
                                           x2c, y2c, x2d, y2d,
                                           label2a, label2b, label2c)
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
            fsky_string = '%.3e' % outputofcalc['fsky']
            numframe_val_string = str(outputofcalc['numframe_val'])
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
            tsncont_p2sp_all_val = float(outputofcalc['tsncont_p2sp_all']/2)
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

            tsncont_centermean = "{0:.2f}".format((seeing_centermean_val/100) * tsncont_p2sp_all_val)
            tsncont_ring1mean = "{0:.2f}".format((seeing_ring1mean_val/100) * tsncont_p2sp_all_val)
            tsncont_ring2mean = "{0:.2f}".format((seeing_ring2mean_val/100) * tsncont_p2sp_all_val)
            tsncont_total = "{0:.2f}".format((seeing_total_val/100) * tsncont_p2sp_all_val)

            sncont_centerspaxel_voxel_val = outputofcalc['sncont_centerspaxel_voxel']
            sncont_centerspaxel_voxel_string = "{0:.2f}".format(float(sncont_centerspaxel_voxel_val))
            sncont_r1spaxel_voxel_val = outputofcalc['sncont_r1spaxel_voxel']
            sncont_r1spaxel_voxel_string = "{0:.2f}".format(float(sncont_r1spaxel_voxel_val))
            sncont_r2spaxel_voxel_val = outputofcalc['sncont_r2spaxel_voxel']
            sncont_r2spaxel_voxel_string = "{0:.2f}".format(float(sncont_r2spaxel_voxel_val))

            sncont_cr1spaxels_voxel_val = outputofcalc['sncont_cr1spaxels_voxel']
            sncont_cr1spaxels_voxel_string = "{0:.2f}".format(float(sncont_cr1spaxels_voxel_val))
            sncont_cr1r2spaxels_voxel_val = outputofcalc['sncont_cr1r2spaxels_voxel']
            sncont_cr1r2spaxels_voxel_string = "{0:.2f}".format(float(sncont_cr1r2spaxels_voxel_val))
            #
            tsncont_centerspaxel_voxel_val = outputofcalc['tsncont_centerspaxel_voxel']
            tsncont_centerspaxel_voxel_string = "{0:.2f}".format(float(tsncont_centerspaxel_voxel_val))
            tsncont_cr1spaxels_voxel_val = outputofcalc['tsncont_cr1spaxels_voxel']
            tsncont_cr1spaxels_voxel_string = "{0:.2f}".format(float(tsncont_cr1spaxels_voxel_val))
            tsncont_cr1r2spaxels_voxel_val = outputofcalc['tsncont_cr1r2spaxels_voxel']
            tsncont_cr1r2spaxels_voxel_string = "{0:.2f}".format(float(tsncont_cr1r2spaxels_voxel_val))
            
            sncont_centerspaxel_aa_val = outputofcalc['sncont_centerspaxel_aa']
            sncont_centerspaxel_aa_string = "{0:.2f}".format(float(sncont_centerspaxel_aa_val))
            sncont_cr1spaxels_aa_val = outputofcalc['sncont_cr1spaxels_aa']
            sncont_cr1spaxels_aa_string = "{0:.2f}".format(float(sncont_cr1spaxels_aa_val))
            sncont_cr1r2spaxels_aa_val = outputofcalc['sncont_cr1r2spaxels_aa']
            sncont_cr1r2spaxels_aa_string = "{0:.2f}".format(float(sncont_cr1r2spaxels_aa_val))
            #
            tsncont_centerspaxel_aa_val = outputofcalc['tsncont_centerspaxel_aa']
            tsncont_centerspaxel_aa_string = "{0:.2f}".format(float(tsncont_centerspaxel_aa_val))
            tsncont_cr1spaxels_aa_val = outputofcalc['tsncont_cr1spaxels_aa']
            tsncont_cr1spaxels_aa_string = "{0:.2f}".format(float(tsncont_cr1spaxels_aa_val))
            tsncont_cr1r2spaxels_aa_val = outputofcalc['tsncont_cr1r2spaxels_aa']
            tsncont_cr1r2spaxels_aa_string = "{0:.2f}".format(float(tsncont_cr1r2spaxels_aa_val))
            
            sncont_centerspaxel_all_val = outputofcalc['sncont_centerspaxel_all']
            sncont_centerspaxel_all_string = "{0:.2f}".format(float(sncont_centerspaxel_all_val))
            sncont_cr1spaxels_all_val = outputofcalc['sncont_cr1spaxels_all']
            sncont_cr1spaxels_all_string = "{0:.2f}".format(float(sncont_cr1spaxels_all_val))
            sncont_cr1r2spaxels_all_val = outputofcalc['sncont_cr1r2spaxels_all']
            sncont_cr1r2spaxels_all_string = "{0:.2f}".format(float(sncont_cr1r2spaxels_all_val))
            #
            tsncont_centerspaxel_all_val = outputofcalc['tsncont_centerspaxel_all']
            tsncont_centerspaxel_all_string = "{0:.2f}".format(float(tsncont_centerspaxel_all_val))
            tsncont_cr1spaxels_all_val = outputofcalc['tsncont_cr1spaxels_all']
            tsncont_cr1spaxels_all_string = "{0:.2f}".format(float(tsncont_cr1spaxels_all_val))
            tsncont_cr1r2spaxels_all_val = outputofcalc['tsncont_cr1r2spaxels_all']
            tsncont_cr1r2spaxels_all_string = "{0:.2f}".format(float(tsncont_cr1r2spaxels_all_val))

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
            sncont_pdp_fibre_string = "{0:.2f}".format(float(sncont_pdp_fibre_val))
            tsncont_pdp_fibre_val = outputofcalc['tsncont_pdp_fibre']
            tsncont_pdp_fibre_string = "{0:.2f}".format(float(tsncont_pdp_fibre_val))
            npixx_pdp_fibre_val = outputofcalc['npixx_pdp_fibre']
            npixx_pdp_fibre_string = "{0:.2f}".format(float(npixx_pdp_fibre_val))
            npixy_pdp_fibre_val = outputofcalc['npixy_pdp_fibre']
            npixy_pdp_fibre_string = "{0:.2f}".format(float(npixy_pdp_fibre_val))

            sncont_psp_fibre_val = outputofcalc['sncont_psp_fibre']
            sncont_psp_fibre_string = "{0:.2f}".format(float(sncont_psp_fibre_val))
            tsncont_psp_fibre_val = outputofcalc['tsncont_psp_fibre']
            tsncont_psp_fibre_string = "{0:.2f}".format(float(tsncont_psp_fibre_val))
            npixx_psp_fibre_val = outputofcalc['npixx_psp_fibre']
            npixx_psp_fibre_string = "{0:.2f}".format(float(npixx_psp_fibre_val))
            npixy_psp_fibre_val = outputofcalc['npixy_psp_fibre']
            npixy_psp_fibre_string = "{0:.2f}".format(float(npixy_psp_fibre_val))

            sncont_psp_all_val = outputofcalc['sncont_psp_all']
            sncont_psp_all_string = "{0:.2f}".format(float(sncont_psp_all_val))
            tsncont_psp_all_val = outputofcalc['tsncont_psp_all']
            tsncont_psp_all_string = "{0:.2f}".format(float(tsncont_psp_all_val))
            npixx_psp_all_val = outputofcalc['npixx_psp_all']
            npixx_psp_all_string = "{0:.2f}".format(float(npixx_psp_all_val))
            npixy_psp_all_val = outputofcalc['npixy_psp_all']
            npixy_psp_all_string = "{0:.2f}".format(float(npixy_psp_all_val))

            outhead1string = '<hr /><span class="boldlarge">Observing Mode: ' + om_val_string + ', VPH: ' + vph_val_string + ', Source Type: ' + sourcet_val_string + ' </span>' + \
                                '<span class="italicsmall"> Computation time: ' + "{0:.4f}".format((time.time() - start_time)) + ' seconds; </span>'

            # tablecoutstring = '<hr /><br />' + \
            #                   'OUTPUT CONTINUUM SNR:' + \
            #                   '<br />(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
            #                   '<table border=1>' + \
            #                   '<tr>' \
            #                     '<th class="iconcolumn" scope="col"> </th>' \
            #                     '<th scope="col" colspan="4">* SNR per fibre:</th>' \
            #                     '<th scope="col"></th></tr>' + \
            #                   '<tr>' \
            #                     '<th class="iconcolumn" scope="row"> </th>' \
            #                     '<td>npixx</td>' \
            #                     '<td>npixy</td>' \
            #                     '<td class="perframecolumn">per frame</td>' \
            #                     '<td class="allframecolumn">all frames</td>' \
            #                     '<td></td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pdp.jpeg" /></td>' \
            #                     '<td>' + npixx_pdp_fibre_string + '</td>' \
            #                     '<td>' + npixy_pdp_fibre_string + '</td>' \
            #                     '<td class="perframecolumn"> ' + sncont_pdp_fibre_string + ' </td>' \
            #                     '<td> ' + tsncont_pdp_fibre_string + '</td>' \
            #                     '<td> per detector pixel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspp.jpeg" /></td>' \
            #                     '<td>' + npixx_psp_fibre_string + '</td>' \
            #                     '<td>' + npixy_psp_fibre_string + '</td>' \
            #                     '<td class="perframecolumn"> ' + sncont_psp_fibre_string + ' </td>' \
            #                     '<td> ' + tsncont_psp_fibre_string + '</td>' \
            #                     '<td> per spectral pixel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
            #                     '<td>' + npixx_p2sp_fibre_string + '</td>' \
            #                     '<td>' + npixy_p2sp_fibre_string + '</td>' \
            #                     '<td class="perframecolumn"> ' + sncont_p2sp_fibre_string + ' </td>' \
            #                     '<td> ' + tsncont_p2sp_fibre_string + '</td>' \
            #                     '<td> per voxel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' \
            #                     '<td>' + npixx_1aa_fibre_string + '</td>' \
            #                     '<td>' + npixy_1aa_fibre_string + '</td>' \
            #                     '<td class="perframecolumn"> ' + sncont_1aa_fibre_string + ' </td>' \
            #                     '<td> ' + tsncont_1aa_fibre_string + '</td>' \
            #                     '<td> per AA</td></tr>' + \
            #                   '<tr class="rowheight">' \
            #                     '<td> </td></tr>' + \
            tablecoutstring = ''
            # tablecoutstring = '<hr />' + \
            #                   'OUTPUT CONTINUUM SNR:' + \
            #                   '<br />(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
            #                   '<table border=1>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"> </td>' \
            #                     '<th scope="col" colspan="4">* SNR in total source area:</th>' \
            #                     '<th>(number of fibers = ' + nfibres_string + ')</th></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"> </td>' \
            #                     '<td>npixx</td><td>npixy</td>' \
            #                     '<td class="perframecolumn">per frame</td>' \
            #                     '<td class="allframecolumn">all frames</td>' \
            #                     '<td></td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspp.jpeg" /></td>' \
            #                     '<td>' + npixx_psp_all_string + '</td>' \
            #                     '<td>' + npixy_psp_all_string + '</td>' \
            #                     '<td> ' + sncont_psp_all_string + ' </td>' \
            #                     '<td> ' + tsncont_psp_all_string + '</td>' \
            #                     '<td> per spectral pixel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
            #                     '<td>' + npixx_p2sp_all_string + '</td>' \
            #                     '<td>' + npixy_p2sp_all_string + '</td>' \
            #                     '<td> ' + sncont_pspfwhm_all_string + ' </td>' \
            #                     '<td> ' + tsncont_pspfwhm_all_string + '</td>' \
            #                     '<td> per voxel</td></tr>' + \
            #                   '<tr>' \
            #                     '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' \
            #                     '<td>' + npixx_1aa_all_string + '</td>' \
            #                     '<td>' + npixy_1aa_all_string + '</td>' \
            #                     '<td> ' + sncont_1aa_all_string + ' </td>' \
            #                     '<td> ' + tsncont_1aa_all_string + '</td>' \
            #                     '<td> per AA</td></tr>' + \
            #                   '</table><br />'

            # if sourcet_val_string == 'E':
            #                       # '<hr />' + \
            #                       # 'OUTPUT CONTINUUM <br />' + \
            #                       # '(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
            #     tablecoutstring = tablecoutstring + \
            #                       '<hr />' + \
            #                       '<table border=1>' + \
            #                       '<tr>' \
            #                         '<th class="iconcolumn" scope="col"> </td>' \
            #                         '<th scope="col" colspan="4">* SNR in one seeing:</th><th scope="col"></th></tr>' + \
            #                       '<tr>' \
            #                         '<th class="iconcolumn" scope="row"> </th>' \
            #                         '<td>npixx</td>' \
            #                         '<td>npixy</td>' \
            #                         '<td class="perframecolumn">per frame</td>' \
            #                         '<td class="allframecolumn">all frames</td>' \
            #                         '<td></td></tr>' + \
            #                       '<tr>' \
            #                         '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
            #                         '<td>' + npixx_p2sp_seeing_string + '</td>' \
            #                         '<td>' + npixy_p2sp_seeing_string + '</td>' \
            #                         '<td> ' + sncont_p2sp_seeing_string + ' </td>' \
            #                         '<td> ' + tsncont_p2sp_seeing_string + '</td>' \
            #                         '<td> per voxel</td></tr>' + \
            #                       '<tr>' \
            #                         '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' \
            #                         '<td>' + npixx_1aa_seeing_string + '</td>' \
            #                         '<td>' + npixy_1aa_seeing_string + '</td>' \
            #                         '<td> ' + sncont_1aa_seeing_string + ' </td>' \
            #                         '<td> ' + tsncont_1aa_seeing_string + '</td>' \
            #                         '<td> per AA</td></tr>' + \
            #                       '<tr>' \
            #                         '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' \
            #                         '<td>' + npixx_band_seeing_string + '</td>' \
            #                         '<td>' + npixy_band_seeing_string + '</td>' \
            #                         '<td> ' + sncont_band_seeing_string + ' </td>' \
            #                         '<td> ' + tsncont_band_seeing_string + '</td>' \
            #                         '<td> per integrated spectrum (spaxel)</td></tr>' + \
            #                       '</table>'
                                  # '<tr class="rowheight">' \
                                  #   '<td> </td></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"> </td>' \
                                  #   '<th scope="col" colspan="4">* SNR in one arcsec^2:</th>' \
                                  #   '<th></th></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"> </td>' \
                                  #   '<td>npixx</td>' \
                                  #   '<td>npixy</td>' \
                                  #   '<td class="perframecolumn">per frame</td>' \
                                  #   '<td class="allframecolumn">all frames</td>' \
                                  #   '<td></td></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
                                  #   '<td>' + npixx_p2sp_1_string + '</td>' \
                                  #   '<td>' + npixy_p2sp_1_string + '</td>' \
                                  #   '<td> ' + sncont_p2sp_1_string + ' </td>' \
                                  #   '<td> ' + tsncont_p2sp_1_string + '</td>' \
                                  #   '<td> per voxel</td></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' \
                                  #   '<td>' + npixx_1aa_1_string + '</td>' \
                                  #   '<td>' + npixy_1aa_1_string + '</td>' \
                                  #   '<td> ' + sncont_1aa_1_string + ' </td>' \
                                  #   '<td> ' + tsncont_1aa_1_string + '</td>' \
                                  #   '<td> per AA</td></tr>' + \
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' \
                                  #   '<td>' + npixx_band_1_string + '</td>' \
                                  #   '<td>' + npixy_band_1_string + '</td>' \
                                  #   '<td> ' + sncont_band_1_string + ' </td>' \
                                  #   '<td> ' + tsncont_band_1_string + '</td>' \
                                  #   '<td> per integrated spectrum (spaxel)</td></tr>' + \
                                  # '</table>'

            if fluxt_val_string == 'L':
                tableloutstring = '<hr />' + \
                                  'OUTPUT LINE SNR: ' + fluxt_val_string + \
                                  '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
                                  '<table border=1>' + \
                                  '<tr>' \
                                    '<th class="iconcolumn" scope="row"> </th>' \
                                    '<td class="perframecolumn">per frame</td>' \
                                    '<td class="allframecolumn">all frames</td>' \
                                    '<td></td></tr>' + \
                                  '<tr>' \
                                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pdp.jpeg" /></td>' \
                                    '<td class="perframecolumn"> ' + snline_pspp_string + '</td>' \
                                    '<td> ' + tsnline_pspp_string + '</td>' \
                                    '<td> per fiber per detector pixel</td></tr>' + \
                                  '<tr>' \
                                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' \
                                    '<td class="perframecolumn"> ' + snline_voxel_string + '</td>' \
                                    '<td> ' + tsnline_voxel_string + '</td>' \
                                    '<td> per fiber per voxel</td></tr>' + \
                                  '<tr>' \
                                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_perfibinappang.jpeg" /></td>' \
                                    '<td class="perframecolumn"> ' + snline_fibre1aa_string + '</td>' \
                                    '<td> ' + tsnline_fibre1aa_string + '</td>' \
                                    '<td> per fiber in aperture per AA</td></tr>' + \
                                  '<tr>' \
                                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_perfibinap.jpeg" /></td>' \
                                    '<td class="perframecolumn"> ' + snline_fibre_string + '</td>' \
                                    '<td> ' + tsnline_fibre_string + '</td>' \
                                    '<td> per fiber in aperture</td></tr>' + \
                                  '<tr>' \
                                    '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_totalinap.jpeg" /></td>' \
                                    '<td class="perframecolumn"> ' + snline_all_string + '</td>' \
                                    '<td>' + tsnline_all_string + '</td>' \
                                    '<td> total in aperture</td></tr>' + \
                                  '</table><br />'
                                  # '<tr>' \
                                  #   '<td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pasqpang.jpeg" /></td>' \
                                  #   '<td class="perframecolumn"> ' + snline_1_aa_string + '</td>' \
                                  #   '<td> ' + tsnline_1_aa_string + '</td>' \
                                  #   '<td> per arcsec per AA</td></tr>' + \

            else:
                tableloutstring = 'No line input<br /><br />'

            if om_val_string == 'MOS':
                switchstring = 'Sky-bundles:'
            elif om_val_string == 'LCB':
                switchstring = 'Sky-fibers:'

            tableinputstring = '<table border=1>' + \
                               '<tr><td>INPUT PARAMETERS:</td><td></td></tr>' + \
                               '<tr><td>Source type:</td><td>' + sourcet_val_string + '</td></tr>' + \
                               '<tr><td>Area:</td><td>' + size_val_string + ' arcsec^2</td></tr>' + \
                               '<tr><td>Observing mode:</td><td>' + om_val_string + '</td></tr>' + \
                               '<tr><td>VPH:</td><td>' + vph_val_string + '</td></tr>' + \
                               '<tr><td>Input flux type:</td><td>' + fluxt_name_string + '</td></tr>' + \
                               '<tr><td>Source spectrum:</td><td>' + spect_val_string + '</td></tr>' + \
                               '<tr><td>Continuum:</td><td>' + bandc_val_string + ' = ' + mag_val_string + 'mag</td></tr>' + \
                               '<tr><td>Continuum flux:</td><td>' + netflux_string + ' erg/s/cm2</td></tr>' + \
                               '<tr><td>Resolved line?:</td><td>' + resolvedline_val_string + '</td></tr>' + \
                               '<tr><td>Line wavelength:</td><td>' + wline_val_string + ' AA</td></tr>' + \
                               '<tr><td>Line flux:</td><td>' + fline_val_string + ' erg/s/cm2</td></tr>' + \
                               '<tr><td>Line FWHM:</td><td>' + fwhmline_val_string + ' AA</td></tr>' + \
                               '<tr><td>*Sky Condition:</td><td>' + skycond_val_string + '</td></tr>' + \
                               '<tr><td>Moon:</td><td>' + moon_val_string + '</td></tr>' + \
                               '<tr><td>Airmass: X=</td><td>' + airmass_val_string + '</td></tr>' + \
                               '<tr><td>Seeing(@X=1):</td><td>' + seeing_zenith_string + ' arcsec</td></tr>' + \
                               '<tr><td>Sky-flux(R,@X):</td><td>' + fsky_string + ' erg/s/cm2</td></tr>' + \
                               '<tr><td>Seeing(@X):</td><td>' + seeingx_string + ' arcsec</td></tr>' + \
                               '<tr><td>*Observation:</td></td><td></tr>' + \
                               '<tr><td>Number of frames:</td><td>' + numframe_val_string + '</td></tr>' + \
                               '<tr><td>Exptime per frame:</td><td>' + exptimepframe_val_string + ' s</td></tr>' + \
                               '<tr><td>Total exptime:</td><td>' + exptime_val_string + ' s</td></tr>' + \
                               '<tr><td>NP_Dark:</td><td>' + npdark_val_string + '</td></tr>' + \
                               '<tr><td>'+switchstring+'</td><td>' + nsbundles_val_string + '</td></tr>' + \
                               '</table><br />'

            # NOT USED BUT KEEP FOR TESTING
            tablecalcstring = '<br /><br />' + \
                              '<p id="mathid">Details of calculations (TEST):<br />' + \
                              '$$\\textrm{Radius of source, } R_{source} = ' + radius_val_string + '\\textrm{ arcsec}$$' + \
                              '$$\\textrm{Area of source, } \Omega_{source} = \pi \\times ' + radius_val_string + '^{2} = ' + size_val_string + '\\textrm{ arcsec}^{2}$$' + \
                              '$$\\textrm{Radius of one fiber, } R_{fiber} = 0.31 \\textrm{ arcsec}$$'+ \
                              '$$\\textrm{Area of one fiber, } \Omega_{fiber} =  3\sqrt{3} \left( \\frac{R_{fiber}^{2}}{2} \\right)$$' + \
                              '$$\\textrm{Number of fibers used to measure sky} = \\frac{\Omega_{source}}{\Omega_{fiber}} = ' + nfibres_string + '$$' + \
                              '$$\\textrm{Area in which sky has been measured, } \Omega_{sky} = ' + nfibres_string + '\\times \Omega_{fiber}$$' + \
                              '</p>' + \
                              '<br /><br />'
            # print om_val_string
            # print 'PID = ', os.getpid()

            # NEW OUTPUT CONTINUUM TABLE FOR MOS AND LCB
            if om_val_string == 'MOS' and sourcet_val_string == 'Point':
                tablenewpsfstring = '<hr />' + \
                                    'OUTPUT CONTINUUM SNR' + \
                                    '<br />(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
                                    '<table border=1>' + \
                                    '<tr><th class="iconcolumn" scope="col"> </th>' + \
                                        '<th scope="col" colspan="7">* Continuum SNR per spaxel zones due to PSF (MOS mode):<br />' + \
                                        'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec</th>' + \
                                        '</tr>' + \
                                    '<tr><th class="iconcolumn" scope="row"></th>' + \
                                        '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
                                        '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
                                        '<td></td>' + \
                                        '</tr>' + \
                                    '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
                                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
                                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
                                        '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area <br />'+ nfibres_string + ' fibers</td>' + \
                                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string + '%)<br />1 fiber</td>' + \
                                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
                                        '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area<br />' + nfibres_string + ' fibers</td>' + \
                                        '<td></td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
                                        '<td> ' + sncont_pspfwhm_all_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
                                        '<td> ' + tsncont_pspfwhm_all_string + '</td>' + \
                                        '<td> per voxel</td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
                                        '<td> ' + sncont_1aa_all_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
                                        '<td> ' + tsncont_1aa_all_string + '</td>' + \
                                        '<td> per AA</td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
                                        '<td> ' + sncont_band_all_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
                                        '<td> ' + tsncont_band_all_string + '</td>' + \
                                        '<td> integrated spectrum </td>' + \
                                        '</tr>' + \
                                    '</table><br />'
                                    # 'TESTING AREA: SNCONT_C_VOXEL= ' + sncont_centerspaxel_voxel_string + '<br />' + \
                                    # 'TESTING AREA: SNCONT_R1_VOXEL= ' + sncont_r1spaxel_voxel_string + '<br />'
            elif om_val_string == 'MOS' and sourcet_val_string == 'Extended':
                tablenewpsfstring = '<hr />' + \
                                    'OUTPUT CONTINUUM SNR' + \
                                    '<br />(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
                                    '<table border=1>' + \
                                    '<tr><th class="iconcolumn" scope="col"> </th>' + \
                                        '<th scope="col" colspan="7">* Continuum SNR per spaxel zones due to PSF (MOS mode):<br />' + \
                                        'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec</th>' + \
                                        '</tr>' + \
                                    '<tr><th class="iconcolumn" scope="row"></th>' + \
                                        '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
                                        '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
                                        '<td></td>' + \
                                        '</tr>' + \
                                    '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
                                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
                                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
                                        '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area <br />'+ nfibres_string + ' fibers</td>' + \
                                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
                                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
                                        '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area<br />' + nfibres_string + ' fibers</td>' + \
                                        '<td></td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
                                        '<td> ' + sncont_pspfwhm_all_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
                                        '<td> ' + tsncont_pspfwhm_all_string + '</td>' + \
                                        '<td> per voxel</td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
                                        '<td> ' + sncont_1aa_all_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
                                        '<td> ' + tsncont_1aa_all_string + '</td>' + \
                                        '<td> per AA</td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
                                        '<td> ' + sncont_band_all_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
                                        '<td> ' + tsncont_band_all_string + '</td>' + \
                                        '<td> integrated spectrum </td>' + \
                                        '</tr>' + \
                                    '</table><br />'
            elif om_val_string == 'LCB' and sourcet_val_string == 'Point':
                tablenewpsfstring = '<hr />' + \
                                    'OUTPUT CONTINUUM SNR' + \
                                    '<br />(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
                                    '<table border=1>' + \
                                    '<tr><th class="iconcolumn" scope="col"> </th>' + \
                                        '<th scope="col" colspan="7">* Continuum SNR per spaxel zones due to PSF (LCB mode):<br />' + \
                                        'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec</th>' + \
                                        '</tr>' + \
                                    '<tr><th class="iconcolumn" scope="row"></th>' + \
                                        '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
                                        '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
                                        '<td></td>' + \
                                        '</tr>' + \
                                    '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
                                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
                                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
                                        '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
                                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
                                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
                                        '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
                                        '<td>percentage of enclosed total flux</td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
                                        '<td> ' + sncont_cr1r2spaxels_voxel_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
                                        '<td> ' + tsncont_cr1r2spaxels_voxel_string + '</td>' + \
                                        '<td> per voxel</td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
                                        '<td> ' + sncont_cr1r2spaxels_aa_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
                                        '<td> ' + tsncont_cr1r2spaxels_aa_string + '</td>' + \
                                        '<td> per AA</td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
                                        '<td> ' + sncont_cr1r2spaxels_all_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
                                        '<td> ' + tsncont_cr1r2spaxels_all_string + '</td>' + \
                                        '<td> integrated spectrum </td>' + \
                                        '</tr>' + \
                                        '</table><br />'
                                    # 'TESTING AREA: SNCONT_C_VOXEL= ' + sncont_centerspaxel_voxel_string + '<br />' + \
                                    # 'TESTING AREA: SNCONT_R1_VOXEL= ' + sncont_r1spaxel_voxel_string + '<br />' + \
                                    # 'TESTING AREA: SNCONT_R2_VOXEL= ' + sncont_r2spaxel_voxel_string + '<br />'
            elif om_val_string == 'LCB' and sourcet_val_string == 'Extended':
                tablenewpsfstring = '<hr />' + \
                                    'OUTPUT CONTINUUM SNR' + \
                                    '<br />(at lambda_c(VPH) = ' + lambdaeff_string + ' AA)' + \
                                    '<table border=1>' + \
                                    '<tr><th class="iconcolumn" scope="col"> </th>' + \
                                        '<th scope="col" colspan="7">* Continuum SNR per spaxel zones due to PSF (LCB mode):<br />' + \
                                        'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec</th>' + \
                                        '</tr>' + \
                                    '<tr><th class="iconcolumn" scope="row"></th>' + \
                                        '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
                                        '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
                                        '<td></td>' + \
                                        '</tr>' + \
                                    '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
                                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
                                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
                                        '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />19 fibers</td>' + \
                                        '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
                                        '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
                                        '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />19 fibers</td>' + \
                                        '<td></td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
                                        '<td> ' + sncont_cr1r2spaxels_voxel_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
                                        '<td> ' + tsncont_cr1r2spaxels_voxel_string + '</td>' + \
                                        '<td> per voxel</td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
                                        '<td> ' + sncont_cr1r2spaxels_aa_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
                                        '<td> ' + tsncont_cr1r2spaxels_aa_string + '</td>' + \
                                        '<td> per AA</td>' + \
                                        '</tr>' + \
                                    '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
                                        '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
                                        '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
                                        '<td> ' + sncont_cr1r2spaxels_all_string + '</td>' + \
                                        '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
                                        '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
                                        '<td> ' + tsncont_cr1r2spaxels_all_string + '</td>' + \
                                        '<td> integrated spectrum </td>' + \
                                        '</tr>' + \
                                        '</table><br />'
            else:
                tablenewpsfstring = ''
            # TABLES NEWPSF LINE (ATTEMPT; TBD)
            # if om_val_string == 'MOS' and fluxt_val_string == 'L' and sourcet_val_string == 'E':
            #     tablenewpsflinestring = '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
            #                         '<table border=1>' + \
            #                         '<tr><th class="iconcolumn" scope="col"> </th>' + \
            #                             '<th scope="col" colspan="7">* Line SNR per spaxel zones due to PSF <br />' + \
            #                             '(MOS mode) for an extended source:<br />' + \
            #                             'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec</th>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"></th>' + \
            #                             '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
            #                             '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
            #                             '<td></td>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
            #                             '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area <br />' + nfibres_string + ' fibers</td>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
            #                             '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area<br />' + nfibres_string + ' fibers</td>' + \
            #                             '<td></td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per voxel</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per AA</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> integrated spectrum </td>' + \
            #                             '</tr>' + \
            #                         '</table><br />'
            # elif om_val_string == 'MOS' and fluxt_val_string == 'L' and sourcet_val_string == 'P':
            #     tablenewpsflinestring = '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
            #                             '<table border=1>' + \
            #                             '<tr><th class="iconcolumn" scope="col"> </th>' + \
            #                                 '<th scope="col" colspan="7">* Line SNR per spaxel zones due to PSF <br />' + \
            #                                 '(MOS mode) for a point source:<br />' + \
            #                                 'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec <br />'
            #     if resolvedline_val_string == 'N':
            #         tablenewpsflinestring = tablenewpsflinestring + \
            #                             'line FWHM = VPH FWHM = ' + fwhmline_val_string + '</th>'
            #     else:
            #         tablenewpsflinestring = tablenewpsflinestring + \
            #                             'input line FWHM = ' + fwhmline_val_string + '</th>'
            #     tablenewpsflinestring = tablenewpsflinestring + \
            #                             '</tr>' + \
            #                             '<tr><th class="iconcolumn" scope="row"></th>' + \
            #                                 '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
            #                                 '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
            #                                 '<td></td>' + \
            #                                 '</tr>' + \
            #                             '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
            #                                 '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
            #                                 '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
            #                                 '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area <br />' + nfibres_string + ' fibers</td>' + \
            #                                 '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />1 fiber</td>' + \
            #                                 '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />7 fibers</td>' + \
            #                                 '<td class="coltot"><img class="iconsize" src="/static/etc/images/icon_total_area_source.jpeg"><br />Total source area<br />' + nfibres_string + ' fibers</td>' + \
            #                                 '<td></td>' + \
            #                                 '</tr>' + \
            #                             '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
            #                                 '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
            #                                 '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
            #                                 '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td> per voxel</td>' + \
            #                                 '</tr>' + \
            #                             '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
            #                                 '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
            #                                 '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
            #                                 '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td> per AA</td>' + \
            #                                 '</tr>' + \
            #                             '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
            #                                 '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
            #                                 '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
            #                                 '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
            #                                 '<td> tofill </td>' + \
            #                                 '<td> integrated spectrum </td>' + \
            #                                 '</tr>' + \
            #                             '</table><br />'
            # elif om_val_string == 'LCB' and fluxt_val_string == 'L' and sourcet_val_string == 'E':
            #     tablenewpsflinestring = '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
            #                         '<table border=1>' + \
            #                         '<tr><th class="iconcolumn" scope="col"> </th>' + \
            #                             '<th scope="col" colspan="7">* Line SNR per spaxel zones due to PSF <br />' + \
            #                             '(LCB mode) for an extended source:<br />' + \
            #                             'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec</th>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"></th>' + \
            #                             '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
            #                             '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
            #                             '<td></td>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
            #                             '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
            #                             '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
            #                             '<td>percentage of enclosed total flux</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per voxel</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per AA</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> integrated spectrum </td>' + \
            #                             '</tr>' + \
            #                         '</table><br />'
            # elif om_val_string == 'LCB' and fluxt_val_string == 'L' and sourcet_val_string == 'P':
            #     tablenewpsflinestring = '<br />(at lambda_line = ' + wline_val_string + ' AA)' + \
            #                         '<table border=1>' + \
            #                         '<tr><th class="iconcolumn" scope="col"> </th>' + \
            #                             '<th scope="col" colspan="7">* Line SNR per spaxel zones due to PSF <br />' + \
            #                             '(LCB mode) for a point source:<br />' + \
            #                             'fiber diameter=0.62 arcsec; Seeing FWHM=' + seeingx_string + ' arcsec<br />'
            #     if resolvedline_val_string == 'N':
            #         tablenewpsflinestring = tablenewpsflinestring + \
            #                             'line FWHM = VPH FWHM = ' + fwhmline_val_string + '</th>'
            #     else:
            #         tablenewpsflinestring = tablenewpsflinestring + \
            #                             'input line FWHM = ' + fwhmline_val_string + '</th>'
            #     tablenewpsflinestring = tablenewpsflinestring + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"></th>' + \
            #                             '<th scope="col" colspan="3" class="perframecolumn">** per frame</th>' + \
            #                             '<th scope="col" colspan="3" class="allframecolumn">** all frames</th>' + \
            #                             '<td></td>' + \
            #                             '</tr>' + \
            #                         '<tr><th class="iconcolumn" scope="row"><img class="iconsize" src="/static/etc/images/icon_psfrings.jpeg" /></th>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
            #                             '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
            #                             '<td class="colc"><img class="iconsize" src="/static/etc/images/icon_psfrings_c.jpeg"><br />C<br />(' + seeing_centermean_string +'%)<br />1 fiber</td>' + \
            #                             '<td class="colcr1"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1.jpeg"><br />C+R1<br />(' + seeing_cr1_string + '%)<br />7 fibers</td>' + \
            #                             '<td class="colcr1r2"><img class="iconsize" src="/static/etc/images/icon_psfrings_cr1r2.jpeg"><br />C+R1+R2<br />(' + seeing_cr1r2_string + '%)<br />19 fibers</td>' + \
            #                             '<td>percentage of enclosed total flux</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_pspfwhm.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_voxel_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_voxel_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per voxel</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_peraa.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_aa_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_aa_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> per AA</td>' + \
            #                             '</tr>' + \
            #                         '<tr><td class="iconcolumn"><img class="iconsize" src="/static/etc/images/icon_integrated.jpeg" /></td>' + \
            #                             '<td class="perframecolumn"> ' + sncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + sncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td class="perframecolumn"> ' + tsncont_centerspaxel_all_string + ' </td>' + \
            #                             '<td> ' + tsncont_cr1spaxels_all_string + '</td>' + \
            #                             '<td> tofill </td>' + \
            #                             '<td> integrated spectrum </td>' + \
            #                             '</tr>' + \
            #                         '</table><br />'
            # else:
            #     tablenewpsflinestring = "no line output"

            # NOT WORKING YET SO SETTING TO EMPTY
            tablenewpsflinestring = ''

            # FOR DOWNLOADABLE FILES
            forfileoutputstring = outputofcalc['forfileoutput']
            forfileoutput2string = outputofcalc['forfileoutput2']

            # EXTRA FOOTER
            footerstring = '<span class="italicsmall">Time of request: ' + start_time_string + ' ; End of request: ' + time.strftime("%H:%M:%S") + '</span>'

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
            footerstring = ''

        html2 = ''  # for testing
        # print html2

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
                             'footerstring': footerstring,
                             })
