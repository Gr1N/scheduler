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

from datasingletons import Params, Schedule


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

        self._set_fonts_colors()
        self._set_time_date()

    def _on_ok_button_clicked(self, widget):
        """ Handler for okbutton.
        """
        self._save_all()
        self._window.destroy()

    def _save_all(self):
        """ Save all data from window.
        """
        self._save_fonts_colors()
        self._save_time_date()

    def _save_fonts_colors(self):
        """ Save all data from 'Fonts & colors' tab.
        """
        widget = self.get_object('defaultfont')
        Params().set_default_font(widget.get_font_name())

        widget = self.get_object('lecturecolor')
        Params().set_lecture_color(widget.get_color())

        widget = self.get_object('laboratorycolor')
        Params().set_labaratory_color(widget.get_color())

        widget = self.get_object('practicecolor')
        Params().set_practice_color(widget.get_color())

        widget = self.get_object('daycolor')
        Params().set_day_color(widget.get_color())

    def _set_fonts_colors(self):
        """ Set all font and color data from singleton to 'Fonts & colors' tab.
        """
        widget = self.get_object('defaultfont')
        widget.set_font_name(Params().get_default_font())

        widget = self.get_object('lecturecolor')
        widget.set_color(Params().get_lecture_color())

        widget = self.get_object('laboratorycolor')
        widget.set_color(Params().get_laboratory_color())

        widget = self.get_object('practicecolor')
        widget.set_color(Params().get_practice_color())

        widget = self.get_object('daycolor')
        widget.set_color(Params().get_day_color())

    def _save_time_date(self):
        """ Save all data from 'Time & date' tab.
        """
        widget = self.get_object('currweek')
        Schedule().set_current_week(widget.get_text())

        lessons_time = []
        for i in range(8):
            lessons_time.append(
                [
                    '%s:%s' % (
                        self.get_object('l%db1' % (i + 1)).get_text(),
                        self.get_object('l%db2' % (i + 1)).get_text()
                    ),
                    '%s:%s' % (
                        self.get_object('l%de1' % (i + 1)).get_text(),
                        self.get_object('l%de2' % (i + 1)).get_text()
                    )
                ]
            )
        Schedule().set_lessons_time(lessons_time)

    def _set_time_date(self):
        """ Set all time and date data from singleton to 'Time & date' tab.
        """
        widget = self.get_object('currweek')
        widget.set_text(Schedule().get_current_week())

        lessons_time = Schedule().get_lessons_time()
        for i in range(8):
            widget = self.get_object('l%db1' % (i + 1))
            widget.set_text(lessons_time[i][0].split(':')[0])
            widget = self.get_object('l%db2' % (i + 1))
            widget.set_text(lessons_time[i][0].split(':')[1])
            widget = self.get_object('l%de1' % (i + 1))
            widget.set_text(lessons_time[i][1].split(':')[0])
            widget = self.get_object('l%de2' % (i + 1))
            widget.set_text(lessons_time[i][1].split(':')[1])


if __name__ == '__main__':
    print __doc__.strip()
