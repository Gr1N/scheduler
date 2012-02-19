#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
preferenceswindow.py - Preferences window for scheduler
Copyright 2012, Grishko Nikita, grin.minsk@gmail.com
"""

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade


class PreferencesWindow(gtk.Builder):
    """ Class view preferences window and do some operations with it.
    """

    def __init__(self, *args):
        """ Class initializer.
        """
        gtk.Builder.__init__(self, *args)
        self.add_from_file('ui-glade/preferenceswindow.glade')

        self._window = self.get_object('preferenceswindow')

        siglans_dict = {
            'on_applybutton_clicked': lambda w: self._save_all(),
            'on_cancelbutton_clicked': lambda w: self._window.destroy(),
            'on_okbutton_clicked': self._on_ok_button_clicked
        }
        self.connect_signals(siglans_dict)

    def _on_ok_button_clicked(self, widget):
        """ Handler for okbutton.
        """
        self._save_all()
        self._window.destroy()

    def _save_all(self):
        """ Save all data from window.
        """
        print 'Saved'


if __name__ == '__main__':
    print __doc__.strip()