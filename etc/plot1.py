import matplotlib.pyplot as plt

def plot_and_save(tempname, x, y, label1, label2, label3):
    # ERASE EVERYTHING FIRST
    plt.clf()
    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    # fig = plt.figure(num=None, figsize=(10, 6), facecolor='w', edgecolor='k')

    plt.xlabel("Wavelength Angstroms", fontsize=18)
    plt.ylabel("Flux (erg/s/cm**2/AA)", fontsize=18)

    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    plt.plot(x, y, '-b', label=label1)
    string1 = "Source: " + str(label1)
    string2 = "Cont. mag: " + str("{:1.3f}".format(label2))
    string3 = "Cont. band: " + str(label3)
    text = string1 + '\n' + string2 + '\n' + string3
    plt.annotate(text, xy=(1.01, 0.4), xytext=(0, +7.5), fontsize=18,
    xycoords='axes fraction', textcoords='offset points',
    bbox=dict(facecolor='white', alpha=0.8),
    horizontalalignment='left', verticalalignment='middle')

    ### ADJUST THE PLOT
    leftval=0.12
    bottomval=0.12
    rightval=0.7
    topval=0.89
    plt.subplots_adjust(left=leftval, bottom=bottomval, right=rightval, top=topval, wspace=0.20, hspace=0.0)#almost default#

    # plt.legend(loc=4)
    plt.savefig(tempname, format='png', dpi=72)
    return tempname


### SECOND PLOT
def plot_and_save2(tempname, x2, y2, x2b, y2b, x2c, y2c, x2d, y2d, label1, label2, label3):
    # CREATE TEMPORARY FILE
    # temp = tempfile.NamedTemporaryFile(suffix=".png", prefix="temp", dir="etc/static/etc/tmp/", delete=False)
    # NEED TO REMOVE THE CANVAS FIRST OR IT OVERPLOTS
    plt.clf()
    # fig = plt.figure(num=None, figsize=(10, 6), facecolor='w', edgecolor='k')
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
    ymaxa = max(filty2)
    ymaxb = max(filty2b)
    ymaxc = max(filty2c)
    ymaxd = max(filty2d)
    ymax = max([ymaxa,ymaxb,ymaxc,ymaxd])

    diffy = ymax - ymin

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax+0.1*diffy)


    plt.plot(filtx2, filty2, '-r', lw=1, label='per frame 1 fib')
    plt.plot(filtx2b, filty2b, '-r', lw=3, label='all frames 1 fib')
    plt.plot(filtx2c, filty2c, '-b', lw=1, label='per frame all fib')
    plt.plot(filtx2d, filty2d, '-b', lw=3, label='all frames all fib')
    plt.legend(loc=1, bbox_to_anchor=(1.53, 1))

    string1 = "Source: " + label1
    string2 = "VPH: " + label2
    string3 = "Cont. band: " + label3
    text = string1 + '\n' + string2 + '\n' + string3
    plt.annotate(text, xy=(1.01, 0.4), xytext=(+0, +7.5), fontsize=18,
    xycoords='axes fraction', textcoords='offset points',
    bbox=dict(facecolor='white', alpha=0.8),
    horizontalalignment='left', verticalalignment='middle')

    ### ADJUST THE PLOT
    leftval=0.12
    bottomval=0.12
    rightval=0.7
    topval=0.89
    plt.subplots_adjust(left=leftval, bottom=bottomval, right=rightval, top=topval, wspace=0.20, hspace=0.0)#almost default#


    plt.savefig(tempname, format='png', dpi=72)
    return tempname

