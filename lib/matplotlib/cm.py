"""
This module provides a large set of colormaps, functions for
registering new colormaps and for getting a colormap by name,
and a mixin class for adding color mapping functionality.

"""

import os

import numpy as np
from numpy import ma
import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.cbook as cbook
from matplotlib._cm import datad

cmap_d = dict()

# reverse all the colormaps.
# reversed colormaps have '_r' appended to the name.

def _reverser(f):
    def freversed(x):
        return f(1-x)
    return freversed

def revcmap(data):
    data_r = {}
    for key, val in data.iteritems():
        if callable(val):
            valnew = _reverser(val)
                # This doesn't work: lambda x: val(1-x)
                # The same "val" (the first one) is used
                # each time, so the colors are identical
                # and the result is shades of gray.
        else:
            valnew = [(1.0 - a, b, c) for a, b, c in reversed(val)]
        data_r[key] = valnew
    return data_r

LUTSIZE = mpl.rcParams['image.lut']

_cmapnames = datad.keys()  # need this list because datad is changed in loop

for cmapname in _cmapnames:
    cmapname_r = cmapname+'_r'
    cmapspec = datad[cmapname]
    if 'red' in cmapspec:
        datad[cmapname_r] = revcmap(cmapspec)
        cmap_d[cmapname] = colors.LinearSegmentedColormap(
                                cmapname, cmapspec, LUTSIZE)
        cmap_d[cmapname_r] = colors.LinearSegmentedColormap(
                                cmapname_r, datad[cmapname_r], LUTSIZE)
    else:
        revspec = list(reversed(cmapspec))
        if len(revspec[0]) == 2:    # e.g., (1, (1.0, 0.0, 1.0))
            revspec = [(1.0 - a, b) for a, b in revspec]
        datad[cmapname_r] = revspec

        cmap_d[cmapname] = colors.LinearSegmentedColormap.from_list(
                                cmapname, cmapspec, LUTSIZE)
        cmap_d[cmapname_r] = colors.LinearSegmentedColormap.from_list(
                                cmapname_r, revspec, LUTSIZE)

locals().update(cmap_d)

def register_cmap(name=None, cmap=None, data=None, lut=None):
    """
    Add a colormap to the set recognized by :func:`get_cmap`.

    It can be used in two ways::

        register_cmap(name='swirly', cmap=swirly_cmap)

        register_cmap(name='choppy', data=choppydata, lut=128)

    In the first case, *cmap* must be a :class:`colors.Colormap`
    instance.  The *name* is optional; if absent, the name will
    be the :attr:`name` attribute of the *cmap*.

    In the second case, the three arguments are passed to
    the :class:`colors.LinearSegmentedColormap` initializer,
    and the resulting colormap is registered.

    """
    if name is None:
        try:
            name = cmap.name
        except AttributeError:
            raise ValueError("Arguments must include a name or a Colormap")

    if not cbook.is_string_like(name):
        raise ValueError("Colormap name must be a string")

    if isinstance(cmap, colors.Colormap):
        cmap_d[name] = cmap
        return

    # For the remainder, let exceptions propagate.
    if lut is None:
        lut = mpl.rcParams['image.lut']
    cmap = colors.LinearSegmentedColormap(name, data, lut)
    cmap_d[name] = cmap

def get_cmap(name=None, lut=None):
    """
    Get a colormap instance, defaulting to rc values if *name* is None.

    Colormaps added with :func:`register_cmap` take precedence over
    builtin colormaps.

    If *name* is a :class:`colors.Colormap` instance, it will be
    returned.

    If *lut* is not None it must be an integer giving the number of
    entries desired in the lookup table, and *name* must be a
    standard mpl colormap name with a corresponding data dictionary
    in *datad*.
    """
    if name is None:
        name = mpl.rcParams['image.cmap']

    if isinstance(name, colors.Colormap):
        return name

    if name in cmap_d:
        if lut is None:
            return cmap_d[name]
        elif name in datad:
            return colors.LinearSegmentedColormap(name,  datad[name], lut)
        else:
            raise ValueError("Colormap %s is not recognized" % name)

