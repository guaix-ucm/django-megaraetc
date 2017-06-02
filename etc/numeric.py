#
# Copyright 2010-2016 Universidad Complutense de Madrid (Spain)
#
# This file is part of Megara Exposure Time Calculator
#
# Megara ETC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Megara ETC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Megara ETC. If not, see <http://www.gnu.org/licenses/>.
#

import math
import numpy
import matplotlib.mlab as mlab

### ADDED FOR TESTING DJANGO WEB FRAMEWORK ###
def thisisatest(somevalue):
    output=somevalue*3
    outstring="The test worked, this is the output in numeric.py<br>"+str(output)
    return outstring

###
def mag2flux(magvega,fvega,inputmag):
    '''Convert magnitude in Vega system to flux in erg/s/cm**2/AA'''
    return fvega * ( 10.0 ** ((inputmag-magvega) / (-2.5)) )

def flux2mag(magvega,fvega,inputf):
    '''Convert flux in erg/s/cm**2/AA to magnitude in Vega system'''
    return -2.5 * math.log10(inputf/fvega) + magvega

# ********************************
# Function to derive spectroscopic parameters according to the case selected for continuum output.
# Args: 
# om_val = Observing mode, MOS or LCB
# xit = index of loop
# disp = VPH dispersion
# ps = plate-scale
# nfibres = number of fibers to cover source;
# nfibresy = number of fibers to cover source; in y-direction (i.e. spatial) in CCD spectral plane
# areafibre = area of fiber
# rfibre = radius of fiber
# deltab = VPH delta_b
# areasource = area of source
# diamsource = diameter of source
# areaseeing = area of seeing
# seeingx = seeing at X

