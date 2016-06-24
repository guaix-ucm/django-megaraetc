
def plot_gaussian(tempname, linef_var, mu_var, sigma_var):
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.mlab as mlab
    import math

    fig, ax = plt.subplots()

    amplitude = linef_var
    mean = mu_var
    variance = sigma_var**2
    sigma = math.sqrt(variance)
    numpoints = 100000

    # PLOT FROM MATPLOTLIB FUNCTION
    x = np.linspace(-5*sigma, 5*sigma, numpoints)
    y = amplitude*mlab.normpdf(x, mean, sigma)
    plt.plot(x, y, color='b')
    ### ADJUST THE PLOT
    # leftval=0.12
    # bottomval=0.12
    # rightval=0.7
    # topval=0.89
    # plt.subplots_adjust(left=leftval, bottom=bottomval, right=rightval, top=topval, wspace=0.20, hspace=0.0)#almost default#
    return fig


def plot_and_save_new(tempname, x, y, mu_var, fwhm_var, linef_var,
                      vph_minval_var, vph_maxval_var, label1, label2, label3):
    import matplotlib.pyplot as plt
    from scipy.interpolate import UnivariateSpline
    import numpy
    # ERASE EVERYTHING FIRST
    plt.clf()

    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    # fig = plt.figure(num=None, figsize=(10, 6), facecolor='w', edgecolor='k')

    # fig = plt.figure()
    #
    # plt.xlabel("Wavelength Angstroms", fontsize=18)
    # plt.ylabel("Flux (erg/s/cm**2/AA)", fontsize=18)
    #
    fig, ax = plt.subplots()

    filtx, filty = ([] for i in range(2))
    for idx, val in enumerate(y):
        if val != 0 and idx % 3 == 0:
            filtx.append(x[idx])
            filty.append(y[idx]*10**17)

    xmin = min(filtx)
    xmax = max(filtx)
    ymin = min(filty)
    ymax = max(filty)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # DETAILED BUT SLOW
    ax.plot(filtx, filty, '-b', label=label1)

    # SMOOTH AND FAST
    # spline = UnivariateSpline(x, y)
    # xs = numpy.linspace(numpy.min(x), numpy.max(x), 5000)
    # ax.plot( xs, spline(xs), alpha=0.3)

    ax.set_xlabel("Wavelength Angstroms", fontsize=18)
    ax.set_ylabel("Flux (10E-17 erg/s/cm**2/AA)", fontsize=18)
    ax.yaxis.set_label_coords(-0.15, +0.8)

    string1 = "Source: " + str(label1)
    string2 = "Cont. mag: " + str("{:1.3f}".format(label2))
    string3 = "Cont. band: " + str(label3)
    # text = string1 + '\n' + string2 + '\n' + string3
    plt.annotate(string1, xy=(0.8, 0.6), xytext=(0, +7.5), fontsize=18,
                 xycoords='axes fraction', textcoords='offset points',
                 bbox=dict(edgecolor='none', facecolor='white', alpha=0.8),
                 horizontalalignment='left', verticalalignment='center')
    plt.annotate(string2, xy=(0.8, 0.5), xytext=(0, +7.5), fontsize=18,
                 xycoords='axes fraction', textcoords='offset points',
                 bbox=dict(edgecolor='none', facecolor='white', alpha=0.8),
                 horizontalalignment='left', verticalalignment='center')
    plt.annotate(string3, xy=(0.8, 0.4), xytext=(0, +7.5), fontsize=18,
                 xycoords='axes fraction', textcoords='offset points',
                 bbox=dict(edgecolor='none', facecolor='white', alpha=0.8),
                 horizontalalignment='left', verticalalignment='center')

    ### PLOT GAUSSIAN ###
    import matplotlib.mlab as mlab
    import math

    amplitude = linef_var
    mean = mu_var
    sigma = fwhm_var/(2*numpy.sqrt(2*numpy.log(2)))
    # variance = sigma**2
    # sigma = math.sqrt(variance)
    numpoints = 1000

    gauxmin = mean-10*sigma
    gauxmax = mean+10*sigma

    if isinstance(gauxmin, float) :
        gaux = numpy.linspace(gauxmin, gauxmax, numpoints)
        minxindex = min(range(len(filtx)), key=lambda i: abs(filtx[i]-gauxmin))
        maxxindex = min(range(len(filtx)), key=lambda i: abs(filtx[i]-gauxmax))
        # meanxindex = int(round((minxindex+maxxindex)/2))    # central value index
        meany = (filty[minxindex]+filty[maxxindex])/2
        gauy = meany + mlab.normpdf(gaux, mean, sigma)*(amplitude*10**17)  # gaussian y
        ax.plot([gauxmin, gauxmax], [filty[minxindex], filty[maxxindex]],
                color='g')  # continuum

        ax.plot([gauxmin, gauxmin], [filty[minxindex], gauy[0]],
                color='g', ls='--')
        ax.plot([gauxmax, gauxmax], [gauy[numpoints-1], filty[maxxindex]],
                color='g', ls='--')

        ax.plot(gaux, gauy, color='purple')  # gaussian plot
        plt.plot([vph_minval_var, vph_minval_var], [ymin/2, ymax*2],
                 ls='--', color='red')  # vph-limit
        plt.plot([vph_maxval_var, vph_maxval_var], [ymin/2, ymax*2],
                 ls='--', color='red')  # vph-limit
    else:
        ax.text(xmax/2, ymax/2,'STOP')
        print "STOP"

    ### ADJUST THE PLOT
    leftval=0.12
    bottomval=0.12
    rightval=0.7
    topval=0.89
    plt.subplots_adjust(left=leftval, bottom=bottomval, right=rightval,
                        top=topval, wspace=0.20, hspace=0.0) # almost default

    # plt.legend(loc=4)
    # plt.savefig(tempname, format='png', dpi=72)
    return fig

