import math
from StringIO import StringIO
import pkgutil
import numpy

from .numeric import mag2flux, sclspect, specpar, signal, dark
from .numeric import darknoisesq, readoutnoise, flux2mag, specparline
from .numeric import linesignal

from .models import PhotometricFilter
from .models import SpectralTemplate, VPHSetup


####################
def reading(filename, skipline):
    alldata = pkgutil.get_data('etc', "data/%s" % filename)
    psfile = StringIO(alldata)
    return numpy.loadtxt(psfile, unpack=True)


# ********************************
# Finding out if input is a float.

def isafloat(inp, val):
    try:
        inp = float(inp)
    except ValueError:
        inp = val
    return inp

# ********************************
# Text for output in warning and help windows.

def outmessage(textcode):
    '''Text for output in warning and help windows.'''
    # Input textcode is an integer
    # HELP buttons
    if textcode == 0:
        outtext = ''
    elif textcode == 1:
        outtext = "** SOURCE SIZE **\nFor extended sources, apparent projected area of source in arcsec**2. Circular shape is assumed for the source.\nThis parameter is available only if the 'Source Type=Extended' option is set."
    elif textcode == 2:
        outtext = "** CONTINUUM MAGNITUDE **\nFor point sources, Vega apparent magnitude of the source continuum in the selected continuum band.\nFor extended sources, the magnitude must be provided per arcsec**2 in the selected band.\nOnly available if 'Continuum flux' option is not set."
    elif textcode == 3:
        outtext = "** CONTINUUM FLUX **\nFor point sources, flux of source continuum in c.g.s. unit system (erg/s/cm**2/AA) in the selected continuum band.\nFor extended sources, this flux is provided per arcsec**2.\nOnly available if the 'Continuum Magnitude' option is not set."
    elif textcode == 4:
        outtext = "** LINE FLUX **\nFor point sources, flux of line in c.g.s. unit system (erg/s/cm**2).\nFor extended sources, this flux must be provided per arcsec**2.\nThis parameter is available only if the 'Continuum+Line' option is set."
    elif textcode == 5:
        outtext = "** LINE WAVELENGTH **\nLine wavelength in Angstroms.\nThis parameter is available only if the 'Continuum+Line' option is set."
    elif textcode == 6:
        outtext = "** LINE FWHM **\nLine FWHM in Angstroms.\nIf the line is not resolved, the nominal FWHM of the selected VPH at its central wavelength is assumed.\nThis parameter is available only if the 'Continuum+Line' and 'Resolved line=yes' options are set."
    elif textcode == 7:
        outtext = "** AIRMASS **\nAirmass scales the number of photons from the sky background with according to the following expression: (-0.000278719*X**3 - 0.0653841*X**2 + 1.11979*X - 0.0552132)."
    elif textcode == 8:
        outtext = "** SEEING **\nSeeing in arcsec.\nThe seeing is assumed to be provided at the given airmass. No correction for airmass is performed."
    elif textcode == 9:
        outtext = "** APERTURE FOR THE SPECTRAL LINE **\nAperture to derive line flux in spectrum, in line FWHM units.\nThis parameter is available only if the 'Continuum+Line' option is set."
    elif textcode == 10:
        outtext = "** NUMBER OF SKY BUNDLES **\nNumber of sky mini-bundles used (max. = 100).\nEach minibundle has 7 fibres.\nThe bundles of 8 robotic actuators, located at the corners\nof the MOS FoV, are used to measure the sky in the LCB observing mode.\nThey are projected at different positions along the pseudo-slit\nto estimate projection effects and different transmissions of instrument depending on the spectrum position in the\ndetector."
    elif textcode == 11:
        outtext =  "** APERTURE FOR CONTINUUM SUBSTRACTION **\nAperture to estimate continuum around the line for continuum-sustraction, in line FWHM units.\nThis parameter is available only if the 'Continuum+Line' option is set."
    elif textcode == 12:
        outtext = "** VPH SETUP **\nConsult the characteristics of each spectral setup in the figure below.\nThe wavelength of the input spectral line must be located into the wavelength range of the selected VPH."
    elif textcode == 13:
        outtext = "** INPUT PARAMETERS **\nA summary of the selected input parameters is provided here, with some warnings and extra information about the input source flux distribution (as if line FWHM is dominated by the VPH FWHM, if the seeing determines the image area instead of the projected area of source, the continuum flux equivalent to an input magnitude, or the sky flux considered)."
    elif textcode == 14:
        outtext = "** OUTPUT CONTINUUM SNRs **\n\nThe SNRs of the continuum input flux distribution expected for the input observational and instrumental setup, and for the input atmospheric conditions are provided.\n\nIn case the input source is punctual, the provided SNRs are for:\n * one fibre, in one spectral FWHM(*2), in 1 Angstrom, in the total integrated spectrum;\n * per detector pixel;\n * the total source area(*1), in one spectral FWHM (*2), in 1 Angstrom, in the total integrated spectrum.\n\nIn case of extended sources, the following outputs are additionally provided:  \n * for 1 seeing disk, in one spectral FWHM(*2), in 1 Angstrom, in the total integrated spectrum;\n * for 1 arcsec**2, in one spectral FWHM(*2), in 1 Angstrom, in the total integrated (integrated) spectrum.\n\n Note: (*1) The number of fibres required to sample the whole source is also provided.\n         (*2) At least, 3.6 spectral pixels in LCB/MOS modes are required to fulfill the Nyquist-Shanon sampling theorem in spectral direction (the VPH FWHM is projected onto 3.6 spectral pixels for all VPHs in LCB/MOS, by construction)."
    elif textcode == 15:
        outtext = "** OUTPUT LINE SNRs **\n\nThe SNRs of the line input flux distribution expected for the input observational and instrumental setup, and for the input atmospheric conditions are provided.\n\nIn case the input source is punctual, the provided SNRs are for(*1):\n * per arcsec and per Angstrom in the detector(*2);\n * in one fibre, in the selected line spectral aperture(*3);\n * in one fibre per Angstrom(*2);\n * per voxel(*4,*5);\n * per detector pixel(*6);\n * the total source area, in the selected line spectral aperture(*3).\n\nIn case of extended sources, the following outputs are additionally provided:  \n * for 1 seeing disk, in the selected line spectral aperture(*); \n * for 1 arcsec**2, in the selected line spectral aperture(*).\n\n Note: (*1) Considering that all the line flux is completely enclosed into the FWHM of the line.\n         (*2) Assuming a spectral aperture of 1 Angstrom.\n         (*3) Assuming the selected spectral apertures for line and continuum subtraction indicated as inputs. If you want to know exactly the SNR in 1 line FWHM, set the spectral apertures of line to 1 (i.e., to one line FWHM).\n         (*4) Assuming one spectral FWHM as spectral aperture (i.e., the FWHM of the selected VPH).\n         (*5) A voxel is the minimum spatial and spectral resolution element sampled. In our case, a voxel is the projection of the whole fibre (minimum spatial resolution element) into the FWHM of the VPH in the spectral direction (minimum spectral resolution element according to the Nyquist-Shanon sampling theorem). The FWHM of all VPHs in MEGARA is projected onto 3.6 spectral pixels in LCB/MOS and onto 2.5 pixels by design.\n         (*6) Assuming 1 spectral pixel as spectral aperture."
    elif textcode == 16:
        outtext = "** OBSERVING MODES **\nMEGARA provides two observing modes according to the design on December, 2014:\n\n * Large Compact Bundle (LCB):\n   An IFU covering 12.5x11.3 arcsec^2, with fibers of 0.62 arcsec diameter and a 1D spectral FWHM sampling of 3.6 pix.\n\n  * Multi-Object Spectrograph (MOS):\n   This mode allows observing up to 100 targets in a region of 3.5x3.5 arcmin^2, with fibers of 0.62 arcsec diameter and a 1D spectral FWHM sampling of 3.6 pix."


    # WARNING MESSAGES
    elif textcode == 100:
        outtext = "** WARNING **\nMagnitude value must be < 35."
    elif textcode == 101:
        outtext = "** WARNING **\nContinuum flux value must be > 0."
    elif textcode == 102:
        outtext = "** WARNING **\nLine flux value must be > 0."
    elif textcode == 103:
        outtext = "** WARNING **\nWavelength line value must be > 0."
    elif textcode == 104:
        outtext = "** WARNING **\nFWHM of line value must be > 0."
    elif textcode == 105:
        outtext = "** WARNING **\nNo. of line FWHMs to derive line flux value must be >= 1."
    elif textcode == 106:
        outtext = "** WARNING **\nNo. of line FWHMs to derive continuum flux value must be >= 1."
    elif textcode == 107:
        outtext = "** WARNING **\nAirmass value must be 1 <= X < 3."
    elif textcode == 108:
        outtext = "** WARNING **\nSeeing value must be 0 < Seeing <= 3.0."
    elif textcode == 109:
        outtext = "** WARNING **\nExptime value must be 0 < Exptime <1e6"
    elif textcode == 110:
        outtext = "** WARNING **\nNo. of sky mini-bundles must be 1 <= No. bundles <= 89 (LCB) or 92 (MOS)"
    elif textcode == 111:
        outtext = "** WARNING **\nThe line wavelength is outside the VPH wavelength range."
    elif textcode == 112:
        outtext = "** WARNING **\nThe object is wider than the MEGARA field of view."
    elif textcode == 113:
        outtext = "** WARNING **\nThe number of frames must be at least 1."
    elif textcode == 114:
        outtext = "** WARNING **\nExptime per frame value must be 0 < Exptime per frame <1e6"
    elif textcode == 115:
        outtext = ""
    else:
        outtext = ""

    return outtext