def specpar(om_val, xit, disp, ps, nfibres, nfibresy, areafibre, rfibre,  deltab, areasource, 
            diamsource, areaseeing, seeingx):
    verbose = ""    # reset at the beginning of each loop
  # FWHM does not depend on Observing mode: is fixed to 4 pixels by design

    fwhmvph_om = 4.0    # Should we change this to 3.6?
    verbose += "Note: FWHM of VPH does not depend on Observing mode: is fixed to 4 pixels. <br /><br />"

    if xit == 0: # P2SP (per 2 spectral pixels), All area
        deltalambda = fwhmvph_om * disp
        omegasource = areasource
        npixx = fwhmvph_om    
        npixy = nfibresy * (2.0 * rfibre) / ps    
        omegaskysource = nfibres * areafibre
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        verbose += "<b>### XIT = 0 <br />"
        verbose += "### per 2 spectral pixels, All area </b><br />"
        # verbose += "$\Delta\lambda = FWHM(VPH) \\times disp = %s \\times %s = %s$ <br />" % (fwhmvph_om, disp, deltalambda)
        # verbose += "$\Omega_{source} = \\textrm{Area of source} = %s $ <br />" % omegasource
        # verbose += "$n_{pix,x} = FWHM(VPH) = %s$ <br />" % npixx
        # verbose += "$n_{pix,y} = N_{fibers,y} \\times \\frac{(2 \\times R_{fiber})}{ps} = %s \\times \\frac{(2 \\times %s)}{%s} = %s $ <br />" % (nfibresy, rfibre, ps, npixy)
        # verbose += "$\Omega_{sky,source} = N_{fibers} \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfibres, areafibre, omegaskysource)
        # verbose += "nfib = %s <br />" % nfib
        # verbose += "nfib1 = %s <br />" % nfib1
    elif xit == 1: # 1AA, All area    
        deltalambda = 1.0    
        omegasource = areasource    
        npixx = 1.0 / disp    
        npixy = nfibresy * (2.0 * rfibre) / ps    
        omegaskysource = nfibres * areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        verbose += "<b>### XIT = 1 <br />"
        verbose += "### per AA, All area </b><br />"
        verbose += "$\Delta\lambda = %s$ <br />" % (deltalambda)
        verbose += "$\Omega_{source} = \\textrm{Area of source} = %s $ <br />" % omegasource
        verbose += "$n_{pix,x} = \\frac{1}{disp} = \\frac{1}{%s} = %s $ <br />" % (disp,npixx)
        verbose += "$n_{pix,y} = N_{fibers,y} \\times \\frac{(2 \\times R_{fiber})}{ps} = %s \\times \\frac{(2 \\times %s)}{%s} = %s $ <br />" % (nfibresy, rfibre, ps, npixy)
        verbose += "$\Omega_{sky,source} = N_{fibers} \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfibres, areafibre, omegaskysource)
        verbose += "nfib = %s <br />" % nfib
        verbose += "nfib1 = %s <br />" % nfib1

    elif xit == 2: # Bandwidth, All area    
        deltalambda = deltab    
        omegasource = areasource    
        npixx = deltab / disp    
        npixy = nfibresy * (2.0 * rfibre) / ps    
        omegaskysource = nfibres * areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        verbose += "<b>### XIT = 2 <br />"
        verbose += "### per bandwidth, All area </b><br />"
        # verbose += "$\Delta\lambda = %s$ <br />" % (deltalambda)
        # verbose += "$\Omega_{source} = \\textrm{Area of source} = %s $ <br />" % omegasource
        # verbose += "$n_{pix,x} = \\frac{deltab}{disp} = \\frac{deltab}{%s} = %s $ <br />" % (disp,npixx)
        # verbose += "$n_{pix,y} = N_{fibers,y} \\times \\frac{(2 \\times R_{fiber})}{ps} = %s \\times \\frac{(2 \\times %s)}{%s} = %s $ <br />" % (nfibresy, rfibre, ps, npixy)
        # verbose += "$\Omega_{sky,source} = N_{fibers} \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfibres, areafibre, omegaskysource)
        # verbose += "nfib = %s <br />" % nfib
        # verbose += "nfib1 = %s <br />" % nfib1

    elif xit == 3: # P2SP, seeing    
        deltalambda = fwhmvph_om * disp    
        omegasource = areaseeing    
        verbose += "<b>### XIT = 3 <br />"
        verbose += "### per 2 spectral pixels, seeing area </b><br />"
        verbose += "$\Delta\lambda = FWHM(VPH) \\times disp = %s \\times %s = %s$ <br />" % (fwhmvph_om, disp, deltalambda)
        verbose += "$\Omega_{source} = A_{seeing} = %s $ <br />" % omegasource
        if (seeingx / 2.) <= rfibre:
            omegaskysource = areafibre
            nfiby = 1.0
            nfib = 1.0
            verbose += "since $\\frac{seeingx}{2} (= \\frac{%s}{2}) \leq R_{fiber} (= %s) $ <br />" % (seeingx, rfibre)
            verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
            verbose += "nfiby = 1.0 <br />"
            verbose += "nfib = 1.0 <br />"
        else:
            nfib = math.ceil (omegasource / areafibre)
            omegaskysource = nfib * areafibre
            nfiby = math.sqrt(nfib)
            verbose += "since $\\frac{seeingx}{2} (= \\frac{%s}{2}) > R_{fiber} (= %s) $ <br />" % (seeingx, rfibre)
            verbose += "nfib = $\\frac{\Omega_{source}}{A_{fiber}} = \\frac{%s}{%s} = %s $ <br />" % (omegasource, areafibre, nfib)
            verbose += "$\Omega_{sky,source} = nfib \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfib, areafibre, omegaskysource)
            verbose += "nfiby = $\sqrt{nfib} = \sqrt{%s} = %s $ <br />" % (nfib, nfiby)
    
        npixx = fwhmvph_om    
        npixy = nfiby * 2.0 * rfibre / ps
        nfib1 = 0. # Default value
        verbose += "FWHM(VPH) = %s <br />" % fwhmvph_om
        verbose += "$N_{pix,y} = nfiby \\times 2 \\times \\frac{R_{fiber}}{ps} = %s \\times 2 \\times \\frac{%s}{%s} = %s $ <br />" % (nfiby, rfibre, ps, npixy)
        verbose += "nfib1 = 0 <br />"
    
    elif xit == 4: # 1AA, seeing    
        deltalambda = 1.0
        omegasource = areaseeing
        verbose += "<b>### XIT = 4 <br />"
        verbose += "### per AA, per seeing </b><br />"
        # verbose += "$\Delta\lambda = 1.0 $ <br />"
        # verbose += "$\Omega_{source} = A_{seeing} = %s $ <br />" % omegasource
        if (seeingx / 2.) <= rfibre:
            omegaskysource = areafibre
            nfiby = 1.0
            nfib = 1.0
            # verbose += "since $\\frac{seeingx}{2} (= \\frac{%s}{2}) \leq R_{fiber} (= %s) $ <br />" % (seeingx, rfibre)
            # verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
            # verbose += "nfiby = 1.0 <br />"
            # verbose += "nfib = 1.0 <br />"
        else:
            nfib = math.ceil (omegasource / areafibre)
            omegaskysource = nfib * areafibre
            nfiby = math.sqrt(nfib)
            # verbose += "since $\\frac{seeingx}{2} (= \\frac{%s}{2}) > R_{fiber} (= %s) $ <br />" % (seeingx, rfibre)
            # verbose += "nfib = $\\frac{\Omega_{source}}{A_{fiber}} = \\frac{%s}{%s} = %s $ <br />" % (omegasource, areafibre, nfib)
            # verbose += "$\Omega_{sky,source} = nfib \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfib, areafibre, omegaskysource)
            # verbose += "nfiby = $\sqrt{nfib} = \sqrt{%s} = %s $ <br />" % (nfib, nfiby)
        npixx = 1.0 / disp    
        npixy = nfiby * 2.0 * rfibre / ps            
        nfib1 = 0. # Default value
        # verbose += "$n_{pix,x} = \\frac{1}{disp} = \\frac{1}{%s} = %s $ <br />" % (disp,npixx)
        # verbose += "$n_{pix,y} = nfiby \\times \\frac{(2 \\times R_{fiber})}{ps} = %s \\times \\frac{(2 \\times %s)}{%s} = %s $ <br />" % (nfiby, rfibre, ps, npixy)
        # verbose += "nfib1 = 0 <br />"

    elif xit == 5: # Bandwidth, seeing
        deltalambda = deltab    
        omegasource = areaseeing
        verbose += "<b>### XIT = 5 <br />"
        verbose += "### per bandwidth, per seeing </b><br />"
        # verbose += "$\Delta\lambda = deltab = %s $ <br />" % deltab
        # verbose += "$\Omega_{source} = A_{seeing} = %s $ <br />" % omegasource
        if (seeingx / 2.) <= rfibre:
            omegaskysource = areafibre
            nfiby = 1.0
            nfib = 1.0
            # verbose += "since $\\frac{seeingx}{2} (= \\frac{%s}{2}) \leq R_{fiber} (= %s) $ <br />" % (seeingx, rfibre)
            # verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
            # verbose += "nfiby = 1.0 <br />"
            # verbose += "nfib = 1.0 <br />"
        else:
            nfib = math.ceil (omegasource / areafibre)
            omegaskysource = nfib * areafibre
            nfiby = math.sqrt(nfib) 
            # verbose += "since $\\frac{seeingx}{2} (= \\frac{%s}{2}) > R_{fiber} (= %s) $ <br />" % (seeingx, rfibre)
            # verbose += "nfib = $\\frac{\Omega_{source}}{A_{fiber}} = \\frac{%s}{%s} = %s $ <br />" % (omegasource, areafibre, nfib)
            # verbose += "$\Omega_{sky,source} = nfib \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfib, areafibre, omegaskysource)
            # verbose += "nfiby = $\sqrt{nfib} = \sqrt{%s} = %s $ <br />" % (nfib, nfiby)

        npixx = deltab / disp     
        npixy = nfiby * 2.0 * rfibre / ps
        nfib1 = 0. # Default value
        # verbose += "$n_{pix,x} = \\frac{deltab}{disp} = \\frac{%s}{%s} = %s $ <br />" % (deltab, disp, npixx)
        # verbose += "$n_{pix,y} = nfiby \\times \\frac{(2 \\times R_{fiber})}{ps} = %s \\times \\frac{(2 \\times %s)}{%s} = %s $ <br />" % (nfiby, rfibre, ps, npixy)
        # verbose += "nfib1 = 0 <br />"
    
    elif xit == 6: # P2SP, 1 arcsec2    
        deltalambda = fwhmvph_om * disp
        verbose += "<b>### XIT = 6 <br />"
        verbose += "### per 2 spectral pixels, per $\\textrm{arcsec}^{2}$ </b><br />"
        # verbose += "$\Delta\lambda = FWHM(VPH) \\times disp = %s \\times %s = %s $ <br />" % (fwhmvph_om, disp, deltalambda)
        if areasource >= 1.0:
            omegasource = 1.0
            # verbose += "$\Omega_{source} = 1$ because $A_{source} \geq 1 $ <br />"
        else:    
            omegasource = areasource
            # verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < 1 $ <br />" % omegasource
        
        nfib1 = math.ceil (1.0 / areafibre)
        omegaskysource = nfib1 * areafibre    
        nfiby = math.sqrt(nfib1) 
        npixx = fwhmvph_om    
        npixy = nfiby * 2.0 * rfibre / ps
        nfib = 0. # Default value        
        # verbose += "nfib1 = ceil(1/$A_{fiber}$) = ceil(1/%s) = %s <br />" % (areafibre, nfib1)
        # verbose += "$\Omega_{sky,source} = nfib1 \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfib1, areafibre, omegaskysource)
        # verbose += "nfiby = $\sqrt{nfbi1} = \sqrt{%s} = %s $ <br />" % (nfib1, nfiby)
        # verbose += "$n_{pix,x} = FWHM(VPH) = %s $ <br />" % npixx
        # verbose += "$n_{pix, y} = nfiby \\times \\frac{(2 \\times R_{fiber})}{ps} = %s \\times \\frac{(2 \\times %s)}{%s} = %s $ <br />" % (nfiby, rfibre, ps, npixy)

    elif xit == 7: # 1AA, 1 arcsec2
        deltalambda = 1.0
        verbose += "<b>### XIT = 7 <br />"
        verbose += "### per AA, per $\\textrm{arcsec}^{2}$ </b><br />"
        # verbose += "$\Delta\lambda = 1 $<br />"
        if areasource >= 1.0:
            omegasource = 1.0
            # verbose += "$\Omega_{source} = 1$ because $A_{source} \geq 1 $ <br />"
        else:    
            omegasource = areasource
            # verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < 1 $ <br />" % omegasource
        
        nfib1 = math.ceil (1.0 / areafibre)
        omegaskysource = nfib1 * areafibre    
        nfiby = math.sqrt(nfib1)     
        npixx = 1.0 / disp    
        npixy = nfiby * 2.0 * rfibre / ps    
        nfib = 0. # Default value
        # verbose += "nfib1 = ceil(1/$A_{fiber}$) = ceil(1/%s) = %s <br />" % (areafibre, nfib1)
        # verbose += "$\Omega_{sky,source} = nfib1 \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfib1, areafibre, omegaskysource)
        # verbose += "nfiby = $\sqrt{nfbi1} = \sqrt{%s} = %s $ <br />" % (nfib1, nfiby)
        # verbose += "$n_{pix,x} = \\frac{1}{disp} = \\frac{1}{%s} = %s $ <br />" % (disp, npixx)
        # verbose += "$n_{pix, y} = nfiby \\times \\frac{(2 \\times R_{fiber})}{ps} = %s \\times \\frac{(2 \\times %s)}{%s} = %s $ <br />" % (nfiby, rfibre, ps, npixy)
        # verbose += "nfib = 0 <br />"
    
    elif xit == 8: # Bandwidth, 1 arcsec2    
        deltalambda = deltab
        verbose += "<b>### XIT = 8 <br />"
        verbose += "### per bandwidth, per $\\textrm{arcsec}^{2}$ </b><br />"
        # verbose += "$\Delta\lambda = deltab = %s $ <br />" % deltab
        if areasource >= 1.0:
            omegasource = 1.0
            # verbose += "$\Omega_{source} = 1$ because $A_{source} \geq 1 $ <br />"
        else:    
            omegasource = areasource
            # verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < 1 $ <br />" % omegasource

        nfib1 = math.ceil (1.0 / areafibre)
        omegaskysource = nfib1 * areafibre    
        nfiby = math.sqrt(nfib1) 
        npixx = deltab / disp    
        npixy = nfiby * 2.0 * rfibre / ps    
        nfib = 0. # Default value
        # verbose += "nfib1 = ceil(1/$A_{fiber}$) = ceil(1/%s) = %s <br />" % (areafibre, nfib1)
        # verbose += "$\Omega_{sky,source} = nfib1 \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfib1, areafibre, omegaskysource)
        # verbose += "nfiby = $\sqrt{nfbi1} = \sqrt{%s} = %s $ <br />" % (nfib1, nfiby)
        # verbose += "$n_{pix,x} = \\frac{deltab}{disp} = \\frac{%s}{%s} = %s $ <br />" % (deltab, disp, npixx)
        # verbose += "$n_{pix, y} = nfiby \\times \\frac{(2 \\times R_{fiber})}{ps} = %s \\times \\frac{(2 \\times %s)}{%s} = %s $ <br />" % (nfiby, rfibre, ps, npixy)
        # verbose += "nfib = 0 <br />"

    
    elif xit == 9: # P2SP, 1 fibre    
        deltalambda = fwhmvph_om * disp
        verbose += "<b>### XIT = 9 <br />"
        verbose += "### per 2 spectral pixels, per fiber </b><br />"
        # verbose += "$\Delta\lambda = FWHM(VPH) \\times disp = %s \\times %s = %s $ <br />" % (fwhmvph_om, disp, deltalambda)
        if areasource >= areafibre:    
            omegasource = areafibre
            # verbose += "$\Omega_{source} = A_{fiber} = %s $ because $A_{source} \geq A_{fiber} $ <br />" % omegasource
        else:    
            omegasource = areasource    
            # verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < A_{fiber} $ <br />" % omegasource
        npixx = fwhmvph_om    
        npixy = 2. * rfibre / ps    
        omegaskysource = areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        # verbose += "$n_{pix,x} = FWHM(VPH) = %s $ <br />" % npixx
        # verbose += "$n_{pix,y} = \\frac{2 \\times R_{fiber}}{ps} = \\frac{2 \\times %s}{%s} = %s $ <br />" % (rfibre, ps, npixy)
        # verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
        # verbose += "nfib = 0 <br />"
        # verbose += "nfib1 = 0 <br />"
    
    elif xit == 10: # 1AA, 1 fibre    
        deltalambda = 1.0
        verbose += "<b>### XIT = 10 <br />"
        verbose += "### per AA, per fiber </b><br />"
        # verbose += "$\Delta\lambda = 1 $ <br />"

        if areasource >= areafibre:    
            omegasource = areafibre
            # verbose += "$\Omega_{source} = A_{fiber} = %s $ because $A_{source} \geq A_{fiber} $ <br />" % omegasource
        else:    
            omegasource = areasource
            # verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < A_{fiber} $ <br />" % omegasource
        npixx = 1.0 / disp    
        npixy = 2. * rfibre / ps    
        omegaskysource = areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        # verbose += "$n_{pix,x} = 1/disp = 1/%s = %s $ <br />" % (disp, npixx)
        # verbose += "$n_{pix,y} = \\frac{2 \\times R_{fiber}}{ps} = \\frac{2 \\times %s}{%s} = %s $ <br />" % (rfibre, ps, npixy)
        # verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
        # verbose += "nfib = 0 <br />"
        # verbose += "nfib1 = 0 <br />"
    
    elif xit == 11: # Bandwidth, 1 fibre    
        deltalambda = deltab
        verbose += "<b>### XIT = 11 <br />"
        verbose += "### per bandwidth, per fiber </b><br />"
        # verbose += "$\Delta\lambda = deltab = %s $ <br />" % deltalambda

        if areasource >= areafibre:    
            omegasource = areafibre
            # verbose += "$\Omega_{source} = A_{fiber} = %s $ because $A_{source} \geq A_{fiber} $ <br />" % omegasource
        else:    
            omegasource = areasource
            # verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < A_{fiber} $ <br />" % omegasource
        npixx = deltab / disp  # lambda range of vph (in angstroms) / (angstrom per pixel)
        npixy = 2. * rfibre / ps    
        omegaskysource = areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        # verbose += "$n_{pix,x} = deltab/disp = %s/%s = %s $ <br />" % (deltab, disp, npixx)
        # verbose += "$n_{pix,y} = \\frac{2 \\times R_{fiber}}{ps} = \\frac{2 \\times %s}{%s} = %s $ <br />" % (rfibre, ps, npixy)
        # verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
        # verbose += "nfib = 0 <br />"
        # verbose += "nfib1 = 0 <br />"

    elif xit==12:   # for C, R1, R2 spaxels SNR per voxel (adapted from xit=9)
        deltalambda = fwhmvph_om * disp
        verbose += "<b>### XIT = 12 <br />"
        verbose += "### for C, R1, R2 spaxels per voxel </b><br />"
        verbose += "$\Delta\lambda = FWHM(VPH) \\times disp = %s \\times %s = %s $ <br />" % (fwhmvph_om, disp, deltalambda)
        if areasource >= areafibre:
            omegasource = areafibre
            verbose += "$\Omega_{source} = A_{fiber} = %s $ because $A_{source} \geq A_{fiber} $ <br />" % omegasource
        else:
            omegasource = areasource
            verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < A_{fiber} $ <br />" % omegasource
        npixx = fwhmvph_om
        npixy = 2. * rfibre / ps
        omegaskysource = areafibre
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        verbose += "$n_{pix,x} = FWHM(VPH) = %s $ <br />" % npixx
        verbose += "$n_{pix,y} = \\frac{2 \\times R_{fiber}}{ps} = \\frac{2 \\times %s}{%s} = %s $ <br />" % (rfibre, ps, npixy)
        verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
        verbose += "nfib = 0 <br />"
        verbose += "nfib1 = 0 <br />"

    elif xit == 13: # for C, R1, R2, for 1AA; adapted from xit=10
        deltalambda = 1.0
        # verbose += "<b>### XIT = 13 <br />"
        # verbose += "### per AA, per fiber </b><br />"
        # verbose += "$\Delta\lambda = 1 $ <br />"

        if areasource >= areafibre:
            omegasource = areafibre
            # verbose += "$\Omega_{source} = A_{fiber} = %s $ because $A_{source} \geq A_{fiber} $ <br />" % omegasource
        else:
            omegasource = areasource
            # verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < A_{fiber} $ <br />" % omegasource
        npixx = 1.0 / disp
        npixy = 2. * rfibre / ps
        omegaskysource = areafibre
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        # verbose += "$n_{pix,x} = 1/disp = 1/%s = %s $ <br />" % (disp, npixx)
        # verbose += "$n_{pix,y} = \\frac{2 \\times R_{fiber}}{ps} = \\frac{2 \\times %s}{%s} = %s $ <br />" % (rfibre, ps, npixy)
        # verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
        # verbose += "nfib = 0 <br />"
        # verbose += "nfib1 = 0 <br />"


    elif xit == 14: # for C, R1, R2 spaxels SNR of integrated spectrum (i.e. Total);
        deltalambda = deltab
        verbose += "<b>### XIT = 14 <br />"
        verbose += "### per bandwidth, per fiber </b><br />"
        verbose += "$\Delta\lambda = deltab = %s $ <br />" % deltalambda

        if areasource >= areafibre:
            omegasource = areafibre
            verbose += "$\Omega_{source} = A_{fiber} = %s $ because $A_{source} \geq A_{fiber} $ <br />" % omegasource
        else:
            omegasource = areasource
            verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < A_{fiber} $ <br />" % omegasource
        npixx = deltab / disp  # lambda range of vph (in angstroms) / (angstrom per pixel)
        npixy = 2. * rfibre / ps
        omegaskysource = areafibre
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        verbose += "$n_{pix,x} = deltab/disp = %s/%s = %s $ <br />" % (deltab, disp, npixx)
        verbose += "$n_{pix,y} = \\frac{2 \\times R_{fiber}}{ps} = \\frac{2 \\times %s}{%s} = %s $ <br />" % (rfibre, ps, npixy)
        verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
        verbose += "nfib = 0 <br />"
        verbose += "nfib1 = 0 <br />"

    elif xit == 15: # pdp_fiber: per detector pixel per fiber
        deltalambda = disp  # because we're only using 1pixx
        verbose += "<b>### XIT = 15 <br />"
        verbose += "### per detector pixel, per fiber </b><br />"
        # verbose += "$\Delta\lambda = FWHM(VPH) \\times disp = %s \\times %s = %s $ <br />" % (fwhmvph_om, disp, deltalambda)
        if areasource >= areafibre:
            omegasource = areafibre
            # verbose += "$\Omega_{source} = A_{fiber} = %s $ because $A_{source} \geq A_{fiber} $ <br />" % omegasource
        else:
            omegasource = areasource
            # verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < A_{fiber} $ <br />" % omegasource
        npixx = 1
        npixy = 1
        omegaskysource = areafibre
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        # verbose += "$n_{pix,x} = FWHM(VPH) = %s $ <br />" % npixx
        # verbose += "$n_{pix,y} = \\frac{2 \\times R_{fiber}}{ps} = \\frac{2 \\times %s}{%s} = %s $ <br />" % (rfibre, ps, npixy)
        # verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
        # verbose += "nfib = 0 <br />"
        # verbose += "nfib1 = 0 <br />"
    elif xit == 16: # psp_fiber: per spectral (1pixx x 4pixy) pixel per fiber
        deltalambda = disp  # because we're only using 1pixx
        verbose += "<b>### XIT = 16 <br />"
        verbose += "### per spectral pixels, per fiber </b><br />"
        # verbose += "$\Delta\lambda = FWHM(VPH) \\times disp = %s \\times %s = %s $ <br />" % (fwhmvph_om, disp, deltalambda)
        if areasource >= areafibre:
            omegasource = areafibre
            # verbose += "$\Omega_{source} = A_{fiber} = %s $ because $A_{source} \geq A_{fiber} $ <br />" % omegasource
        else:
            omegasource = areasource
            # verbose += "$\Omega_{source} = A_{source} = %s $ because $A_{source} < A_{fiber} $ <br />" % omegasource
        npixx = 1
        npixy = 4
        omegaskysource = areafibre
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        # verbose += "$n_{pix,x} = FWHM(VPH) = %s $ <br />" % npixx
        # verbose += "$n_{pix,y} = \\frac{2 \\times R_{fiber}}{ps} = \\frac{2 \\times %s}{%s} = %s $ <br />" % (rfibre, ps, npixy)
        # verbose += "$\Omega_{sky,source} = A_{fiber} = %s $ <br />" % omegaskysource
        # verbose += "nfib = 0 <br />"
        # verbose += "nfib1 = 0 <br />"
    if xit == 17: # psp_all: per spectral (1pixx x 4pixy) pixel for total source area (i.e. times number of fibers)
        deltalambda = disp
        omegasource = areasource
        npixx = 1
        npixy = nfibresy * 4
        omegaskysource = nfibres * areafibre
        nfib = 0. # Default value
        nfib1 = 0. # Default value
        verbose += "<b>### XIT = 17 <br />"
        verbose += "### per spectral pixels, All area </b><br />"
        # verbose += "$\Delta\lambda = FWHM(VPH) \\times disp = %s \\times %s = %s$ <br />" % (fwhmvph_om, disp, deltalambda)
        # verbose += "$\Omega_{source} = \\textrm{Area of source} = %s $ <br />" % omegasource
        # verbose += "$n_{pix,x} = FWHM(VPH) = %s$ <br />" % npixx
        # verbose += "$n_{pix,y} = N_{fibers,y} \\times \\frac{(2 \\times R_{fiber})}{ps} = %s \\times \\frac{(2 \\times %s)}{%s} = %s $ <br />" % (nfibresy, rfibre, ps, npixy)
        # verbose += "$\Omega_{sky,source} = N_{fibers} \\times A_{fiber} = %s \\times %s = %s $ <br />" % (nfibres, areafibre, omegaskysource)
        # verbose += "nfib = %s <br />" % nfib
        # verbose += "nfib1 = %s <br />" % nfib1

    return deltalambda, omegasource, npixx, npixy, nfib, nfib1, omegaskysource, verbose

