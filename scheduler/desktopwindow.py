#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Grishko Nikita <grin.minsk at gmail dot com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
desktopwindow.py - Base window for scheduler
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
