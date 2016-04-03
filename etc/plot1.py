

# def plot_and_save(tempname, x, y, label1, label2, label3):
#     import matplotlib.pyplot as plt
#     # ERASE EVERYTHING FIRST
#     plt.clf()
#     # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
#     # fig = plt.figure(num=None, figsize=(10, 6), facecolor='w', edgecolor='k')
#
#     plt.xlabel("Wavelength Angstroms", fontsize=18)
#     plt.ylabel("Flux (erg/s/cm**2/AA)", fontsize=18)
#
#     xmin = min(x)
#     xmax = max(x)
#     ymin = min(y)
#     ymax = max(y)
#
#     plt.xlim(xmin, xmax)
#     plt.ylim(ymin, ymax)
#
#     plt.plot(x, y, '-b', label=label1)
#     string1 = "Source: " + str(label1)
#     string2 = "Cont. mag: " + str("{:1.3f}".format(label2))
#     string3 = "Cont. band: " + str(label3)
#     text = string1 + '\n' + string2 + '\n' + string3
#     plt.annotate(text, xy=(1.01, 0.4), xytext=(0, +7.5), fontsize=18,
#     xycoords='axes fraction', textcoords='offset points',
#     bbox=dict(edgecolor='none', facecolor='white', alpha=0.8),
#     horizontalalignment='left', verticalalignment='middle')
#
#     ### ADJUST THE PLOT
#     leftval=0.12
#     bottomval=0.12
#     rightval=0.7
#     topval=0.89
#     plt.subplots_adjust(left=leftval, bottom=bottomval, right=rightval, top=topval, wspace=0.20, hspace=0.0)#almost default#
#
#     # plt.legend(loc=4)
#     plt.savefig(tempname, format='png', dpi=72)
#     return tempname



def plot_and_save_new(tempname, x, y, label1, label2, label3):
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

    ### ADJUST THE PLOT
    leftval=0.12
    bottomval=0.12
    rightval=0.7
    topval=0.89
    plt.subplots_adjust(left=leftval, bottom=bottomval, right=rightval, top=topval, wspace=0.20, hspace=0.0)#almost default#

    # plt.legend(loc=4)
    # plt.savefig(tempname, format='png', dpi=72)
    return fig

def plot_and_save2_new(tempname, x2, y2, x2b, y2b, x2c, y2c, x2d, y2d, label1, label2, label3):
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
    ymax = max([ymaxa,ymaxb,ymaxc,ymaxd])

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


    ### ADJUST THE PLOT
    leftval=0.12
    bottomval=0.12
    rightval=0.7
    topval=0.89
    plt.subplots_adjust(left=leftval, bottom=bottomval, right=rightval, top=topval, wspace=0.20, hspace=0.0)#almost default#


    plt.savefig('archivo_borrar.png', format='png', dpi=72)
    return fig



### SECOND PLOT
# def plot_and_save2(tempname, x2, y2, x2b, y2b, x2c, y2c, x2d, y2d, label1, label2, label3):
#     import matplotlib.pyplot as plt
#     # CREATE TEMPORARY FILE
#     # temp = tempfile.NamedTemporaryFile(suffix=".png", prefix="temp", dir="etc/static/etc/tmp/", delete=False)
#     # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
#     plt.clf()
#     # fig = plt.figure(num=None, figsize=(10, 6), facecolor='w', edgecolor='k')
#     plt.xlabel("Wavelength Angstroms", fontsize=18)
#     plt.ylabel("SNR per spectral pixel", fontsize=18)
#
#     filtx2, filty2 = ([] for i in range(2))
#     filtx2b, filty2b = ([] for i in range(2))
#     filtx2c, filty2c = ([] for i in range(2))
#     filtx2d, filty2d = ([] for i in range(2))
#
#     for idx, val in enumerate(y2):
#         if val != 0:
#             filtx2.append(x2[idx])
#             filty2.append(y2[idx])
#             filtx2b.append(x2b[idx])
#             filty2b.append(y2b[idx])
#             filtx2c.append(x2c[idx])
#             filty2c.append(y2c[idx])
#             filtx2d.append(x2d[idx])
#             filty2d.append(y2d[idx])
#
#
#     xmin = min(filtx2)
#     xmax = max(filtx2)
#     ymin = min(filty2)
#     ymaxa = max(filty2)
#     ymaxb = max(filty2b)
#     ymaxc = max(filty2c)
#     ymaxd = max(filty2d)
#     ymax = max([ymaxa,ymaxb,ymaxc,ymaxd])
#
#     diffy = ymax - ymin
#
#     plt.xlim(xmin, xmax)
#     plt.ylim(ymin, ymax+0.1*diffy)
#
#
#     plt.plot(filtx2, filty2, '-r', lw=1, label='per frame 1 fib')
#     plt.plot(filtx2b, filty2b, '-r', lw=3, label='all frames 1 fib')
#     plt.plot(filtx2c, filty2c, '-b', lw=1, label='per frame all fib')
#     plt.plot(filtx2d, filty2d, '-b', lw=3, label='all frames all fib')
#     plt.legend(loc=1, bbox_to_anchor=(1.53, 1))
#
#     string1 = "Source: " + label1
#     string2 = "VPH: " + label2
#     string3 = "Cont. band: " + label3
#     text = string1 + '\n' + string2 + '\n' + string3
#     plt.annotate(text, xy=(1.01, 0.4), xytext=(+0, +7.5), fontsize=18,
#     xycoords='axes fraction', textcoords='offset points',
#     bbox=dict(edgecolor='none', facecolor='white', alpha=0.8),
#     horizontalalignment='left', verticalalignment='middle')
#
#     ### ADJUST THE PLOT
#     leftval=0.12
#     bottomval=0.12
#     rightval=0.7
#     topval=0.89
#     plt.subplots_adjust(left=leftval, bottom=bottomval, right=rightval, top=topval, wspace=0.20, hspace=0.0)#almost default#
#
#
#     plt.savefig(tempname, format='png', dpi=72)
#     return tempname