# ********************************
# Function to derive spectroscopic parameters according to the case selected for line output.
# These parameters are related to the projected target area contributing to the line.
# Args:
#
def specparline(om_val, xit, areasource, diamsource, ps, disp, nfibres, areafibre, rfibre, nfibresy,
    areaseeing, seeingx, npixx):

  # FWHM does not depend on Observing mode: is fixed to 4 pixels by design

    fwhmvph_om = 4.0


    if xit == 0: # All area
        omegasource = areasource
        npixy = nfibresy * (2.0 * rfibre) / ps
    
        omegaskysource = nfibres * areafibre
        nfiby = 0.0
        nfib = 0.0
    
    elif xit == 1: # Seeing
        omegasource = areaseeing
        if (seeingx / 2.) <= rfibre:
            omegaskysource = areafibre
            nfiby = 1.0
            nfib = 1.0
        else:
            nfib = math.ceil (omegasource / areafibre)
            omegaskysource = nfib * areafibre
            nfiby = math.sqrt(nfib)         

        npixy = nfiby * 2.0 * rfibre / ps
    
    elif xit == 2: # 1 arcsec2    
        if areasource >= 1.0:    
            omegasource = 1.0    
        else:    
            omegasource = areasource    
            
        nfib1 = math.ceil (1.0 / areafibre)
        omegaskysource = nfib1 * areafibre    
        nfiby = math.sqrt(nfib1) 
        npixy = nfiby * 2.0 * rfibre / ps    
        
    elif xit == 3 : # 1 fibre
        if areasource >= areafibre:    
            omegasource = areafibre    
        else:    
            omegasource = areasource    

        nfiby = 1.0
        npixy = 2. * rfibre / ps    
        omegaskysource = areafibre

    return omegasource, npixy, omegaskysource, nfiby, npixx

