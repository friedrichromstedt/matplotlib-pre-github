import numpy
import pylab
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D

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

######################################################################
#	Author:	Ben Root
#	Date:	February 3, 2010
#	ECE 5273
#	Assignment 2
######################################################################

def plot_cube(ax, cubePoints) :

    # polys is a list which each element contains a matrix of coordinates
    # for the verticies of a polygon.  So, each element represents a polygon.
    polys = []

    # Face 1
    # An element member can be a 2-D numpy array.
    # Each row in cubePoints is the coordinate of a vertex.
    # The columns correspond to X, Y, and Z axes.
    polys.append(cubePoints[0:4, :])

    # Face 2
    # An element member of polys can also be a list of 1-D numpy arrays.
    # Again, each member of list 's' is a vertex, and
    #  each element of the 1-D numpy array correspond to X,Y,Z.
    s = []
    s.append(cubePoints[0, :])
    s.append(cubePoints[1, :])
    s.append(cubePoints[5, :])
    s.append(cubePoints[4, :])
    polys.append(s)

    # Face 3
    # Lastly, an element member of polys can also be a 2d python array (list 
    # of lists)
    s = [ [cubePoints[0, 0], cubePoints[0, 1], cubePoints[0, 2]],
	  [cubePoints[3, 0], cubePoints[3, 1], cubePoints[3, 2]],
          [cubePoints[7, 0], cubePoints[7, 1], cubePoints[7, 2]],
          [cubePoints[4, 0], cubePoints[4, 1], cubePoints[4, 2]] ]
	  
    polys.append(s)

    # faceColors can be a scalar, applying that color to all polygons,
    #   or can be a list of colors of equal size to polys.
    faceColors = ['r', 'g', 'gray']
    
    polyc = art3d.Poly3DCollection(polys, facecolors = faceColors)

    # Alpha value is applied to all polygons.
    polyc.set_alpha(0.1)

    # ------- This doesn't work either... --------
    #polyc.set_gray(True)

    # Add this collection to the 3d axis object.
    ax.add_collection3d(polyc)

def test_polygon3d():

    # Numpy matrix containing the coordinates of
    # the 8 verticies of a unit cube in 3D space.
    cubePoints = numpy.array([ [0.0, 0.0, 0.0],
			       [0.0, 0.0, 1.0],
			       [1.0, 0.0, 1.0],
			       [1.0, 0.0, 0.0],

			       [0.0, 1.0, 0.0],
			       [0.0, 1.0, 1.0],
			       [1.0, 1.0, 1.0],
			       [1.0, 1.0, 0.0] ])

    fig = plt.figure()

    # ----- This doesn't make a difference to grayscale mode ------
    #ax = Axes3D(fig)
    ax = fig.gca(projection='3d')

    plot_cube(ax, cubePoints)

    ax.hold(True)

    ########################
    # Rotate cube a bit, move it a bit,  and add it to the figure.
    ########################
    cubePoints = numpy.array([[ 1.0,   1.0,   0.0 ],
			      [ 1.5,   1.0,   1.0 ],
			      [ 2.5,   1.0,   0.5],
			      [ 2.0,   1.0,  -0.5],
			      [ 1.0,   2.14,  0.0],
 			      [ 1.5,   2.14,  1.0],
			      [ 2.5,   2.14,  0.5],
			      [ 2.0,   2.14, -0.5] ])

    plot_cube(ax, cubePoints)

    ########################
    # Some more rotations and moving, and add it to the figure
    ########################
    cubePoints = numpy.array([[ 0.0,   1.0,   1.0],
			      [ 0.0 ,  0.658, 2.0],
			      [ 1.06,  0.658, 2.0],
			      [ 1.06,  1.0,   1.0],
			      [ 0.0,   2.0,   1.342],
 			      [ 0.0,   1.658, 2.342],
			      [ 1.06,  1.658, 2.342],
			      [ 1.06,  2.0,   1.342] ])
  
    plot_cube(ax, cubePoints)

    ax.set_xlim3d(0.0, 2.5)
    ax.set_ylim3d(0.0, 2.5)
    ax.set_zlim3d(0.0, 10.0)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # ------ These don't work... ---------
    fig.set_gray(True)
    ax.set_gray(True)

    plt.savefig('gray_polygon3d.png')
