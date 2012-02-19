#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
aboutwindow.py - About window for scheduler
Copyright 2012, Grishko Nikita, grin.minsk@gmail.com
"""

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade


class AboutWindow(gtk.Builder):
    """ Class shows information about scheduler.
    """

    def __init__(self, *args):
        """ Class initializer.
        """
        gtk.Builder.__init__(self, *args)
        self.add_from_file('ui-glade/aboutscheduler.glade')

        about = self.get_object('aboutscheduler')
        about.run()
        about.hide()


if __name__ == '__main__':
    print __doc__.strip()