# ********************************
# Function sclspect
# This function scales the input spectrum to the input flux in the band of interest
# Args: 
# iflux - total flux (in erg/s/cm**2/AA/arcsec2)
# wv - Wavelength (AA)
# wv1 - Lower wavelength of bandwidth (AA)
# wv2 - Upper wavelength of bandwidth (AA)
# ispect - Input spectrum template to normalize
# iband - Input filter transmission
#
def sclspect (iflux, wv, wv1, wv2, ispect, iband, wline, fline, fwhml):
    print 'FCONT=',iflux
    print 'ispect=',ispect
    wv1 = numpy.array(wv1)
    wv2 = numpy.array(wv2)
    minwv = min(wv)
    maxwv = max(wv)
    print 'min max wv=', minwv, maxwv
    print 'wv1=', wv1
    print 'wv2=', wv2

    # Extract effective wavelength of band
    leff = (wv2 + wv1) / 2.
    print "leff=", leff

    # Where input lambda range equals to leff - 0.5 AA
    leff1 = leff - 0.5
    dif = numpy.abs(wv - (leff1))
    mindif = numpy.min(dif)
  
    if leff1 < minwv:
        ind1 = numpy.where(wv == minwv)
    elif leff1 > maxwv-10:
        ind1 = numpy.where(wv == maxwv) - 10
    else:
        ind1 = numpy.where(dif == mindif)
    print 'leff1, dif, mindif, ind1=', leff1, dif, mindif, ind1

    # Where input lambda range equals to leff + 0.5 AA (need to add 0.1 AA to have exactly 11 points and thus 10 intervals for the normalization)
    leff2 = leff + 0.6 # or 0.6 for 11 points
    dif = numpy.abs(wv - (leff2))
    mindif = numpy.min(dif)
  
    if leff2 < minwv-10:
        ind2 = numpy.where(wv == minwv) + 10
    elif leff2 > maxwv:
        ind2 = numpy.where(wv == maxwv)
    else:
        ind2 = numpy.where(dif == mindif)
    print 'leff1, dif, mindif, ind1=', leff1, dif, mindif, ind1

    ind1 = ind1[0]
    ind2 = ind2[0]
    print 'ind1, ind2=', ind1, ind2

    if (ind1.size == 0):
        ind1 = 0
    else:
        ind1 = ind1[0]
    if (ind2.size == 0):
        ind2 = wv.size -1 
    else:
        ind2 = ind2[0]

    wvrange = wv[ind1:ind2]
    srange = ispect[ind1:ind2]
    print "wvrange =", wvrange
    print "srange =", srange
    # Extract filter transmission in wavelength range
    iband = iband[ind1:ind2]
    print "iband =", iband

    # Integrate in range to derive value    
    # value = numpy.trapz(srange * iband, wvrange) #/ numpy.trapz(iband, wvrange)
    # value = ispect[leff] / numpy.trapz(srange * iband, wvrange)
    # print "value =",value


    # Compute scaling
    # norm = iflux / value
    norm = iflux/ispect[leff]   #NEW scaling factor
    print "iflux =", iflux
    print "ispect[leff] =", ispect[leff]
    print "norm =", norm
    # Scaled spectrum
    scspect = ispect * norm
    print "ispect =", ispect
    print "scspect =", scspect

    # Create Gaussian
    print "# Adding Gaussian emission line"
    amplitude = fline
    mean = wline
    sigma = fwhml/(2*numpy.sqrt(2*numpy.log(2)))
    gauxmin = mean-5*sigma
    gauxmax = mean+5*sigma

    insidegaux = []
    insidegauy = []
    for idx, val in enumerate(wv):
        if gauxmin < wv[idx] < gauxmax:
            insidegaux.append(wv[idx])
            insidegauy.append(ispect[idx])

    numpoints = len(insidegaux)

    if isinstance(gauxmin, float) :
        minxindex = min(range(len(wv)), key=lambda i: abs(wv[i]-gauxmin))
        maxxindex = min(range(len(wv)), key=lambda i: abs(wv[i]-gauxmax))
        # meanxindex = int(round((minxindex+maxxindex)/2))    # central value index
        # meany = (ispect[minxindex] + ispect[maxxindex]) / 2
        if numpoints < maxxindex+1-minxindex:
            numpoints = numpoints+2
        gaux = numpy.linspace(gauxmin, gauxmax, numpoints, endpoint=True)
        gauy = mlab.normpdf(gaux, mean, sigma)  # gaussian y

    scspect[minxindex : maxxindex] = scspect[minxindex : maxxindex] + gauy[0: -1] * amplitude

    # print 'amplitude=', amplitude
    # print 'numpoints=', numpoints
    # print 'minxindex=', minxindex
    # print 'maxxindex=', maxxindex
    # print 'deltaindex=', maxxindex+1-minxindex
    # print 'len(gaux)=', len(gaux)
    # print 'len(gauy)=', len(gauy)
    # print 'len(ispect)=', len(ispect[minxindex : maxxindex])
    # print 'len(scspect)=', len(scspect[minxindex : maxxindex])
    # print ''
    # print 'len(insidegaux)=', numpoints
    # print 'len(wv)=',len(wv)
    # print 'len(ispect)=', len(ispect)
    # print 'len(newispect)=', len(newispect)
    # print 'type(newispect)=', type(newispect)
    # print 'scspect=', scspect
    print ''

    return norm, scspect

