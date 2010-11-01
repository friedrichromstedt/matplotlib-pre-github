import numpy
import pylab

def test_annotate():
    #pylab.rcParams['gray'] = True
    fig = pylab.figure(1, figsize=(8, 5))
    fig.set_gray(True)

    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, 5), 
            ylim=(-4, 3))

    t = numpy.arange(0.0, 5.0, 0.01)
    s = numpy.cos(2 * numpy.pi * t)
    line, = ax.plot(t, s, lw=3, color='yellow')
    outtext = pylab.text(-0.5, 3.2, 'waka', ha='center', color='green')
    arr = pylab.annotate('blah', (1, 2.1), (2.5, 2.1),
            va='center', ha='center', 
            arrowprops=dict(arrowstyle='<->', linewidth=2.0, color='red'),
            color='green')
    otherarrow = pylab.arrow(3.5, 2, 0.25, 0.25, color='red', linewidth=2.0)
    otherarrow.set_gray(True)
    pylab.savefig('gray_annotate.png')