# ********************************
# Function to create the text for giving final output for input parameters.

def outtextinp(om_val, bandc_val, sourcet_val, mag_val, netflux, isize_val,
               size_val, radius_val,
               seeingx, pi, fluxt_val, wline_val, fline_val, fwhmline_val,
               vph_val, skycond_val, moon_val, airmass_val, seeing_zenith, fsky, numframe_val,
               exptimepframe_val, exptime_val, npdark_val, nsbundles_val, nsfib_val,
               nfwhmline_val, cnfwhmline_val, resolvedline_val, bandsky):

    if sourcet_val == "P":
        text = '* Source type: Point\n  Continuum: %s = %5.3f mag\n' % (bandc_val,mag_val)
        text = text + '  Continuum Flux = %7.3e cgs\n' % (netflux)
    else:
        text = '* Source type: Extended\n  Continuum: V = %5.3f mag/arcsec**2\n' % (mag_val)
        text = text + '  Flux = %7.3e cgs\n' % (netflux)
        text = text + '  Radius = %5.2f arcsec\n' % (radius_val)
        text = text + '  Area = %5.2f arcsec**2\n' % (size_val)

    if seeingx >= (2. * math.sqrt (size_val / pi)) and sourcet_val == "E":
        text = text + '  ** SEEING-DOMINATED ** \n'

    if fluxt_val == "L":
        text =  text + '  Line: Lambda = %7.1f AA\n  Line: Flux = %7.3e cgs\n  Line: FWHM = %3.1f AA\n' % (wline_val, fline_val, fwhmline_val)
        if resolvedline_val == "N":
            text = text + '  ** Non-resolved line **\n  ** Line FWHM set by VPH **\n'


    text = text + '* Instrument: \n  Obs. Mode = %3s\n' % (om_val)
    text = text + '  VPH = %10s\n' % (vph_val)

    text = text + '* Sky: \n  Condition = %15s \n  Moon = %6s\n  Airmass: X = %3.2f\n  Seeing(@X=1) = %4.2f\n' % (skycond_val, moon_val, airmass_val, seeing_zenith)
    text = text + '  Sky-flux(%s,@X) = %7.3e cgs\n  Seeing(@X) = %4.2f\n' % (bandsky, fsky, seeingx)
    text = text + '* Observation: \n  Num. of frames = %6i\n  Exptime/frame = %7.1f\n  Total Exptime = %7.1f\n  NP_Dark = %6i\n  Sky-bundles = %i, Bundles = %i\n' % (numframe_val, exptimepframe_val, exptime_val, npdark_val, nsbundles_val, nsfib_val)

    if fluxt_val == "L":
        text =  text + '  Spectral apertures:\n    For line=%2i\n    For continuum=%2i\n' % (nfwhmline_val, cnfwhmline_val)

    # Adding blank spaces, to overwrite previous outputs
    textfile = text
    textfile= " INPUT PARAMETERS:\n" + textfile
    # textfile = "**************************\n* MEGARA ETC OUTPUT FILE *\n**************************\n" + textfile      # FOR DJANGO

    if (sourcet_val == "P"):
        text = text + "\n"

    if seeingx < (2. * math.sqrt (size_val / pi)) or sourcet_val == "E":
        text = text + "\n"

    if (fluxt_val == "C"):
        text = text + "\n\n\n\n\n\n\n"

    if fluxt_val == "L" and resolvedline_val == "Y":
        text = text + "\n\n"


    return text,textfile


# ********************************
# Function to create the text for giving final output for continuum.

def outtextoutc(sourcet_val,nfibres, nfib, nfib1,
                sncont_p2sp_all, tsncont_p2sp_all,
                sncont_1aa_all, tsncont_1aa_all,
                sncont_band_all, tsncont_band_all,
                sncont_p2sp_fibre, tsncont_p2sp_fibre,
                sncont_1aa_fibre, tsncont_1aa_fibre,
                sncont_band_fibre, tsncont_band_fibre,
                sncont_p2sp_seeing, tsncont_p2sp_seeing,
                sncont_1aa_seeing, tsncont_1aa_seeing,
                sncont_band_seeing, tsncont_band_seeing,
                sncont_p2sp_1, tsncont_p2sp_1,
                sncont_1aa_1, tsncont_1aa_1,
                sncont_band_1, tsncont_band_1,
                sncont_psp_pspp, tsncont_psp_pspp,
                lambdaeff):

    # Output in one fibre
    text = '* SNR per fibre:\n'
    # Output per spectral and spatial pixel
    text = text + ' %4.2f // %4.2f per detector pixel\n' % (sncont_psp_pspp, tsncont_psp_pspp)
    # Output per spectral pixel
    text = text + ' %4.2f // %4.2f per spectral pixel\n' % (sncont_psp_pspp*2, tsncont_psp_pspp*2)
    text = text + ' %4.2f // %4.2f per spectral FWHM (voxel)\n' \
                  ' %4.2f // %4.2f per AA\n' \
                  % (sncont_p2sp_fibre, tsncont_p2sp_fibre,\
                     sncont_1aa_fibre, tsncont_1aa_fibre)
                     # sncont_band_fibre, tsncont_band_fibre)
                  # '%4.2f // %4.2f integrated spectrum (spaxel)\n' \


    # Output in all spectrum
    text = text + '\n * SNR in total source area:\n  (no. of fibres~%5.1f)\n' % nfibres
    text = text + ' %4.2f // %4.2f per spectral pixel\n' \
                  ' %4.2f // %4.2f per spectral FWHM\n' \
                  ' %4.2f // %4.2f per AA\n' \
                  % (sncont_p2sp_all/2, tsncont_p2sp_all/2,\
                      sncont_p2sp_all, tsncont_p2sp_all,\
                     sncont_1aa_all, tsncont_1aa_all)
                     # sncont_band_all, tsncont_band_all)

    # Output in 1 FWHM (only if source is extended, different from previous one)
    if sourcet_val == "E":
        text = text + '\n* SNR in 1 seeing:\n'
        if nfib > 0.:
            text = text + ' (no. of fibres~%5.1f)\n' % nfib
        text = text + ' %4.2f // %4.2f per spectral FWHM\n' \
                      ' %4.2f // %4.2f per AA\n' \
                      ' %4.2f // %4.2f integrated spectrum (spaxel)\n' \
                      % (sncont_p2sp_seeing, tsncont_p2sp_seeing,\
                         sncont_1aa_seeing, tsncont_1aa_seeing,\
                         sncont_band_seeing, tsncont_band_seeing)

    # Output in 1 arcsec**2 (only if source is extended, different from previous one)
    if sourcet_val == "E":
        text = text + '\n* SNR in 1 arcsec**2:\n'

        if nfib1 > 0.:
            text = text + ' %4.2f // %4.2f per spectral FWHM\n' \
                          ' %4.2f // %4.2f per AA\n    ' \
                          ' %4.2f // %4.2f integrated spectrum (spaxel)\n' \
                          % (sncont_p2sp_1, tsncont_p2sp_1,\
                             sncont_1aa_1, tsncont_1aa_1,\
                             sncont_band_1, tsncont_band_1)

    # Adding blank spaces, to overwrite previous outputs
    textfile = text
    textfile = " OUTPUT CONTINUUM SNR \n"+\
               " (at lambda_c = "+ str(lambdaeff) +" AA)\n" \
               " (of frame // of total)\n" + textfile

    if (sourcet_val == "P"):
        text = text + "\n\n\n\n\n\n\n\n"
    elif (sourcet_val == "E" and nfib <= 0.):
        text = text + "\n"
    elif (sourcet_val == "E" and nfib1 <= 0.):
        text = text + "\n"
    else:
        pass

    return text,textfile


# ********************************
# Function to create the text for giving final output for line output.

def outtextoutl(fluxt_val,\
                snline_all, snline_fibre,\
                snline_pspp, snline_1_aa,\
                sourcet_val, snline_seeing,\
                snline_1, snline_spaxel,\
                snline_fibre1aa):

    if fluxt_val == "L":

        # Output in 1 arcsec**2 (only if source is extended, different from previous one)
        # In 1 AA and 1 arcsec in spatial direction
        text = '* SNR per arcsec per AA = %4.2f\n' % (snline_1_aa)

        # Output in one fibre, the whole line
        text = text + '* SNR in 1 fibre (in aperture) = %4.2f\n' % (snline_fibre)
        text = text + '* SNR in 1 fibre (in 1 AA) = %4.2f\n' % (snline_fibre1aa)

        # Output per voxel: in one spectral FWHM * dimension of fibre in spatial direction
        text = text + '* SNR per voxel = %4.2f\n' % (snline_spaxel)  # OJO: el nombre de esta variable no parece apropiado (NCL's comment)

        # Output per spatial pixel
        text = text + '* SNR per detector pixel = %4.2f\n' % (snline_pspp)

        # Output in all source area in the whole line (considering FWHM of line)
        text = text + '* SNR total (in aperture) = %4.2f\n' % (snline_all)

        # For the whole line, if extended source:
        if sourcet_val == "E":
            text = text + '* SNR in 1 seeing = %4.2f\n' % (snline_seeing)
            text = text + '* SNR in 1 arcsec**2 = %4.2f\n' % (snline_1)

        textfile = text
        textfile =  " OUTPUT LINE SNR: \n" + textfile
        if sourcet_val == "E":
            text = text + "\n\n"

    # End of if fluxt_val == "L"
    else:
        text = '*** None selected ***\n\n\n\n\n\n\n'
        textfile =  ' OUTPUT LINE SNR: \n*** None selected ***\n'

    return text,textfile

