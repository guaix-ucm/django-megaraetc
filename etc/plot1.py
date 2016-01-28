import matplotlib.pyplot as plt
import numpy as np


def plot_and_save(x, y, label1):

    output = "etc/static/etc/plot_test.png"
    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    plt.clf()

    plt.xlabel("Wavelength Angstroms")
    plt.ylabel("Flux (erg/s/cm**2/AA)")

    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    plt.plot(x, y, '-b', label=label1)
    plt.legend(loc=4)
    plt.savefig(output, format='png', dpi=72)
    return output

def plot_and_save2(x, y, x2, y2, label, label2, label3):

    output = "etc/static/etc/plot_test2.png"
    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    plt.clf()

    plt.xlabel("Wavelength Angstroms")
    plt.ylabel("SNR per detector pixel per AA")

    filtx, filty, filty2 = ([] for i in range(3))

    for idx, val in enumerate(y):
        if val != 0:
            filtx.append(x[idx])
            filty.append(y[idx])
            filty2.append(y2[idx])

    xmin = min(filtx)
    xmax = max(filtx)
    ymin = min(filty2)
    ymax = max(filty2)
    diffx = xmax - xmin
    diffy = ymax - ymin

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    # plt.plot(filtx, filty, '-b', label='continuum signal')
    plt.plot(filtx, filty2, '-r', label='total snr')
    string1 = "Source spectrum: "+label
    string2 = "VPH: "+label2
    string3 = "Phot. band: "+label3
    plt.text(xmin+0.1*diffx, ymin+0.22*diffy, string1, fontsize=18)
    plt.text(xmin+0.1*diffx, ymin+0.12*diffy, string2, fontsize=18)
    plt.text(xmin+0.1*diffx, ymin+0.02*diffy, string3, fontsize=18)

    plt.legend(loc=4)
    plt.savefig(output, format='png', dpi=72)
    return output

