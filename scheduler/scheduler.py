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
scheduler.py - Main file for scheduler app, contains main class for widget that
shows schedule. The program is based on the idea of displaying the schedule of
the student studying in Belarusian State University of Informatics and
Radioelectronics (BSUIR).
"""

import pygtk
pygtk.require('2.0')
import gtk
import sys
import multiprocessing
import time

from desktopwindow import DesktopWindow
from schedulermenu import SchedulerMenu
from datasingletons import Params, Schedule


class Scheduler:
    """ Widget, which shows a schedule on your desktop.
    """

    def __init__(self):
        """ Class initialiser.
        """
        self.window = DesktopWindow()

        self._initialize_settings()
        self._initialize_table()
        self._initialize_menu()

        self.window.show_all()

        pr = multiprocessing.Process(target=self._update_schedule, args=(60,))
        pr.daemon = True
        pr.start()

    def _initialize_settings(self):
        """ Initialize schedule settings.
        """
        pos = Params().get_pos()
        self.window.move(pos[0], pos[1])
        self.is_moving = False

        self.window.connect('button-release-event',
            self._button_release_event)
        self.window.connect('motion-notify-event',
            self._button_move_event)
        self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON_MOTION_MASK)

    def _initialize_table(self):
        """ Initialize gtk.Table() for view schedule.
        """
        self.table = gtk.Table()
        self.table.set_col_spacings(8)
        self.table.set_row_spacings(3)
        self.window.add(self.table)
        self._view_schedule()
        self.table.show()

    def _view_schedule(self):
        """ Insert labels with schedule information to table.
        """
        def plus_top_attach(f):

            def plus(*args, **kwargs):
                top_attach, left_attach = f(*args, **kwargs)
                return top_attach + 1, left_attach + 1

            return plus

        @plus_top_attach
        def create_label(text, left_attach, right_attach,
                         top_attach, bottom_attach, align=None):
            label = gtk.Label('<span font="%s">%s</span>' %
                              (Params().get_default_font(), text))
            label.set_use_markup(True)
            if align == 'left':
                label.set_alignment(xalign=0.0, yalign=0.5)
            elif align == 'right':
                label.set_alignment(xalign=1.0, yalign=0.5)
            self.table.attach(label, left_attach, right_attach,
                top_attach, bottom_attach, xoptions=gtk.FILL, yoptions=False)
            label.show()
            return top_attach, left_attach

        @plus_top_attach
        def create_separator(left_attach, right_attach,
                             top_attach, bottom_attach):
            separator = gtk.HSeparator()
            self.table.attach(separator, left_attach, right_attach,
                top_attach, bottom_attach, xoptions=gtk.FILL, yoptions=False)
            separator.show()
            return top_attach, left_attach

        tattach, tlen, view_sch = 0, 0, Params().get_view_sch()
        for i in view_sch:
            if i:
                tlen += 1
        for day in ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday']:
            tattach = create_label('<b><span color="%s">%s</span></b>' %
                                   (Params().get_day_color(), day), 0, tlen,
                tattach, tattach + 1, 'left')[0]
            tattach = create_separator(0, tlen, tattach, tattach + 1)[0]

            schedule = Schedule().get_schedule(day,
                Schedule().get_current_week() - 1)
            for i in range(8):
                if not schedule[i][1] == '' and \
                   (schedule[i][0] == Schedule().get_subgroup() or
                       schedule[i][0] == 2):
                    if not schedule[i][2]:
                        label_color = '%s' % str(Params().get_lecture_color())
                    elif schedule[i][2] == 1:
                        label_color = '%s' % \
                                      str(Params().get_laboratory_color())
                    elif schedule[i][2] == 2:
                        label_color = '%s' % str(Params().get_practice_color())
                    else:
                        label_color = '%s' % str(Params().get_non_color())

                    label_template = '<span color="%s">%s</span>'
                    lattach = 0
                    if view_sch[0]:
                        lattach = create_label('<span color="%s">%d.</span>' %
                                               (label_color, i),
                            lattach, lattach + 1, tattach, tattach + 1)[1]
                    if view_sch[1]:
                        lattach = create_label(label_template % (label_color,
                            '-'.join(Schedule().get_lessons_time()[i])),
                            lattach, lattach + 1, tattach, tattach + 1)[1]
                    if view_sch[2]:
                        lattach = create_label(label_template %
                                               (label_color, schedule[i][1]),
                            lattach, lattach + 1,
                            tattach, tattach + 1, 'left')[1]
                    if view_sch[3]:
                        lattach = create_label(label_template %
                                               (label_color, schedule[i][3]),
                            lattach, lattach + 1, tattach, tattach + 1)[1]
                    if view_sch[4]:
                        create_label(label_template %
                                     (label_color, schedule[i][4]),
                            lattach, lattach + 1,
                            tattach, tattach + 1, 'right')
                    tattach += 1

    def _update_schedule(self, interval):
        """ Subprocess function. Check for num of week,
        if it changed, then update schedule view.
        """
        while True:
            if Schedule().update_current_week():
                self._view_schedule()
                print 'Yes'
            time.sleep(interval)

    def _initialize_menu(self):
        """ Initialize scheduler menu.
        """
        menu = SchedulerMenu()

        self.window.connect_object('button-press-event',
            self._button_press_event, menu)

    def _button_press_event(self, widget, event):
        """ Buttons press handler.
        """
        if event.button == 1 and not Params().get_lock_pos():
            self.is_moving = True
        elif event.button == 3:
            widget.popup(None, None, None, event.button, event.time)
        return True

    def _button_release_event(self, widget, event):
        """ Buttons release handler.
        """
        if event.button == 1 and not Params().get_lock_pos():
            self.is_moving = False
            Params().set_pos(self.window.get_position())
        return True

    def _button_move_event(self, widget, event):
        """ Buttons move handler.
        """
        if self.is_moving and not Params().get_lock_pos():
            self.window.move(int(event.x_root), int(event.y_root))  # FIX: fix moving
        return True


def main():
    Scheduler()
    print 'Scheduler is running.\nLook at your desktop!'
    try:
        gtk.main()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