# ********************************
# Function to create the text for giving final output for line output.
# Returns errind = 1 if called. This index implies that no computation is performed in main()
# and an error message is sent.
# Args: outtext - error message.

# class LabelFoo(Exception):
#         pass


def warn(outtext,framex,title):
    # message(outtext,framex,title)     # COMMENTED FOR DJANGO
    # try:
    #    raise LabelFoo('esto', 'funciona')
    # except LabelFoo, inst:
    #     print inst.args      # los argumentos guardados en .args
    #    x, y = inst          # __getitem__ permite desempaquetar los args "
    #    print 'x =', x,y
    errind = 1
    return errind











# Initializing strings of output
global texti,textoc,textol
texti = ""
textoc = ""
textol = ""

# Global definitions
# Constants
hplanck = 6.62606885e-27  # Planck constant (ergs/s)
lightv = 2.99792458e10    # Light velocity (cm/s)
pi = 2. * math.acos(0.)

# Instrument definitions
# Number of fibres per mini-bundle for sky
nsfibres = 7.0

# Dark current in e-/pix/s
dc = 0.02/3600.0

# Readout noise (e- rms)
ron = 2.8

# Telescope effective radius for collecting area = 74.14 m**2 (in m).
rt = 4.858

# Dimensions of detector (Horizontal direction)
npy = 4096.0

# Dimensions of detector (Vertical direction). Plus 16 rows devoted to dark? npy = 4112
npx = 4096.0


# vph_list = list( [o.name for o in VPHSetup.objects.all()] )
# reads the database every time it is called, so better not use it too much.
# To avoid multiple database loads,
# simply save the QuerySet and reuse it as follows:
queryvph = VPHSetup.objects.all()
vph_list = list([str(p.name) for p in queryvph if p.name != u'-empty-'])
# vph_list = ['HR-R', 'HR-I', 'MR-U', 'MR-UB', 'MR-B', 'MR-G', 'MR-V', 'MR-VR',\
#            'MR-R', 'MR-RI', 'MR-I', 'MR-Z',\
#            'LR-U', 'LR-B', 'LR-V', 'LR-R', 'LR-I', 'LR-Z']

vphchar = list( [(p.fwhm, p.dispersion, p.deltab, p.lambdac, p.relatedband,\
                  p.lambda_b, p.lambda_e, p.specconf) for p in queryvph if p.name != u'-empty-'])
# VPH configurations: FWHM @lambda_c, Dispersion (AA/pix), DeltaB (AA),
#                     lambda_c (AA)  Band_of_VPH_to_relate_with_Vega_zp lambda_0 lambda_f Spectrograph_configuration
# Band_of_VPH_to_relate_with_Vega_zp must be defined in bandc_list
# vphchar = [(0.354, 0.089, 380.0, 6650.0, 'R', 6450., 6830., 'HR'),  # 'HR-R'
#            (0.462, 0.116, 491.0, 8630.0, 'I', 8379., 8870., 'HR'),  # 'HR-I'
#            (0.358, 0.090, 360.0, 4104.0, 'U', 3917., 4277., 'MR'),  # 'MR-U'
#            (0.394, 0.099, 396.0, 4431.0, 'B', 4225., 4621., 'MR'),  # 'MR-UB'
#            (0.435, 0.109, 438.0, 4814.0, 'B', 4586., 5024., 'MR'),  # 'MR-B'
#            (0.476, 0.119, 480.0, 5213.0, 'V', 4963., 5443., 'MR'),  # 'MR-G'
#            (0.523, 0.131, 526.0, 5667.0, 'V', 5393., 5919., 'MR'),  # 'MR-V'
#            (0.574, 0.144, 578.0, 6170.0, 'V', 5869., 6447., 'MR'),  # 'MR-VR'
#            (0.613, 0.153, 618.0, 6563.0, 'R', 6241., 6859., 'MR'),  # 'MR-R'
#            (0.669, 0.167, 673.0, 7115.0, 'I', 6764., 7437., 'MR'),  # 'MR-RI'
#            (0.733, 0.183, 738.0, 7767.0, 'I', 7382., 8120., 'MR'),  # 'MR-I'
#            (0.875, 0.219, 886.0, 9262.0, 'I', 8800., 9686., 'MR'),  # 'MR-Z'
#            (0.739, 0.185, 733.0, 4051.0, 'U', 3653., 4386., 'LR'),  # 'LR-U'
#            (0.871, 0.218, 864.0, 4800.0, 'B' ,4332., 5196., 'LR'),  # 'LR-B'
#            (1.030, 0.261, 1021.0, 5695.0, 'V' , 5143., 6164., 'LR'),  # 'LR-V'
#            (1.217, 0.304, 1206.0, 6747.0, 'R' , 6094., 7300., 'LR'),  # 'LR-R'
#            (1.439, 0.360, 1426.0, 7991.0, 'I' , 7220., 8646., 'LR'),  # 'LR-I'
#            (1.600, 0.400, 1587.0, 8900.0, 'I' , 8043., 9630., 'LR')]  # 'LR-Z'


# Templates of spectrum of different astronomical objects
queryspec = SpectralTemplate.objects.all()
spect_list = list([str(p.name) for p in queryspec])
# spect_list = ['Uniform', 'Elliptical', 'S0', 'Sa', 'Sb', 'Sc', 'NGC1068', 'M2 I', 'Starburst1',
#              'Starburst2','Starburst3','Starburst4','Starburst5','Starburst6',
#              'Bulge', 'Liner', 'QSO', 'Sy1', 'Sy2', 'Orion', 'PN',
#              'O5 V','O7 V',
#              'O9 V', 'B0 V', 'B1 V','B3 V', 'B5 V', 'B8 V',
#              'A1 V', 'A3 V', 'A5 V', 'F0 V', 'F2 V', 'F5 V',
#              'F8 V', 'G2 V', 'G5 I',
#              'G5 V', 'G8 V', 'K0 V', 'K4 V', 'K7 V',
#              'M2 V', 'M4 V', 'M6 V']

specttmplt_list = list( [str(p.path) for p in queryspec])
# specttmplt_list = ['SPECTRA_0.1aa/uniform.dat', 'SPECTRA_0.1aa/Elliptical.dat', 'SPECTRA_0.1aa/S0.dat',
#              'SPECTRA_0.1aa/Sa.dat', 'SPECTRA_0.1aa/Sb.dat', 'SPECTRA_0.1aa/Sc.dat',
#              'SPECTRA_0.1aa/NGC1068.dat','SPECTRA_0.1aa/M2I.dat', 'SPECTRA_0.1aa/Starburst1.dat',
#              'SPECTRA_0.1aa/Starburst2.dat', 'SPECTRA_0.1aa/Starburst3.dat', 'SPECTRA_0.1aa/Starburst4.dat',
#              'SPECTRA_0.1aa/Starburst5.dat', 'SPECTRA_0.1aa/Starburst6.dat', 'SPECTRA_0.1aa/Bulge.dat',
#              'SPECTRA_0.1aa/Liner.dat', 'SPECTRA_0.1aa/QSO.dat', 'SPECTRA_0.1aa/Sy1.dat', 'SPECTRA_0.1aa/Sy2.dat',
#              'SPECTRA_0.1aa/Orion.dat', 'SPECTRA_0.1aa/PN.dat', 'SPECTRA_0.1aa/O5V.dat', 'SPECTRA_0.1aa/O7V.dat',
#              'SPECTRA_0.1aa/O9V.dat', 'SPECTRA_0.1aa/B0V.dat', 'SPECTRA_0.1aa/B1V.dat', 'SPECTRA_0.1aa/B3V.dat',
#              'SPECTRA_0.1aa/B5V.dat', 'SPECTRA_0.1aa/B8V.dat', 'SPECTRA_0.1aa/A1V.dat', 'SPECTRA_0.1aa/A3V.dat',
#              'SPECTRA_0.1aa/A5V.dat', 'SPECTRA_0.1aa/F0V.dat', 'SPECTRA_0.1aa/F2V.dat', 'SPECTRA_0.1aa/F5V.dat',
#              'SPECTRA_0.1aa/F8V.dat', 'SPECTRA_0.1aa/G2V.dat', 'SPECTRA_0.1aa/G5I.dat', 'SPECTRA_0.1aa/G5V.dat',
#              'SPECTRA_0.1aa/G8V.dat', 'SPECTRA_0.1aa/K0V.dat', 'SPECTRA_0.1aa/K4V.dat', 'SPECTRA_0.1aa/K7V.dat',
#              'SPECTRA_0.1aa/M2V.dat', 'SPECTRA_0.1aa/M4V.dat', 'SPECTRA_0.1aa/M6V.dat']

# Band for continuum list
queryband = PhotometricFilter.objects.all()
bandc_list = list( [str(p.name) for p in queryband])
# bandc_list = ['U', 'B', 'V', 'R', 'I']

