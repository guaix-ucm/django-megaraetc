import matplotlib.pyplot as plt
import numpy as np


def plot_and_save2(x, y, label):

    output = "etc/static/etc/plot_test2.png"
    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    plt.clf()

    plt.xlabel("Wavelength Angstroms")
    plt.ylabel("Source Flux")

    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    plt.plot(x, y, '-b', label=label)
    plt.legend()
    plt.savefig(output, format='png', dpi=72)
    return output


