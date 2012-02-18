#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
desktopwindow.py - Base window for scheduler
Copyright 2012, Grishko Nikita, grin.minsk@gmail.com
"""

import pygtk
pygtk.require('2.0')
import gtk
import cairo


class DesktopWindow(gtk.Window):
    """ A transparent and borderless window, fixed on the desktop.
    """

    def __init__(self, *args):
        """ Class initialiser.
        """
        gtk.Window.__init__(self, *args)

        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
        self.set_keep_below(True)
        self.set_decorated(False)
        self.stick()

        screen = self.get_screen()
        rgba = screen.get_rgba_colormap()
        self.set_colormap(rgba)
        self.set_app_paintable(True)
        self.connect('expose-event', self._transparent_expose)

    def _transparent_expose(self, widget, event):
        """ Make the given widget transparent.
        """
        cr = widget.window.cairo_create()
        cr.set_operator(cairo.OPERATOR_CLEAR)
        region = gtk.gdk.region_rectangle(event.area)
        cr.region(region)
        cr.fill()
        return False


if __name__ == '__main__':
    print __doc__.strip()