filterc_list = list( [str(p.path) for p in queryband])
# filterc_list = ['FILTERS_0.1aa/u_johnsonbessel.dat','FILTERS_0.1aa/b_johnsonbessel.dat',
#                 'FILTERS_0.1aa/v_johnsonbessel.dat','FILTERS_0.1aa/r_johnsonbessel.dat',
#                 'FILTERS_0.1aa/i_johnsonbessel.dat']

# Central Wavelength and width of filters.
filterchar_list = list( [(p.cwl, p.width, p.lambda_b, p.lambda_e) for p in queryband])
# filterchar_list = [(3657.5, 577.0, 3369.0, 3946.),   # For Johnson-Cousins U-band
#                    (4334.5, 975.0, 3847., 4822.),   # For Johnson-Cousins B-band
#                    (5374.0, 846.0, 4951., 5797.),   # For Johnson-Cousins V-band
#                    (6272.5, 1273.0, 5635.5, 6909.),  # For Johnson-Cousins R-band
#                    (8722.0, 2980.0, 7232., 10212.)]  # For Johnson-Cousins I-band


# Vega magnitude and flux (erg/s/cm**2/AA according to selected continuum band, following order of bandc_list
# Colina 1996
vegachar = list( [(p.mvega, p.fvega) for p in queryband])
# vegachar = [(0.030,4.22e-9),   # For Johnson-Cousins U-band
#             (0.035,6.20e-9),   # For Johnson-Cousins B-band
#             (0.035,3.55e-9),   # For Johnson-Cousins V-band
#             (0.075,1.795e-9),  # For Johnson-Cousins R-band
#             (0.095,8.60e-9)]   # For Johnson-Cousins I-band

# Sky emission, for bright, grey, dark nights in La Palma, in mag/arcsec**2 in the V-band.
# (I. Skillen, 2002, ING Technical Note 127)
# Asssuming difference of emission between dark-bright and dark-grey is constant with optical band
# Substracting 0.5 mag/arcs**2 due to zodiacal light, airglow, starlight (brighter emission).
moon_list = ['Bright', 'Grey', 'Dark']
extraskyemission = [-3.1, -1.5, -0.5]

# Near-zenith dark-of-moon broad-band sky brightness at La Palma for different bands
# Units: Mag/arcsec**2 (C.R.Benn & S.L. Ellison, 1997, La Palma technical note 115.)
# Independent of atmospheric extinction, not variable during the night, but with solar cycle,
# latitude and airmass

bandsky_list = ['U', 'B', 'V', 'R', 'I']
skymag_list = [22.0,   # Sky U
               22.7,   # Sky B
               21.9,   # Sky V
               21.0,   # Sky R
               20.0]   # Sky I


# Transmission curves
# Atmospheric transmission at La Palma: 72% @400 nm, 80% @450 nm, 84% @500 nm
# Preub, Hermann, Hofmann, & Kohnle NIMPR.
# Section A, Volume 481, Issues 1-3, 1 April 2002, Pages 229-240
tatmdat = "MEGARA_TRANSM_0.1aa/atmt_total_0.1aa.dat"

# Reading transmission curve of atmosphere
lamb, tatm = reading(tatmdat,2)
tatm = numpy.array(tatm)

# Atmospheric conditions: (in magnitude)
# Photometric = 10^(-0.4*0), Clear = 10^(-0.4*0.4), Spectroscopic = 10^(-0.4*1)
skycond_list = ['Photometric', 'Clear', 'Spectroscopic']
tcond = [1,             # Photometric
         0.69183097091, # Clear
         0.39810717055  # Spectroscopic
         ]
# tcond = [1,
#          0.4,
#          0
#          ]