def plot_and_save2_new(tempname, x2, y2, x2b, y2b,
                       x2c, y2c, x2d, y2d, label1, label2, label3):
    import matplotlib.pyplot as plt
    # CREATE TEMPORARY FILE
    # temp = tempfile.NamedTemporaryFile(suffix=".png", prefix="temp", dir="etc/static/etc/tmp/", delete=False)
    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    plt.clf()
    fig, ax = plt.subplots()
    # fig = plt.figure(num=None, figsize=(10, 6), facecolor='w', edgecolor='k')
    ax.set_xlabel("Wavelength Angstroms", fontsize=18)
    ax.set_ylabel("SNR per spectral pixel", fontsize=18)
    ax.yaxis.set_label_coords(-0.15, +0.8)

    filtx2, filty2 = ([] for i in range(2))
    filtx2b, filty2b = ([] for i in range(2))
    filtx2c, filty2c = ([] for i in range(2))
    filtx2d, filty2d = ([] for i in range(2))

    for idx, val in enumerate(y2):
        if val != 0:
            filtx2.append(x2[idx])
            filty2.append(y2[idx])
            filtx2b.append(x2b[idx])
            filty2b.append(y2b[idx])
            filtx2c.append(x2c[idx])
            filty2c.append(y2c[idx])
            filtx2d.append(x2d[idx])
            filty2d.append(y2d[idx])

    xmin = min(filtx2)
    xmax = max(filtx2)
    ymin = min(filty2)
    ymaxa = max(filty2)
    ymaxb = max(filty2b)
    ymaxc = max(filty2c)
    ymaxd = max(filty2d)
    ymax = max([ymaxa, ymaxb, ymaxc, ymaxd])

    diffy = ymax - ymin

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax+0.1*diffy)

    ax.plot(filtx2, filty2, '-r', lw=1, label='per frame 1 fib')
    ax.plot(filtx2b, filty2b, '-r', lw=3, label='all frames 1 fib')
    ax.plot(filtx2c, filty2c, '-b', lw=1, label='per frame all fib')
    ax.plot(filtx2d, filty2d, '-b', lw=3, label='all frames all fib')

    # ax.legend(loc='center right', bbox_to_anchor=(1.5, 1.0))
    import pylab
    pylab.legend(loc='best')
    string1 = "Source: " + label1
    string2 = "VPH: " + label2
    string3 = "Cont. band: " + label3
    # text = string1 + '\n' + string2 + '\n' + string3
    ax.annotate(string1, xy=(0.8, 0.6), xytext=(+0, +7.5), fontsize=18,
                xycoords='axes fraction', textcoords='offset points',
                bbox=dict(edgecolor='none', facecolor='white', alpha=0.8),
                horizontalalignment='left', verticalalignment='center')
    ax.annotate(string2, xy=(0.8, 0.5), xytext=(+0, +7.5), fontsize=18,
                xycoords='axes fraction', textcoords='offset points',
                bbox=dict(edgecolor='none', facecolor='white', alpha=0.8),
                horizontalalignment='left', verticalalignment='center')
    ax.annotate(string3, xy=(0.8, 0.4), xytext=(+0, +7.5), fontsize=18,
                xycoords='axes fraction', textcoords='offset points',
                bbox=dict(edgecolor='none', facecolor='white', alpha=0.8),
                horizontalalignment='left', verticalalignment='center')

    # ADJUST THE PLOT
    leftval = 0.12
    bottomval = 0.12
    rightval = 0.7
    topval = 0.89
    plt.subplots_adjust(left=leftval, bottom=bottomval, right=rightval,
                        top=topval, wspace=0.20, hspace=0.0)  # almost default

    plt.savefig('archivo_borrar.png', format='png', dpi=72)
    return fig
