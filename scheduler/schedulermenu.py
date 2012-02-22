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
schedulermenu.py - Drop menu for scheduler
"""

import pygtk
pygtk.require('2.0')
import gtk

from aboutwindow import AboutWindow
from preferenceswindow import PreferencesWindow
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
        menu_item.connect('activate', lambda e: PreferencesWindow())
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