class ScalarMappable:
    """
    This is a mixin class to support scalar -> RGBA mapping.  Handles
    normalization and colormapping
    """

    def __init__(self, norm=None, cmap=None):
        """
        *norm* is an instance of :class:`colors.Normalize` or one of
        its subclasses, used to map luminance to 0-1. *cmap* is a
        :mod:`cm` colormap instance, for example :data:`cm.jet`
        """

        self.callbacksSM = cbook.CallbackRegistry((
                'changed',))

        if cmap is None: cmap = get_cmap()
        if norm is None: norm = colors.Normalize()

        self._A = None
        self.norm = norm
        self.cmap = get_cmap(cmap)
        self.colorbar = None
        self.update_dict = {'array':False}

    def set_colorbar(self, im, ax):
        'set the colorbar image and axes associated with mappable'
        self.colorbar = im, ax

    def to_rgba(self, x, alpha=None, bytes=False):
        """Return a rgba array corresponding to *x*, taking *alpha* and 
        *bytes* into account.
        
        If *x* is a np.ndarray and already an colour array, insert *alpha* if
        of rgb type, else if already rgba, ignore *alpha*.  In all other cases
        normalise and colormap *x*, and insert *alpha* if necessary.
        
        *alpha* is always assumed to be in the [0, 1] scale.
        
        If *bytes* is True, return the rgba array with dtype=np.uint8s in
        scale range [0, 255], else as floats in scale range [0, 1].

        No clipping is perfomed.  Gray conversion is performed if requested
        in rc params (ITU-R 601-2 luma transform).  The operations are
        carried out in float space [0, 1] internally."""

        if alpha is None:
            alpha = np.asarray(1.0)
        else:
            # See __doc__ string:
            alpha = np.asarray(alpha)

        if isinstance(x, np.ndarray) and x.ndim == 3:
            # We are going to process a colour array.
            #
            # We convert to float if given in bytes.
            if x.dtype.kind == 'i':
                input_colour_array = np.asarray(x, dtype=np.float) / 255.0
            else:
                input_colour_array = x

            # Insert alpha if necessary ...

            if x.shape[-1] == 3:
                # We have a rgb array.  Add alpha:
                m, n = input_colour_array.shape[:2]
                rgba = np.empty(shape=(m,n,4))
                rgba[:,:,:3] = input_colour_array
                rgba[:,:,3] = alpha
            elif x.shape[-1] == 4:
                rgba = input_colour_array
            else:
                raise ValueError("can only handle rgb or rgba data")
        
            # Convert to grayscale if requested ...

            rgba = colors.colorConverter.rgba_apply_rc_gray_setting(rgba)

            # Convert to bytes if requested ...

            if bytes:
                output_rgba = (rgba * 255).astype(np.uint8)
            else:
                output_rgba = rgba

            # Finished.
            return output_rgba

        else:
            # If not 3-dimensional, *x* is to be normalised first.
            x = ma.asarray(x)
            x = self.norm(x)
            # We do bytes transform later, this saves full colour precision:
            x = self.cmap(x, alpha=alpha, bytes=False)

            # Process it via this function again to get the desired result:
            return self.to_rgba(x, alpha=alpha, bytes=bytes)

    def set_array(self, A):
        'Set the image array from numpy array *A*'
        self._A = A
        self.update_dict['array'] = True

    def get_array(self):
        'Return the array'
        return self._A

    def get_cmap(self):
        'return the colormap'
        return self.cmap

    def get_clim(self):
        'return the min, max of the color limits for image scaling'
        return self.norm.vmin, self.norm.vmax

    def set_clim(self, vmin=None, vmax=None):
        """
        set the norm limits for image scaling; if *vmin* is a length2
        sequence, interpret it as ``(vmin, vmax)`` which is used to
        support setp

        ACCEPTS: a length 2 sequence of floats
        """
        if (vmin is not None and vmax is None and
                                cbook.iterable(vmin) and len(vmin)==2):
            vmin, vmax = vmin

        if vmin is not None: self.norm.vmin = vmin
        if vmax is not None: self.norm.vmax = vmax
        self.changed()

    def set_cmap(self, cmap):
        """
        set the colormap for luminance data

        ACCEPTS: a colormap or registered colormap name
        """
        cmap = get_cmap(cmap)
        self.cmap = cmap
        self.changed()

    def set_norm(self, norm):
        'set the normalization instance'
        if norm is None: norm = colors.Normalize()
        self.norm = norm
        self.changed()

    def autoscale(self):
        """
        Autoscale the scalar limits on the norm instance using the
        current array
        """
        if self._A is None:
            raise TypeError('You must first set_array for mappable')
        self.norm.autoscale(self._A)
        self.changed()

    def autoscale_None(self):
        """
        Autoscale the scalar limits on the norm instance using the
        current array, changing only limits that are None
        """
        if self._A is None:
            raise TypeError('You must first set_array for mappable')
        self.norm.autoscale_None(self._A)
        self.changed()


    def add_checker(self, checker):
        """
        Add an entry to a dictionary of boolean flags
        that are set to True when the mappable is changed.
        """
        self.update_dict[checker] = False

    def check_update(self, checker):
        """
        If mappable has changed since the last check,
        return True; else return False
        """
        if self.update_dict[checker]:
            self.update_dict[checker] = False
            return True
        return False

    def changed(self):
        """
        Call this whenever the mappable is changed to notify all the
        callbackSM listeners to the 'changed' signal
        """
        self.callbacksSM.process('changed', self)

        for key in self.update_dict:
            self.update_dict[key] = True