# ********************************
# Function signal: Number of photons from the source 
# For continuum, no strong dependence on source spectrum
# Args: 
# farcs - spectrum (already scaled to total flux, in erg/s/cm**2/AA) 
# dlambda - Bandwidth (AA)
# eff - Total system efficiency
# st - collecting area of telescope (cm**2)
# omega - Projected source area (arcsec**2)
# expt - Exposure time (seconds)
# ep - Energy of photons (ergs)
# linf - Minimum wavelength to consider
# lsup - Maximum wavelength to consider
# wv - Wavelength vector
#    
def signal(farcs, dlambda, lambdaeff, eff, st, omega, expt, ep, wv):
  
    total = farcs * eff * st * omega * expt / ep
    verbose = "$Total = \\frac{farcs \\times \Delta\lambda \\times eff \\times st \\times omega \\times expt}{E_{\gamma}} = \\frac{%s \\times %s \\times %s \\times %s \\times %s}{%s} = %s $ <br />" % (farcs, eff, st, omega, expt, ep, total)

    wv1 = lambdaeff - (dlambda / 2.)
    wv2 = lambdaeff + (dlambda / 2.)
    wv = numpy.array(wv)

    # If Deltalambda high enough, integration with trapezoid rule is realistic 
    if (dlambda > 1.5):
        # print 'dlambda = ', dlambda
        verbose += "<font color='red'>$\Delta\lambda > 1.5$, integration with trapezoid rule is realistic.<br /></font>"

        wv1 = numpy.array((math.ceil( wv1*10.))/10.)
        wv2 = numpy.array((math.ceil( wv2*10.))/10.)
        
        # Extract region of spectrum inside wavelength range
        ind1 = numpy.where(wv == wv1)
        ind2 = numpy.where(wv == wv2)
        ind1 = ind1[0]
        ind2 = ind2[0]

        if (ind1.size == 0):
            ind1 = 0
        else:
            ind1 = ind1[0]
        if (ind2.size == 0):
            ind2 = wv.size -1 
        else:
            ind2 = ind2[0]

        wvrange = wv[ind1:ind2]
        trange = total[ind1:ind2]

        # Integrate in range to derive value    
        if (len(wvrange) == 1):
            integ = trange[0] * dlambda
            verbose += "<font color='red'>ATTENTION! wvrange=1 and only 1 trange value is taken into account.<br />"
            verbose += "$S = trange \\times dlambda = %s \\times %s = %s $ <br /></font>" % (trange[0], dlambda, integ)
        else:
            integ = numpy.trapz(trange,wvrange)
            verbose += "Using Trapezoid rule to integrate in range to derive value.<br />"
            verbose += "$S = %s$ <br />" % integ
    # If Deltalambda is low, integration with trapezoid rule is non-realistic
    # Considering that the wavelength-dependence is low provides better results
    else:    
        verbose += "<font color='red'>$\Delta\lambda$ is low, integration with trapezoid rule is non-realistic. <br />"
        verbose += "Considering that the wavelength-dependence is low provides better results. <br />"
        verbose += "Extracting nearest wavelegnth to $\lambda_{eff}$ of VPH.</font><br />"
        # Extract nearest wavelength to the effective lambda of VPH
        diff = numpy.abs(wv - lambdaeff)
        ind = numpy.where(diff == numpy.min(diff))
        ind = ind[0]

        tvalue = total[ind]

        # Integrate in range to derive value    
        integ = tvalue * dlambda
        verbose += "Signal $S = tvalue \\times \Delta\lambda = %s \\times %s = %s$<br />" % (tvalue, dlambda, integ)
    return integ, verbose

