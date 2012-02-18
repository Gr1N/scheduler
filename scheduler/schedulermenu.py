#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
schedulermenu.py - Drop menu for scheduler
Copyright 2012, Grishko Nikita, grin.minsk@gmail.com
"""

import pygtk
pygtk.require('2.0')
import gtk

from aboutwindow import AboutWindow
from datasingletons import Params


class SchedulerMenu(gtk.Menu):
    """ Drop menu for scheduler desktop window.
    """

    def __init__(self, *args):
        """ Class initializer.
        """
        gtk.Menu.__init__(self, *args)
        self._initialize_menu_items()

    def _initialize_menu_items(self):
        """ Initialize menu items.
        """
        menu_item = gtk.CheckMenuItem('Lock window position')
        menu_item.set_active(Params().get_lock_pos())
        menu_item.connect('activate',
            lambda e: Params().set_lock_pos(False)
                if Params().get_lock_pos() is True
                else Params().set_lock_pos(True))
        self.append(menu_item)
        menu_item.show()

        menu_item = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
        self.append(menu_item)
#        menu_item.connect()  # TODO: add connect to preferences window
        menu_item.show()

        menu_item = gtk.SeparatorMenuItem()
        self.append(menu_item)
        menu_item.show()

        menu_item = gtk.ImageMenuItem(gtk.STOCK_HELP)
        self.append(menu_item)
        menu_item.connect('activate', lambda e: AboutWindow())
        menu_item.show()

        menu_item = gtk.SeparatorMenuItem()
        self.append(menu_item)
        menu_item.show()

        menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.append(menu_item)
        menu_item.connect('activate', lambda e: gtk.main_quit())
        menu_item.show()


if __name__ == '__main__':
    print __doc__.strip()
