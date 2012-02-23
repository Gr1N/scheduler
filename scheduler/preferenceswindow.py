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
preferenceswindow.py - Preferences window for scheduler
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
            'on_okbutton_clicked': self._on_ok_button_clicked,
            'on_weekday_changed': self._on_weekday_changed,
            'on_weeknum_changed': self._on_weeknum_changed
        }
        self.connect_signals(siglans_dict)

        self._set_fonts_colors()
        self._set_time_date()
        self._set_schedule_day('Monday', 0)

    def _on_ok_button_clicked(self, widget):
        """ Handler for okbutton.
        """
        self._save_all()
        self._window.destroy()

    def _on_weekday_changed(self, widget):
        """ Handler for weekday spinbutton.
        """
        self._set_schedule_day(
            widget.get_active_text(),
            self.get_object('weeknum').get_active()
        )

    def _on_weeknum_changed(self, widget):
        """ Handler for weeknum spinbutton.
        """
        self._set_schedule_day(
            self.get_object('weekday').get_active_text(),
            widget.get_active()
        )

    def _save_all(self):
        """ Save all data from window.
        """
        self._save_fonts_colors()
        self._save_time_date()
        self._save_schedule_day()

    def _save_fonts_colors(self):
        """ Save all data from 'Fonts & colors' tab to 'Params' singleton.
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
        """ Set all font and color data from 'Params' singleton
        to 'Fonts & colors' tab.
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
        """ Save all data from 'Time & date' tab to 'Schedule' singleton.
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
        """ Set all time and date data from 'Schedule' singleton
        to 'Time & date' tab.
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

    def _save_schedule_day(self):
        """ Save all data about active day from 'Schedule' tab
        to 'Schedule' singleton.
        """
        schedule = []
        for i in range(8):
            schedule.append(
                [
                    self.get_object('l%dsub' % (i + 1)).get_active(),
                    self.get_object('l%dname' % (i + 1)).get_text(),
                    self.get_object('l%dtype' % (i + 1)).get_active(),
                    self.get_object('l%dclass' % (i + 1)).get_text(),
                    self.get_object('l%dlector' % (i + 1)).get_text()
                ]
            )
        Schedule().set_schedule(
            self.get_object('weekday').get_active_text(),
            self.get_object('weeknum').get_active(),
            schedule
        )

    def _set_schedule_day(self, day, week):
        """ Set all data about active day from 'Schedule' singleton
        to 'Schedule' tab.
        """
        schedule = Schedule().get_schedule(day, week)
        for i in range(8):
            self.get_object('l%dsub' % (i + 1)).set_active(schedule[i][0])
            self.get_object('l%dname' % (i + 1)).set_text(schedule[i][1])
            self.get_object('l%dtype' % (i + 1)).set_active(schedule[i][2])
            self.get_object('l%dclass' % (i + 1)).set_text(schedule[i][3])
            self.get_object('l%dlector' % (i + 1)).set_text(schedule[i][4])


if __name__ == '__main__':
    print __doc__.strip()
