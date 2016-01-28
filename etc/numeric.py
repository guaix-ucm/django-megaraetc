#
# Copyright 2010-2014 Universidad Complutense de Madrid (Spain)
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
#
def specpar(om_val, xit, disp, ps, nfibres, nfibresy, areafibre, rfibre,  deltab, areasource, 
            diamsource, areaseeing, seeingx):

  # FWHM does not depend on Observing mode: is fixed to 4 pixels by design

    fwhmvph_om = 4.0
    
    if xit == 0: # P2SP (per 2 spectral pixels), All area    
        deltalambda = fwhmvph_om * disp
        omegasource = areasource
        npixx = fwhmvph_om    
        npixy = nfibresy * (2.0 * rfibre) / ps    
        omegaskysource = nfibres * areafibre
        nfib = 0. # Default value
        nfib1 = 0. # Default value
    
    elif xit == 1: # 1AA, All area    
        deltalambda = 1.0    
        omegasource = areasource    
        npixx = 1.0 / disp    
        npixy = nfibresy * (2.0 * rfibre) / ps    
        omegaskysource = nfibres * areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
    
    elif xit == 2: # Bandwidth, All area    
        deltalambda = deltab    
        omegasource = areasource    
        npixx = deltab / disp    
        npixy = nfibresy * (2.0 * rfibre) / ps    
        omegaskysource = nfibres * areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
    
    elif xit == 3: # P2SP, seeing    
        deltalambda = fwhmvph_om * disp    
        omegasource = areaseeing    
        if (seeingx / 2.) <= rfibre:
            omegaskysource = areafibre
            nfiby = 1.0
            nfib = 1.0
        else:
            nfib = math.ceil (omegasource / areafibre)
            omegaskysource = nfib * areafibre
            nfiby = math.sqrt(nfib) 
    
        npixx = fwhmvph_om    
        npixy = nfiby * 2.0 * rfibre / ps
        nfib1 = 0. # Default value
    
    elif xit == 4: # 1AA, seeing    
        deltalambda = 1.0
        omegasource = areaseeing    
        if (seeingx / 2.) <= rfibre:
            omegaskysource = areafibre
            nfiby = 1.0
            nfib = 1.0
        else:
            nfib = math.ceil (omegasource / areafibre)
            omegaskysource = nfib * areafibre
            nfiby = math.sqrt(nfib) 
    
        npixx = 1.0 / disp    
        npixy = nfiby * 2.0 * rfibre / ps            
        nfib1 = 0. # Default value
    
    elif xit == 5: # Bandwidth, seeing    
        deltalambda = deltab    
        omegasource = areaseeing
        if (seeingx / 2.) <= rfibre:
            omegaskysource = areafibre
            nfiby = 1.0
            nfib = 1.0
        else:
            nfib = math.ceil (omegasource / areafibre)
            omegaskysource = nfib * areafibre
            nfiby = math.sqrt(nfib) 
    
        npixx = deltab / disp     
        npixy = nfiby * 2.0 * rfibre / ps
        nfib1 = 0. # Default value
    
    elif xit == 6: # P2SP, 1 arcsec2    
        deltalambda = fwhmvph_om * disp    
        if areasource >= 1.0:
            omegasource = 1.0    
        else:    
            omegasource = areasource
        
        nfib1 = math.ceil (1.0 / areafibre)
        omegaskysource = nfib1 * areafibre    
        nfiby = math.sqrt(nfib1) 
        npixx = fwhmvph_om    
        npixy = nfiby * 2.0 * rfibre / ps
        nfib = 0. # Default value        

    elif xit == 7: # 1AA, 1 arcsec2    
        deltalambda = 1.0    
        if areasource >= 1.0:
            omegasource = 1.0    
        else:    
            omegasource = areasource
        
        nfib1 = math.ceil (1.0 / areafibre)
        omegaskysource = nfib1 * areafibre    
        nfiby = math.sqrt(nfib1)     
        npixx = 1.0 / disp    
        npixy = nfiby * 2.0 * rfibre / ps    
        nfib = 0. # Default value
    
    elif xit == 8: # Bandwidth, 1 arcsec2    
        deltalambda = deltab    
        if areasource >= 1.0:
            omegasource = 1.0    
        else:    
            omegasource = areasource

        nfib1 = math.ceil (1.0 / areafibre)
        omegaskysource = nfib1 * areafibre    
        nfiby = math.sqrt(nfib1) 
        npixx = deltab / disp    
        npixy = nfiby * 2.0 * rfibre / ps    
        nfib = 0. # Default value
    
    elif xit == 9: # P2SP, 1 fibre    
        deltalambda = fwhmvph_om * disp    
        if areasource >= areafibre:    
            omegasource = areafibre    
        else:    
            omegasource = areasource    

        npixx = fwhmvph_om    
        npixy = 2. * rfibre / ps    
        omegaskysource = areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
    
    elif xit == 10: # 1AA, 1 fibre    
        deltalambda = 1.0    
        if areasource >= areafibre:    
            omegasource = areafibre    
        else:    
            omegasource = areasource    
        npixx = 1.0 / disp    
        npixy = 2. * rfibre / ps    
        omegaskysource = areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
    
    elif xit == 11: # Bandwidth, 1 fibre    
        deltalambda = deltab    
        if areasource >= areafibre:    
            omegasource = areafibre    
        else:    
            omegasource = areasource    

        npixx = deltab / disp  # lambda range of vph (in angstroms) / (angstrom per pixel)
        npixy = 2. * rfibre / ps    
        omegaskysource = areafibre    
        nfib = 0. # Default value
        nfib1 = 0. # Default value
    

    return deltalambda, omegasource, npixx, npixy, nfib, nfib1, omegaskysource, omegasource    

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
# iflux - total flux (in erg/s/cm**2/AA) 
# wv - Wavelength (AA)
# wv1 - Lower wavelength of bandwidth (AA)
# wv2 - Upper wavelength of bandwidth (AA)
# ispect - Input spectrum template to normalize
# iband - Input filter transmission
#
def sclspect (iflux, wv, wv1, wv2, ispect, iband):

    wv1 = numpy.array(wv1)
    wv2 = numpy.array(wv2)
    minwv = min(wv)
    maxwv = max(wv)

    # Extract effective wavelength of band
    leff = (wv2 + wv1) / 2.

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

    # Where input lambda range equals to leff + 0.5 AA
    leff2 = leff + 0.5
    dif = numpy.abs(wv - (leff2))
    mindif = numpy.min(dif)
  
    if leff2 < minwv-10:
        ind2 = numpy.where(wv == minwv) + 10
    elif leff2 > maxwv:
        ind2 = numpy.where(wv == maxwv)
    else:
        ind2 = numpy.where(dif == mindif)

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
    srange = ispect[ind1:ind2]
 
    # Extract filter transmission in wavelength range
    iband = iband[ind1:ind2]

    # Integrate in range to derive value    
    value = numpy.trapz(srange * iband ,wvrange)

    # Compute scaling
    norm = iflux / value

    # Scaled spectrum
    scspect = norm * ispect

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

    wv1 = lambdaeff - (dlambda / 2.)
    wv2 = lambdaeff + (dlambda / 2.)
    wv = numpy.array(wv)

    # If Deltalambda high enough, integration with trapezoid rule is realistic 
    if (dlambda > 1.0):

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
        else:
            integ = numpy.trapz(trange,wvrange)

    # If Deltalambda is low, integration with trapezoid rule is non-realistic
    # Considering that the wavelength-dependence is low provides better results
    else:    

        # Extract nearest wavelength to the effective lambda of VPH
        diff = numpy.abs(wv - lambdaeff)
        ind = numpy.where(diff == numpy.min(diff))
        ind = ind[0]

        tvalue = total[ind]

        # Integrate in range to derive value    
        integ = tvalue * dlambda

    return integ, total

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
    lightv = 2.99792458e10    # Light velocity (cm/s)
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
    return exptime_val2 * dc2 * npix2

# ********************************    
# Noise due to dark measurement to the square    
def darknoisesq(npix2, npdark_val2, exptime_val2, dc2, ron2):    
    return (npix2 / npdark_val2)**2 * npdark_val2 * (exptime_val2 * dc2  + (ron2 **2))    

# ********************************
# RON    
def readoutnoise (npix2, ron2):    
    return npix2 * (ron2 **2)


