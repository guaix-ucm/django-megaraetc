from justcalc import calc
import numpy

import matplotlib.pyplot as plt
import os

def plot_and_save(x,y,label):

    output = "etc/static/etc/plot_test.png"
    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    plt.clf()

    plt.xlabel("Wavelength Angstroms")
    plt.ylabel("Flux (integrated area normalized to 1)")

    xmin=min(x)
    xmax=max(x)
    ymin=min(y)
    ymax=max(y)

    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)

    plt.plot(x,y,'-r',label=label)
    plt.legend()
    plt.savefig(output, format='png', dpi=72)
    return output