#######
# Compute results
def calc(sourcet_val, inputcontt_val, mag_val, fc_val,\
         isize_val, size_val, radius_val,\
         fluxt_val,\
         fline_val, wline_val,\
         nfwhmline_val, cnfwhmline_val,\
         fwhmline_val, resolvedline_val,\
         spect_val, bandc_val,\
         om_val,vph_val,\
         skycond_val, moon_val, airmass_val, seeing_val,\
         numframe_val, exptimepframe_val, nsbundles_val):

    global texti, textoc, textol
    # Clear previous outputs
    # Warning
    errind = 0
    frame0 = 0

    # Source type

    # Magnitude continuum; checking float
    if inputcontt_val == "M":
        mag_val = isafloat (mag_val, 20.0)
        if abs(mag_val) > 35.0 :
            mag_val = 20.0
            outtext = outmessage(100)
            errind = warn(outtext,frame0,'MEGARA ETC Warning')

    else:
        fc_val = isafloat(fc_val, 1.0e-16)
        if fc_val <= 0.0:
            fc_val = 1.0e-16
            outtext = outmessage(101)
            errind = warn(outtext,frame0,'MEGARA ETC Warning')

    # Size if extended in arcsec**2; checking float
    size_val = isafloat(size_val, 1.0)
    radius_val = isafloat(radius_val, 1.0)
    if sourcet_val == "P":
        size_val = 0.
        radius_val = 0.

    # Type of computation: continuum or line+continuum
    # Input parameters related to Line
    if fluxt_val == "L":
        fline_val = isafloat(fline_val, 1.0e-13)
        if fline_val <= 0.0:
            fline_val = 1.0e-13
            outtext = outmessage(102)
            errind = warn(outtext,frame0,'MEGARA ETC Warning')
        wline_val = isafloat(wline_val, 6562.8)
        if wline_val <= 0.0:
            wline_val = 6562.8
            outtext = outmessage(103)
            errind = warn(outtext,frame0,'MEGARA ETC Warning')

        # Considering only down to first decimal of wavelength
        wline_val =  wline_val * 10.
        wline_val =  math.ceil (wline_val)
        wline_val =  wline_val / 10.
        wline_val = numpy.array(wline_val)

        if resolvedline_val == "Y":
            fwhmline_val = isafloat(fwhmline_val, 0.5)
        else: # We will assign its value after reading the VPH in this case
            fwhmline_val = 0.5
        if fwhmline_val <= 0.0:
            fwhmline_val = 0.5
            outtext = outmessage(104)
            errind = warn(outtext,frame0,'MEGARA ETC Warning')

        nfwhmline_val = isafloat(nfwhmline_val, 1.0)
        if nfwhmline_val < 1.0:
            nfwhmline_val = 1.0
            outtext = outmessage(105)
            errind = warn(outtext,frame0,'MEGARA ETC Warning')

        cnfwhmline_val = isafloat(cnfwhmline_val, 1.0)
        if cnfwhmline_val < 1.0:
            cnfwhmline_val = 1.0
            outtext = outmessage(106)
            errind = warn(outtext,frame0,'MEGARA ETC Warning')
    else:
        fline_val = 0.
        wline_val = 0.
        fwhmline_val = 0.
        nfwhmline_val = 0.
        cnfwhmline_val = 0.

    # Airmass
    airmass_val = isafloat(airmass_val,1.0)
    if airmass_val < 1.0 or airmass_val >=3.0:
        airmass_val = 1.0
        outtext = outmessage(107)
        errind = warn(outtext,frame0,'MEGARA ETC Warning')

    # Seeing
    seeing_val = isafloat(seeing_val,0.5)
    if seeing_val <= 0.0 or seeing_val > 3.05:
        seeing_val = 0.5
        outtext = outmessage(108)
        errind = warn(outtext,frame0,'MEGARA ETC Warning')

    # Number of frame
    numframe_val = isafloat(numframe_val,1)
    if numframe_val <= 0:
        numframe_val = 1
        outtext = outmessage(113)
        errind = warn(outtext,frame0,'MEGARA ETC Warning')

    # Exptime per frame
    exptimepframe_val = isafloat(exptimepframe_val,1)
    if exptimepframe_val <= 0.0 or exptimepframe_val >= 1.e6:
        exptimepframe_val = 3600.
        outtext = outmessage(114)
        errind = warn(outtext,frame0,'MEGARA ETC Warning')

    # Exptime
    exptime_val = numframe_val * exptimepframe_val
    # exptime_val = exptime_entry.get()
    exptime_val = isafloat(exptime_val,3600.0)
    if exptime_val <= 0.0 or exptime_val >= 1.e6:
        exptime_val = 3600.
        outtext = outmessage(109)
        errind = warn(outtext,frame0,'MEGARA ETC Warning')

    # Dark
    npdark_val = 65500.

    # Sky fibres
    nsfib_val = isafloat(nsbundles_val*7,92.0) # convert from number of bundles to number of fibers. These are SKY FIBERS
    if nsfib_val <= 0. or nsfib_val > 644:
        nsfib_val = 56.
        outtext = outmessage(110)
        errind = warn(outtext,frame0,'MEGARA ETC Warning')

    # Setting dispersion, bandwidth, central wavelength, band for estimating sky flux from VPH setup,
    # and spectrograph configuration for setting instrument transmission.

    vph_val = vph_val.encode('utf-8')   # need it to get rid of unicode
    vphfeatures = vphchar[vph_list.index(vph_val)]
    # vphfeatures = VPHSetup.objects.filter
    # queryfwhmvph = list( VPHSetup.objects.filter(name=vph_val).values('fwhm') )
    # fwhmvph = queryfwhmvph[0]['fwhm']
    #
    # querydisp = list( VPHSetup.objects.filter(name=vph_val).values('dispersion') )
    # disp = querydisp[0]['dispersion']
    #
    # querydeltab = list( VPHSetup.objects.filter(name=vph_val).values('deltab') )
    # deltab = querydeltab[0]['deltab']
    #
    # queryset = list( VPHSetup.objects.filter(name=vph_val).values('lambdac') )
    # lambdaeff = queryset[0]['lambdac']
    # bandskyquery = list( VPHSetup.objects.filter(name=vph_val).values('relatedband') )
    # bandsky = bandskyquery[0]['relatedband']
    # spectrograph_conf = VPHSetup.objects.filter(name=vph_val).values('specconf')

    fwhmvph = vphfeatures[0]
    disp = vphfeatures[1]
    deltab = vphfeatures[2]
    lambdaeff = vphfeatures[3]
    bandsky = vphfeatures[4]
    spectrograph_conf = vphfeatures[7]
    #
    # Lower and upper wavelengths of VPH
    # querylvph1 = list(VPHSetup.objects.filter(name=vph_val).values('lambda_b'))
    # lvph1 = querylvph1[0]['lambda_b']
    # querylvph2 = list(VPHSetup.objects.filter(name=vph_val).values('lambda_e'))
    # lvph2 = querylvph2[0]['lambda_e']
    lvph1 = vphfeatures[5]
    lvph2 = vphfeatures[6]

    if fluxt_val == "L":
        if (wline_val <= lvph1 or wline_val >= lvph2 ):
            outtext = outmessage(111)
            errind = warn(outtext,frame0,'MEGARA ETC Warning')

    # Avoiding computations if exception found
    if errind == 0:

        # Reading template
        spectdat = specttmplt_list[spect_list.index(spect_val)]
        lamb, sourcespectrum = reading(spectdat,2)
        # lamb = spectdat[0]
        # sourcespectrum = spectdat[1]
        sourcespectrum = numpy.array(sourcespectrum)

        # Reading template of sky emission [code to be done HERE]
        skyspectrum = sourcespectrum

        # Characteristics depending on observing mode:
        # Plate scale (arcsec/pix) - ps
        # Total number of fibres in one CCD  - ntotalfibres
        # (~4700 in the case of 8 spectrographs) - ntotalfibresins
        # Only one spectrograph in this design
        # Fibre radius in arcsec - rfibre
        # The hexagonal microlense is circunscribed into the circular projection of the fiber.
        # This is equivalent to the apotheme of the hexagonal fibre.
        # The equivalent circular fibre is circunscribed in the hexagon (arcsec).

        if om_val == 'LCB':
            ps = 0.155
            ntotalfibres = 567
            ntotalfibresins = 567
            rfibre = 0.620 / 2.0
        elif om_val == 'MOS':
            ps = 0.155
            ntotalfibres = 644
            ntotalfibresins = 644
            rfibre = 0.620 / 2.0
        else:
            ps = 0.155
            ntotalfibres = 567
            ntotalfibresins = 567
            rfibre = 0.620 / 2.0

        lhex = rfibre* math.sqrt(3)
        afibre = rfibre / 2.0


        # Total transmission curves of telescope + MEGARA as intended on October, 2013
        # They include: GTC 3-mirrors + FC subsystem + spectrograph (main optics + detector QE) + grating subsystem
        # (including additional optics + coatings + SO filters + vignetting when required)
        # Configuration and transmissions as intended in the CDR level of the instrument

        if spectrograph_conf == 'HR' and vph_val == 'HR-R' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH665.dat',2)
        elif spectrograph_conf == 'HR' and vph_val == 'HR-R' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH665.dat',2)
        elif spectrograph_conf == 'HR' and vph_val == 'HR-I' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH863.dat',2)
        elif spectrograph_conf == 'HR' and vph_val == 'HR-I' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH863.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-U' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH410.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-U' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH410.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-UB' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH443.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-UB' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH443.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-B' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH481.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-B' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH481.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-G' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH521.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-G' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH521.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-V' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH567.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-V' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH567.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-VR' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH617.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-VR' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH617.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-R' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH656.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-R' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH656.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-RI' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH712.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-RI' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH712.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-I' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH777.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-I' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH777.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-Z' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH926.dat',2)
        elif spectrograph_conf == 'MR' and vph_val == 'MR-Z' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH926.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-U' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH405.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-U' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH405.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-B' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH480.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-B' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH480.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-V' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH570.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-V' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH570.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-R' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH675.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-R' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH675.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-I' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH799.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-I' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH799.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-Z' and om_val == 'LCB' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH890.dat',2)
        elif spectrograph_conf == 'LR' and vph_val == 'LR-Z' and om_val == 'MOS' :
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH890.dat',2)
        else:
            lamb, tgtcinst = reading('MEGARA_TRANSM_0.1aa/t_LCB_VPH570.dat',2)

        tgtcinst = numpy.array(tgtcinst)

        # Filter transmission for the continuum
        filtercdat = filterc_list[bandc_list.index(bandc_val)]
        lamb, tfilterc = reading(filtercdat,2)
        tfilterc = numpy.array(tfilterc)

        # Wavelength array
        lamb = numpy.array(lamb)

        # Initial and final lambda of continuum filter:
        filtercar = filterchar_list[bandc_list.index(bandc_val)]
        lc1 = filtercar[2]
        lc2 = filtercar[3]

        # Initial and final lambda of sky band (included in the VPH range):
        filtercar = filterchar_list[bandc_list.index(bandsky)]
        ls1 = filtercar[2]
        ls2 = filtercar[3]

        # Seeing at selected airmass:
        seeingx = seeing_val
        seeing_zenith = seeing_val / (airmass_val ** (3./5.)) # seeing at airmass=1.0
        areaseeing = pi * ((seeingx / 2.0) **2.)
        rseeingx = seeingx / 2.0

        # Setting line FWHM to VPH FWHM in case that the line is not resolved
        if resolvedline_val == "N":
            fwhmline_val = fwhmvph

        # Setting line FWHM to VPH FWHM in case that the line is resolved, but input line fwhm
        # is < fwhmvph
        if resolvedline_val == "Y" and fwhmline_val < fwhmvph:
            fwhmline_val = fwhmvph

        # Photon energy
        lambdaeffcm = lambdaeff * 1.e-8
        lambdacm = lamb * 1.e-8
        enph = hplanck * lightv / lambdacm
        enpheff = hplanck * lightv / lambdaeffcm

        # System efficiency
        tcondmag = tcond[skycond_list.index(skycond_val)]
        effsys = tatm * tgtcinst * tcondmag

        # Telescope collecting area (cm**2)
        stel = pi * ( (rt * 100.0)**2 )

        # Projected size of a hexagonal fibre (arcsec**2)
        areafibre = 3.0 * math.sqrt(3.0) * (rfibre**2) / 2.0

        # Projected source area in arcsec**2
        if isize_val == "A":
            realareasource = size_val
            realrsource = math.sqrt(size_val / pi)
        else:
            realareasource = pi*(radius_val**2)
            realrsource = radius_val

        # Area equivalent to a seeing disk circunscribed in the hexagonal fibre
        areaeq =  pi * (afibre **2.)

        # Setting fvega and mvega according to selected continuum filter
        vegafeatures = vegachar[bandc_list.index(bandc_val)]
        magvegac = vegafeatures[0]
        fvegac = vegafeatures[1]

        # Source continuum flux per arcsec**2 (erg/s/cm**2/AA)
        if inputcontt_val == "M":
            netflux = mag2flux(magvegac,fvegac,mag_val)
        else:
            netflux = fc_val
            mag_val = flux2mag(magvegac,fvegac,fc_val)

        # Flux per arcsec**2
        if sourcet_val == "E":
            # Dominated by seeing: if seeing dominates, the size is set by seeing.
            # flux per arcsec**2 must be provided for the seeing disk.
            # Converting flux/arcsec**2 in real source to the more disperse flux/arcsec**2 in case of seeing-dominated
            if rseeingx >= realrsource:
                fcont = netflux * realareasource / areaseeing
                flineparc = fline_val * realareasource / areaseeing
            else:
                fcont = netflux
                flineparc = fline_val
        else:
            fcont = netflux / areaseeing
            flineparc = fline_val / areaseeing

        # Source spectrum scaled to totalflux in continuum
        normc, fc = sclspect(fcont, lamb, lc1, lc2, sourcespectrum, tfilterc)
        # plot_and_save(lambdacm, fc, spect_val)
        # Sky magnitude and scaled flux. Sky flux scaled to the airmass per arcsec**2
        # We consider the brightness due to moon phase
        # fsky is assumed to be valid in the wavelength range of the selected VPH, as it is derived in the
        # most similar band to the VPH range.
        skybf = -0.000278719 * (airmass_val**3) - 0.0653841* (airmass_val**2) + 1.11979* (airmass_val) - 0.0552132
        skymag = skymag_list[bandsky_list.index(bandsky)]
        skymag = skymag + extraskyemission[moon_list.index(moon_val)]

        vegafeatures = vegachar[bandc_list.index(bandsky)]
        magvegas = vegafeatures[0]
        fvegas = vegafeatures[1]
        fsky = mag2flux(magvegas,fvegas,skymag)
        fsky = fsky * skybf

        # Filter transmission for continuum in VPH (or for sky).
        # It must be similar to the most similar band to the VPH wavelength range.
        # This is for changing continuum flux from input band to that similar to the selected VPH
        filtercvphdat = filterc_list[bandsky_list.index(bandsky)]
        lamb, tfiltercvph = reading(filtercvphdat,2)

        tfiltercvph = numpy.array(tfiltercvph)

        # Sky spectrum scaled to totalflux in input filter
        norms, fs = sclspect(fsky, lamb, ls1, ls2, skyspectrum, tfiltercvph)

        # Source projected area (arcsec**2) and projected diameter (arcsec)

        if sourcet_val == "E": # Assuming that projected source area is circular
            diamsource = 2. * realrsource
            if isize_val == "A":
                areasource = size_val
            else:
                areasource = pi*(radius_val**2)
            # if source is dominated by seeing
            if rseeingx >= realrsource:
                diamsource = seeingx
                areasource = areaseeing
        else:
            diamsource = seeingx
            areasource = areaseeing

        rsource = diamsource / 2.0

        # Number of fibres covered by the source:
        # Assuming that the fibres are completely packed and covering 100% of source area
        nfibres = areasource / areafibre

        if nfibres > ntotalfibresins:
            # ERROR
            areasource = ntotalfibresins * areafibre
            diamsource = 2. * math.sqrt (areasource / pi)
            rsource = diamsource / 2.0
            nfibres = ntotalfibresins
            outtext = outmessage(112)
            errind = warn(outtext,frame0,'MEGARA ETC Warning')
        else:
            pass

        nfibres = math.ceil (nfibres)

        # Number of fibres covered by the source in Y direction in spectra
        nfibresy = math.ceil( (2.0 * rsource) / (2. * afibre))

        # Area in which sky has been measured
        nfibresky = nsfib_val
        nfibresky = math.ceil (nfibresky)
        omegasky = nfibresky * areafibre

        # Different spatial and resolution elements to consider, depending on whether the source is punctual or extended.
        # Starting FOR loop for computations of SNR per frame
        items = range(12)
        for xit in items:

            # Deriving spectroscopic parameters for each case:
            deltalambda, omegasource, npixx, npixy, nfib, nfib1, omegaskysource = specpar(om_val, xit, disp, ps,
             nfibres, nfibresy, areafibre, rfibre,  deltab, areasource, diamsource, areaseeing, seeingx)

            # Number of pixels in detector under consideration: just counting the factor in area
            # when we consider the used sky minibundles
            npix = npixx * npixy
            npixsky = (omegasky / omegaskysource) * npix

            # Source continuum signal in defined spectral and spatial resolution element
            signalcont = signal(fc, deltalambda, lambdaeff, effsys, stel, omegasource, exptimepframe_val, enph, lamb)

            # Sky signal in defined spectral and spatial resolution element
            signalsky = signal(fs, deltalambda, lambdaeff, effsys, stel, omegaskysource, exptimepframe_val, enph, lamb)

            # Dark signal
            signaldark = dark(exptimepframe_val, dc, npix)

            # Noise due to dark measurement to the square
            noisedarksq = darknoisesq(npix, npdark_val, exptimepframe_val, dc, ron)

            # RON
            ronoise = readoutnoise(npix, ron)

            # Noise due to sky substraction
            # Sky signal *MEASURED* in defined spectral and spatial resolution element
            signalskymeasured = signal(fs, deltalambda,  lambdaeff, effsys, stel, omegasky, exptimepframe_val, enph, lamb)
            ronoiseskymeasured = readoutnoise(npixsky, ron)
            signaldarkskymeasured = dark(exptime_val, dc, npixsky)
            noisedarksqskymeasured = darknoisesq(npixsky, npdark_val, exptimepframe_val, dc, ron)

            noiseskysq = (omegaskysource / omegasky)**2 * (signalskymeasured + ronoiseskymeasured + signaldarkskymeasured + noisedarksqskymeasured)

            # Source continuum noise in defined spectral and spatial resolution element
            noisecont = math.sqrt(signalcont + signalsky + signaldark + ronoise + noisedarksq + noiseskysq)

            # Signal-to-noise of continuum
            sncont = signalcont / noisecont
            # TEST TEST TEST

            if xit == 0: # P2SP (per 2 spectral pixels), All area
                sncont_p2sp_all = sncont
                tsncont_p2sp_all = sncont * numpy.sqrt(numframe_val)
            elif xit == 1: # 1AA, All area
                sncont_1aa_all = sncont
                tsncont_1aa_all = sncont * numpy.sqrt(numframe_val)
            elif xit == 2: # Bandwidth, All area
                sncont_band_all = sncont
                tsncont_band_all = sncont * numpy.sqrt(numframe_val)
            elif xit == 3: # P2SP, seeing
                sncont_p2sp_seeing = sncont
                tsncont_p2sp_seeing = sncont * numpy.sqrt(numframe_val)
            elif xit == 4: # 1AA, seeing
                sncont_1aa_seeing = sncont
                tsncont_1aa_seeing = sncont * numpy.sqrt(numframe_val)
            elif xit == 5: # Bandwidth, seeing
                sncont_band_seeing = sncont
                tsncont_band_seeing = sncont * numpy.sqrt(numframe_val)
            elif xit == 6: # P2SP, 1 arcsec2
                sncont_p2sp_1 = sncont
                tsncont_p2sp_1 = sncont * numpy.sqrt(numframe_val)
                nfib1def = nfib1
            elif xit == 7: # 1AA, 1 arcsec2
                sncont_1aa_1 = sncont
                tsncont_1aa_1 = sncont * numpy.sqrt(numframe_val)
                print 'xit=7 :', sncont
            elif xit == 8: # Bandwidth, 1 arcsec2
                sncont_band_1 = sncont
                tsncont_band_1 = sncont * numpy.sqrt(numframe_val)
                print 'xit=8 :', sncont
            elif xit == 9: # P2SP, 1 fibre
                sncont_p2sp_fibre = sncont
                tsncont_p2sp_fibre = sncont * numpy.sqrt(numframe_val)
                print 'xit=9 :', sncont_p2sp_fibre
                # PSP (per spectral pixel), per spatial pixel
                sncont_psp_pspp = sncont / 4  #numpy.sqrt(16.)
                tsncont_psp_pspp = sncont * numpy.sqrt(numframe_val) / 4
                # PSP (per spectral pixel), all spatial pixel
                sncont_psp_asp = sncont_psp_pspp * 2
                tsncont_psp_asp = tsncont_psp_pspp * 2
            elif xit == 10: # 1AA, 1 fibre
                sncont_1aa_fibre = sncont
                tsncont_1aa_fibre = sncont * numpy.sqrt(numframe_val)
                print 'xit=10 :', sncont_1aa_fibre
            elif xit == 11: # Bandwidth, 1 fibre
                sncont_band_fibre = sncont
                tsncont_band_fibre = sncont * numpy.sqrt(numframe_val)
        # End of FOR loop for computations of SNR per frame.
        pass

        # FOR COMPUTING SNR per detector pixel at each lamb (not just lambdaeff)
        # we need to recompute the SNR as above but just for the case of SNR per detector pixel
        # and replacing in the function signal(), lambdaeff by lamb.
        # Then, for exptime per frame:
        items = [9, 0]
        for xit in items:
            # Deriving spectroscopic parameters for each case:
            deltalambda, omegasource, npixx, npixy, nfib, nfib1, omegaskysource = specpar(om_val, xit, disp, ps,
             nfibres, nfibresy, areafibre, rfibre,  deltab, areasource, diamsource, areaseeing, seeingx)

            # Number of pixels in detector under consideration: just counting the factor in area
            # when we consider the used sky minibundles
            npix = npixx * npixy
            npixsky = (omegasky / omegaskysource) * npix

            # Source continuum signal in defined spectral and spatial resolution element
            signalcont = signal(fc, deltalambda, lamb, effsys, stel, omegasource, exptimepframe_val, enph, lamb)

            # Sky signal in defined spectral and spatial resolution element
            signalsky = signal(fs, deltalambda, lamb, effsys, stel, omegaskysource, exptimepframe_val, enph, lamb)

            # Dark signal
            signaldark = dark(exptime_val, dc, npix)

            # Noise due to dark measurement to the square
            noisedarksq = darknoisesq(npix, npdark_val, exptimepframe_val, dc, ron)

            # RON
            ronoise = readoutnoise(npix, ron)

            # Noise due to sky substraction
            # Sky signal *MEASURED* in defined spectral and spatial resolution element
            signalskymeasured = signal(fs, deltalambda,  lamb, effsys, stel, omegasky, exptimepframe_val, enph, lamb)
            ronoiseskymeasured = readoutnoise(npixsky, ron)
            signaldarkskymeasured = dark(exptimepframe_val, dc, npixsky)
            noisedarksqskymeasured = darknoisesq(npixsky, npdark_val, exptimepframe_val, dc, ron)

            noiseskysq = (omegaskysource / omegasky)**2 * (signalskymeasured + ronoiseskymeasured + signaldarkskymeasured + noisedarksqskymeasured)

            if xit == 9:
                # Source continuum noise in defined spectral and spatial resolution element
                noisecont_psp_asp = []
                pframesn_psp_asp = []
                allframesn_psp_asp = []
                # pframesn_psp_asp_all = []    #SNR per frame per spectral pixel all source area
                # allframesn_psp_asp_all = []  #SNR total per spectral pixel all source area
                for idxno, valno in enumerate(signalcont):
                    noisecont_val = math.sqrt(signalcont[idxno] + signalsky[idxno] + signaldark + ronoise + noisedarksq + noiseskysq[idxno])
                    noisecont_psp_asp.append(noisecont_val)
                    # Signal-to-noise of continuum
                    # sncont_val = signalcont[idxno] / (noisecont_val*4)  #SNR per detector pixel
                    sncont_val = signalcont[idxno] / (noisecont_val*2)  #SNR per spectral pixel
                    pframesn_psp_asp.append(sncont_val)

                    tsncont_val = sncont_val * numpy.sqrt(numframe_val) #total SNR per detector pixel
                    allframesn_psp_asp.append(tsncont_val)
            elif xit == 0:
            # Source continuum noise in defined spectral and spatial resolution element
                noisecont_psp_asp_all = []
                pframesn_psp_asp_all = []    #SNR per frame per spectral pixel all source area
                allframesn_psp_asp_all = []  #SNR total per spectral pixel all source area
                for idxno, valno in enumerate(signalcont):
                    noisecont_val = math.sqrt(signalcont[idxno] + signalsky[idxno] + signaldark + ronoise + noisedarksq + noiseskysq[idxno])
                    noisecont_psp_asp_all.append(noisecont_val)
                    # Signal-to-noise of continuum
                    sncont_val = signalcont[idxno] / (noisecont_val*2)  #SNR per detector pixel
                    pframesn_psp_asp_all.append(sncont_val)

                    tsncont_val = sncont_val * numpy.sqrt(numframe_val) #total SNR per detector pixel
                    allframesn_psp_asp_all.append(tsncont_val)



        ### END COMPUTATION OF SNR_PSP_PSPP PER FRAME EXPTIME


        ###################
        # In case of line #
        ###################
        if fluxt_val == "L":

            deltalambda = fwhmline_val * nfwhmline_val
            npixx = deltalambda / disp
            deltalambdacont = fwhmline_val * cnfwhmline_val
            npixxcont = deltalambdacont / disp

            # Different spatial elements to consider, depending on whether the source is punctual or extended.
            # Starting FOR loop for computations
            items = range(4)
            for xit in items:

                # Deriving spectroscopic parameters for each case:
                omegasource, npixy, omegaskysource, nfiby, npixx = \
                    specparline(om_val, xit, areasource, diamsource, ps, disp, nfibres, areafibre, rfibre, nfibresy, areaseeing, seeingx, npixx)

                # Line signal in defined spatial resolution element: only in the line
                # Line flux is given already integrated (not per AA)--> bandwidth deltalambda = 1 AA
                signalline = linesignal(flineparc, 1.0, effsys, stel, omegasource, exptime_val, wline_val, lamb)

                # Continuum signal in defined spatial resolution element, in deltalambda.
                # (If no. of line FWHMs selected is deltalambda to derive the line signal).
                # Extract continuum at the wavelength.
                ind = numpy.where(lamb == wline_val)
                contatline= fc[ind]

                signalcont_line = linesignal(contatline, deltalambda, effsys, stel, omegasource, exptime_val, wline_val, lamb)

                # Number of pixels in detector under consideration: just counting the factor in area
                # when we consider the used sky minibundles
                npix = npixx * npixy
                npixcont = (cnfwhmline_val / nfwhmline_val) * npix

                # Signal of dark current
                signaldark_line = dark(exptime_val, dc, npix)

                # Noise due to dark measurement to the square
                noisedarksq_line = darknoisesq(npix, npdark_val, exptime_val, dc, ron)

                # RON
                ronoiseline = readoutnoise(npix, ron)

                # Noise due to continuum substraction
                # Continuum signal *MEASURED* in spatial resolution element, in cnfwhmline_val
                signalcontmeasured = linesignal(contatline, deltalambdacont, effsys, stel,
                  omegasource, exptime_val, wline_val, lamb)
                ronoisecontmeasured = readoutnoise(npixcont, ron)
                signaldarkcontmeasured = dark(exptime_val, dc, npixcont)
                noisedarksqcontmeasured = darknoisesq(npixcont, npdark_val, exptime_val, dc, ron)

                noisecontsq = (nfwhmline_val / cnfwhmline_val)**2 * (signalcontmeasured +
                  ronoisecontmeasured + signaldarkcontmeasured + noisedarksqcontmeasured)

                # Line noise in defined spectral and spatial resolution element
                noiseline = math.sqrt (signalline + signalcont_line  + signaldark_line + ronoiseline +
                  noisedarksq_line + noisecontsq)

                # Signal-to-noise of line
                snline = signalline / noiseline

                # Cases per arcsec2 and per AA and per fibre per AA
                if xit == 2 or xit == 3:
                    npixxinAA = 1.0 / disp
                    npixinAA = npixxinAA * npixy

                    # If line FWHM is > 1 A, line and continuum fluxes contributing to measurement
                    if fwhmline_val > 1.0:
                        signallineperAA = signalline / fwhmline_val
                        signalcont_lineperAA = signalcont_line / deltalambda
                    # If line FWHM is < 1 A, line and continuum fluxes contributing to measurement
                    else:
                        signallineperAA = signalline
                        signalcont_lineperAA = linesignal(contatline, 1.0, effsys, stel, omegasource,
                          exptime_val, wline_val, lamb)

                    # Common computations, independent on if FWHM > 1AA or not.
                    signaldark_lineperAA = dark(exptime_val, dc, npixinAA)
                    noisedarksq_lineperAA = darknoisesq(npixinAA, npdark_val, exptime_val, dc, ron)
                    ronoiselineperAA = readoutnoise(npixinAA, ron)

                    # Noise in continuum measurement is the same as before, but the scaling is
                    # different according to the different number of pixels in 1 AA.
                    noisecontmeasuredperAA = (( (1./fwhmline_val) / nfwhmline_val)**2) * noisecontsq

                    # Total noise in line
                    noiselineperAA = math.sqrt (signallineperAA + signalcont_lineperAA +
                      signaldark_lineperAA + ronoiselineperAA + noisedarksq_lineperAA +
                      noisecontmeasuredperAA)

                    if xit == 2:
                        snlineperAA = signallineperAA / noiselineperAA
                    if xit == 3:
                        snlinefibreperAA = signallineperAA / noiselineperAA     ### SAME AS snlineperAA ???

                # 1 spaxel, (1 fibre diameter * 4 pix in spectral direction)
                if xit == 3:

                    # VPH FWHM is always <= line FWHM (it is imposed)
                    npixfibre = (fwhmvph /disp) * (2.* rfibre/ps)
                    npixxspaxel = 4.0 # Nyquist-Shannon sampling theorem
                    npixspaxel = npixxspaxel * npixy
                    ratio = npixfibre / (npixspaxel)
                    signallinespaxel = signalline / ratio
                    signalcont_linespaxel = signalcont_line / ratio

                    signaldark_linespaxel = dark(exptime_val, dc, npixspaxel)
                    noisedarksq_linespaxel = darknoisesq(npixspaxel, npdark_val, exptime_val, dc, ron)
                    ronoiselinespaxel = readoutnoise(npixspaxel, ron)

                    # Noise in continuum measurement is the same as before, but the scaling is
                    # different according to the different number of pixels in 4 pixels.
                    noisecontmeasuredperspaxel = (((fwhmvph/fwhmline_val) / nfwhmline_val)**2) * noisecontsq

                    noiselinespaxel = math.sqrt (signallinespaxel + signalcont_linespaxel +
                     signaldark_linespaxel + ronoiselinespaxel + noisedarksq_linespaxel +
                     noisecontmeasuredperspaxel)

                    snlinespaxel = signallinespaxel / noiselinespaxel

                # 1 spectral and spatial pixel
                if xit == 3:
                    npixfibre = (fwhmline_val/disp) * (2.* rfibre/ps)
                    npixx1pix = 1.0
                    npixy1pix = 1.0
                    npix1pix = npixx1pix * npixy1pix
                    ratio = npixfibre / (npix1pix)
                    signalline1pix = signalline / ratio
                    signalcont_line1pix = signalcont_line / ratio

                    signaldark_line1pix = dark(exptime_val, dc, npix1pix)
                    noisedarksq_line1pix = darknoisesq(npix1pix, npdark_val, exptime_val, dc, ron)
                    ronoiseline1pix = readoutnoise(npix1pix, ron)

                    # Noise in continuum measurement is the same as before, but the scaling is
                    # different according to the different number of pixels 1 pix.
                    noisecontmeasuredperspaxel = ((( (fwhmvph/fwhmline_val)/4.0 ) /
                        nfwhmline_val)**2) * noisecontsq

                    noiseline1pix = math.sqrt (signalline1pix + signalcont_line1pix +
                        signaldark_line1pix + ronoiseline1pix + noisedarksq_line1pix +
                        noisecontmeasuredperspaxel)

                    snline1pix = signalline1pix / noiseline1pix
                    # snline1pix = snlinespaxel / math.sqrt(16)

                # Output values:

                if xit == 0: # All area
                    snline_all = snline
                    tsnline_all = snline_all * numpy.sqrt(numframe_val)

                elif xit == 1: # Seeing
                    snline_seeing = snline
                    tsnline_seeing = snline_seeing * numpy.sqrt(numframe_val)

                elif xit == 2: # 1 arcsec**2
                    snline_1 = snline
                    tsnline_1 = snline_1 * numpy.sqrt(numframe_val)
                    snline_1_aa = snlineperAA
                    tsnline_1_aa = snline_1_aa * numpy.sqrt(numframe_val)

                elif xit == 3: # 1 fibre
                    snline_fibre = snline
                    tsnline_fibre = snline_fibre * numpy.sqrt(numframe_val) # all frames
                    snline_fibre1aa = snlinefibreperAA
                    tsnline_fibre1aa = snline_fibre1aa * numpy.sqrt(numframe_val) # all frames
                    snline_spaxel = snlinespaxel
                    tsnline_spaxel = snline_spaxel * numpy.sqrt(numframe_val) # all frames
                    snline_pspp = snline1pix
                    tsnline_pspp = snline_pspp * numpy.sqrt(numframe_val) #total SNR per detector pixel

            # End of FOR loop for computations
            pass

        # Ending if line
        else:
            snline_all = 0.
            tsnline_all = 0.
            snline_seeing = 0.
            tsnline_seeing = 0.
            snline_1 = 0.
            tsnline_1 = 0.
            snline_1_aa = 0.
            tsnline_1_aa = 0.
            snline_fibre = 0.
            tsnline_fibre = 0.
            snline_pspp = 0.
            tsnline_pspp = 0.
            snline_spaxel = 0.
            tsnline_spaxel = 0.
            snline_fibre1aa = 0.
            tsnline_fibre1aa = 0.

        ##############################
        # Output of input parameters #
        ##############################
        textigui,texti = outtextinp(om_val, bandc_val, sourcet_val, mag_val,\
                                    netflux, isize_val, realareasource, realrsource,\
                                    seeingx, pi, fluxt_val, wline_val,\
                                    fline_val, fwhmline_val, vph_val,\
                                    skycond_val, moon_val, airmass_val,\
                                    seeing_zenith,fsky, numframe_val,\
                                    exptimepframe_val, exptime_val,\
                                    npdark_val, nsbundles_val, nsfib_val,\
                                    nfwhmline_val, cnfwhmline_val,\
                                    resolvedline_val, bandsky)

        #######################################
        # Output of continuum signal-to-noise #
        #######################################
        textocgui,textoc = outtextoutc(sourcet_val, nfibres, nfib, nfib1def,\
                                       sncont_p2sp_all, tsncont_p2sp_all,\
                                       sncont_1aa_all, tsncont_1aa_all,\
                                       sncont_band_all, tsncont_band_all,\
                                       sncont_p2sp_fibre, tsncont_p2sp_fibre,\
                                       sncont_1aa_fibre, tsncont_1aa_fibre,\
                                       sncont_band_fibre, tsncont_band_fibre,\
                                       sncont_p2sp_seeing, tsncont_p2sp_seeing,\
                                       sncont_1aa_seeing, tsncont_1aa_seeing,\
                                       sncont_band_seeing, tsncont_band_seeing,\
                                       sncont_p2sp_1, tsncont_p2sp_1,\
                                       sncont_1aa_1, tsncont_1aa_1,\
                                       sncont_band_1, tsncont_band_1,\
                                       sncont_psp_pspp,tsncont_psp_pspp,\
                                       lambdaeff)

        ############################################
        # Output of line+continuum signal-to-noise #
        ############################################
        textolgui, textol = outtextoutl(fluxt_val,\
                                       snline_all, snline_fibre,\
                                       snline_pspp, snline_1_aa,\
                                       sourcet_val,\
                                       snline_seeing, snline_1,\
                                       snline_spaxel, snline_fibre1aa)


        if errind==0:       # ADDED FOR DJANGO
            # outtext="No Warnings."     # ADDED FOR DJANGO
            outtext = ""

        # FOR DJANGO: This is for saving the output of calc() in the static folder.
        outputfilename = "etc/static/etc/outputcalc.txt"
        with open(outputfilename, 'w') as f:
            print >> f, outtext
            print >> f, texti
            print >> f, textoc
            print >> f, textol

        # FOR DJANGO: Finally, return these outputs.
        # Order: input values, Output Cont., Output Line.
        #
        return {'outtext' : outtext, 'texti' : texti,\
                'textoc' : textoc, 'textol' : textol,\
                'om_val' : om_val, 'bandc_val' : bandc_val,\
                'sourcet_val' : sourcet_val,\
                'mag_val' : mag_val, 'netflux' : netflux,\
                'isize_val': isize_val,\
                'size_val' : areasource, 'radius_val' : rsource,\
                'seeingx' : seeingx, 'pi': pi, 'fluxt_val' : fluxt_val,\
                'wline_val' : wline_val, 'fline_val' : fline_val, 'fwhmline_val' : fwhmline_val,\
                'vph_val' : vph_val, 'skycond_val' : skycond_val, 'moon_val' : moon_val,\
                'airmass_val' : airmass_val, 'seeing_zenith' : seeing_zenith,\
                'fsky' : fsky, 'numframe_val' : numframe_val,\
                'exptimepframe_val' : exptimepframe_val, 'exptime_val' : exptime_val,\
                'npdark_val' : npdark_val, 'nsbundles_val' : nsbundles_val, 'nsfib_val' : nsfib_val,\
                'nfwhmline_val' : nfwhmline_val, 'cnfwhmline_val' : cnfwhmline_val,\
                'resolvedline_val' : resolvedline_val, 'bandsky' : bandsky,\

                'sourcespectrum' : sourcespectrum, 'lamb' : lamb,\
                'spect_val' : spect_val,\
                'fc' : fc,\
                'pframesn_psp_asp' : pframesn_psp_asp,\
                'allframesn_psp_asp' : allframesn_psp_asp,\
                'pframesn_psp_asp_all' : pframesn_psp_asp_all,\
                'allframesn_psp_asp_all' : allframesn_psp_asp_all,\

                'nfibres' : nfibres, 'nfib' : nfib, 'nfib1def' : nfib1def,\
                'sncont_p2sp_all' : sncont_p2sp_all, 'tsncont_p2sp_all' : tsncont_p2sp_all,\
                'sncont_1aa_all' : sncont_1aa_all, 'tsncont_1aa_all' : tsncont_1aa_all,\
                'sncont_band_all' : sncont_band_all, 'tsncont_band_all' : tsncont_band_all,\
                'sncont_p2sp_fibre' : sncont_p2sp_fibre, 'tsncont_p2sp_fibre' : tsncont_p2sp_fibre,\
                'sncont_1aa_fibre' : sncont_1aa_fibre, 'tsncont_1aa_fibre' : tsncont_1aa_fibre,\
                'sncont_band_fibre' : sncont_band_fibre, 'tsncont_band_fibre' : tsncont_band_fibre,\
                'sncont_p2sp_seeing' : sncont_p2sp_seeing, 'tsncont_p2sp_seeing' : tsncont_p2sp_seeing,\
                'sncont_1aa_seeing' : sncont_1aa_seeing, 'tsncont_1aa_seeing' : tsncont_1aa_seeing,\
                'sncont_band_seeing' : sncont_band_seeing, 'tsncont_band_seeing' : tsncont_band_seeing,\
                'sncont_p2sp_1' : sncont_p2sp_1, 'tsncont_p2sp_1' : tsncont_p2sp_1,\
                'sncont_1aa_1' : sncont_1aa_1, 'tsncont_1aa_1' : tsncont_1aa_1,\
                'sncont_band_1' : sncont_band_1, 'tsncont_band_1' : tsncont_band_1,\
                'sncont_psp_pspp' : sncont_psp_pspp, 'tsncont_psp_pspp' : tsncont_psp_pspp,\
                'lambdaeff' : lambdaeff,\

                'snline_all' : snline_all, 'tsnline_all' : tsnline_all,\
                'snline_fibre' : snline_fibre, 'tsnline_fibre' : tsnline_fibre,\
                'snline_pspp' : snline_pspp, 'tsnline_pspp' : tsnline_pspp,\
                'snline_1_aa' : snline_1_aa, 'tsnline_1_aa' : tsnline_1_aa,\
                'snline_seeing' : snline_seeing, 'tsnline_seeing' : tsnline_seeing,\
                'snline_1' : snline_1, 'tsnline_1' : tsnline_1,\
                'snline_spaxel' : snline_spaxel, 'tsnline_spaxel' : tsnline_spaxel,\
                'snline_fibre1aa': snline_fibre1aa, 'tsnline_fibre1aa' : tsnline_fibre1aa
                }     # ADDED FOR DJANGO
    # Avoiding computations in case of exception of errind
    else:
        spectdat = specttmplt_list[spect_list.index(spect_val)]
        lamb, sourcespectrum = reading(spectdat,2)

        texti = " "       # ADDED FOR DJANGO
        textoc = " "      # ADDED FOR DJANGO
        textol = " "      # ADDED FOR DJANGO
        outtext = "** MEGARA ETC HELP "+outtext       # ADDED FOR DJANGO
        # return "\n** MEGARA ETC HELP **\n",outtext        # COMMENTED OUT FOR DJANGO
        return {'outtext' : outtext, 'texti' : texti, 'textoc' : textoc, 'textol' : textol,\
                'sourcespectrum' : sourcespectrum, 'lamb' : lamb}     # ADDED FOR DJANGO
        pass