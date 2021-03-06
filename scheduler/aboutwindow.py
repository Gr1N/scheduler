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
aboutwindow.py - About window for scheduler
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
