import numpy
import numpy as np
import pylab
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter

def test_annotate():
    """Puts some annotation with arrows."""

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
    """Plots some polygons."""

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
    """Plots some ill-designed cubes ... :-) Don't worry Ben"""

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
    #######################
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

def test_surface3d():
    """From the examples.  It is expected that the colorbar will not
    inherit gray setting."""

    fig = plt.figure()

    ax = fig.gca(projection='3d')
    ax.set_gray(True)
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    Z = np.ma.masked_array(Z, mask=np.logical_and(Z > -0.45, Z < 0.25))
    print "Z shape:", Z.shape
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,
            linewidth=0, antialiased=False)
    ax.set_zlim3d(-1.01, 1.01)

    ax.w_zaxis.set_major_locator(LinearLocator(10))
    ax.w_zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.savefig('gray_surface3d.png')

def test_cylinder():
    """Plots a cylinder."""

    fig = plt.figure()
    #ax = Axes3D(fig)
    ax = fig.gca(projection='3d')

    # ----- Doesn't seem to do anything -------
    fig.set_gray(True)
    ax.set_gray(True)


    # Cylindrical shell
    phi = np.linspace(0, 2 * np.pi, 100)
    #r = np.ones(100)
    h = np.linspace(0, 1, 100)

    phi_grid, h_grid = np.meshgrid(phi, h)

    #phi_grid, r_grid = np.meshgrid(phi, r)
    x = 10 * np.cos(phi_grid)
    y = 10 * np.sin(phi_grid)
    z = 10 * h_grid


    # Top cover
    #phi_a = np.linspace(0, 2 * np.pi, 100)
    #h_2 = np.ones(100)
    r = np.linspace(0, 1, 100)

    phi_grid, r_grid = np.meshgrid(phi, r)
    x_2 = 10 * np.cos(phi_grid) * r_grid
    y_2 = 10 * np.sin(phi_grid) * r_grid
    z_2 = 10 * np.ones([100,100])


    #ax.plot_surface(x, y, z,  rstride=9, cstride=15)#, linewidth=1, alpha=1)
    #ax.plot_surface(x_2, y_2, z_2,  rstride=5, cstride=20)#, linewidth=1, alpha=1)
    print x.shape, y.shape, z.shape
    print x_2.shape, y_2.shape, z_2.shape
    surf = ax.plot_surface(x, y, z,  rstride=9, cstride=15, linewidth=1, alpha=1)
    surf.set_gray(True)
    #ax.plot_surface(x_2, y_2, z_2,  rstride=5, cstride=20, linewidth=1, alpha=1)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.savefig('gray_cylinder.png')

def test_spheres():
    """Plots Spheres."""

    fig = plt.figure()
    #ax = Axes3D(fig)
    ax = fig.add_subplot(111, projection='3d')
    #tracer.run("ax = Axes3D(fig)")


    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x = 10 * np.outer(np.cos(u), np.sin(v))
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x*0.9, y*0.9, z*0.9,  rstride=4, cstride=4, color='r', alpha=0.5)
    ax.plot_wireframe(x, y, z, rstride=10, cstride=10, color='b')
    ax.plot_wireframe(x*1.1, y*1.1, z*1.1, rstride=20, cstride=20, color='r')

    ax.set_gray(True)

    plt.savefig('gray_spheres.png')
