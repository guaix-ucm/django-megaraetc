import matplotlib.pyplot as plt

def plot_and_save(x, y, label1, label2, label3):

    output = "etc/static/etc/plot_test.png"
    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    plt.clf()

    plt.xlabel("Wavelength Angstroms", fontsize=18)
    plt.ylabel("Flux (erg/s/cm**2/AA)", fontsize=18)

    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    plt.plot(x, y, '-b', label=label1)
    string1 = "Source spec.: " + str(label1)
    string2 = "Continuum mag: " + str("{:1.3f}".format(label2))
    string3 = "Photometric band: " + str(label3)
    text = string1 + '\n' + string2 + '\n' + string3
    plt.annotate(text, xy=(1, 0.4), xytext=(-15, +5), fontsize=18,
    xycoords='axes fraction', textcoords='offset points',
    bbox=dict(facecolor='white', alpha=0.8),
    horizontalalignment='right', verticalalignment='middle')

    # plt.legend(loc=4)
    plt.savefig(output, format='png', dpi=72)
    return output


### SECOND PLOT
def plot_and_save2(x2, y2, x2b, y2b, x2c, y2c, x2d, y2d, label1, label2, label3):

    output = "etc/static/etc/plot_test2.png"
    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    plt.clf()

    plt.xlabel("Wavelength Angstroms", fontsize=18)
    plt.ylabel("SNR per spectral pixel", fontsize=18)

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
    ymax = max(filty2d)

    diffy = ymax - ymin

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax+0.1*diffy)


    plt.plot(filtx2, filty2, '-r', lw=1, label='SNR per frame 1 fib')
    plt.plot(filtx2b, filty2b, '-r', lw=3, label='SNR all frames 1 fib')
    plt.plot(filtx2c, filty2c, '-b', lw=1, label='SNR per frame all fib')
    plt.plot(filtx2d, filty2d, '-b', lw=3, label='SNR all frames all fib')
    string1 = "Source spec.: " + label1
    string2 = "VPH: " + label2
    string3 = "Photometric band: " + label3
    text = string1 + '\n' + string2 + '\n' + string3
    plt.annotate(text, xy=(1, 0.4), xytext=(-15, +7.5), fontsize=18,
    xycoords='axes fraction', textcoords='offset points',
    bbox=dict(facecolor='white', alpha=0.8),
    horizontalalignment='right', verticalalignment='middle')

    plt.legend(loc=4)
    plt.savefig(output, format='png', dpi=72)
    return output