# ********************************
# Function linesignal: Number of photons from the source if input flux is a line
# Args: 
# farcs - Total line flux, in erg/s/cm**2/AA or in erg/s/cm**2 if already integrated
# deltal: if line flux is provided in erg/s/cm**2 --> provide deltal = 1.
# eff - Total system efficiency array
# st - collecting area of telescope (cm**2)
# omega - Projected source area (arcsec**2)
# expt - Exposure time (seconds)
# lwv - Line wavelength 
# wv - Wavelength vector of efficiency
#     
def linesignal(farcs, deltal, eff, st, omega, expt, lwv, wv):
    import numpy    

    # Physical constants
    hplanck = 6.62606885e-27  # Planck constant (ergs/s)    
    lightv = 2.99792458e10    # Speed of light (cm/s)
    pi = 3.14159

    lwv = numpy.array(lwv)

    # Extract efficiency at the wavelength
    ind = numpy.where(wv ==  lwv)
    effatl = eff[ind]

    # Photon energy at the wavelength
    lambdacm = lwv * 1.e-8    
    enph = hplanck * lightv / (lambdacm)    
    # Number of photons in line captured by the instrument
    total = farcs * deltal * effatl * st * omega * expt / enph

    return total            


# ********************************    
# Signal of dark current    
def dark (exptime_val2, dc2, npix2):    
    results = exptime_val2 * dc2 * npix2
    verbose = "$S_{dark} = exptime \\times dc \\times npix = %s \\times %s \\times %s = %s $ <br />" % (exptime_val2, dc2, npix2, results)
    return results, verbose

# ********************************    
# Noise due to dark measurement to the square    
def darknoisesq(npix2, npdark_val2, exptime_val2, dc2, ron2):
    results = (npix2 / npdark_val2)**2 * npdark_val2 * (exptime_val2 * dc2  + (ron2 **2))
    verbose = "$ N_{DM}^{2} = \left(\\frac{n_{pix}}{npdark}\\right)^{2} \\times npdark \\times (exptime \\times dc  + (RON^{2})) = \left(\\frac{%s}{%s}\\right)^{2} \\times %s \\times (%s \\times %s + %s^{2} = %s $ <br />" % (npix2, npdark_val2, npdark_val2, exptime_val2, dc2, ron2, results)
    return results, verbose

# ********************************
# RON    
def readoutnoise (npix2, ron2):    
    results = npix2 * (ron2 **2)
    verbose = "$ RON = n_{pix} \\times RON^{2} = %s \\times %s = %s $ <br />" % (npix2, ron2, results)
    return results, verbose


