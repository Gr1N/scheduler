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
        self._initialize_gui()
        self._initialize_menu()

        self.window.show_all()

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

    def _initialize_gui(self):  # TODO: add auto update
        """ Initialize GUI for view schedule.
        """
        table = gtk.Table()
        table.set_col_spacings(8)
        table.set_row_spacings(3)
        self.window.add(table)

        def plus_top_attach(f):

            def plus(*args, **kwargs):
                to_plus = f(*args, **kwargs)
                return to_plus + 1

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
            table.attach(label, left_attach, right_attach,
                top_attach, bottom_attach, xoptions=gtk.FILL, yoptions=False)
            label.show()
            return top_attach

        @plus_top_attach
        def create_separator(left_attach, right_attach,
                             top_attach, bottom_attach):
            separator = gtk.HSeparator()
            table.attach(separator, left_attach, right_attach,
                top_attach, bottom_attach, xoptions=gtk.FILL, yoptions=False)
            separator.show()
            return top_attach

        attach = 0
        for day in ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday']:
            attach = create_label('<b><span color="%s">%s</span></b>' %
                                  (Params().get_day_color(), day), 0, 5,
                attach, attach + 1, 'left')
            attach = create_separator(0, 5, attach, attach + 1)

            schedule = Schedule().get_schedule(day,
                Schedule().get_current_week() - 1)
            for i in range(8):
                if not schedule[i][1] == '' and \
                   (schedule[i][0] == Schedule().get_subgroup() or
                       schedule[i][0] == 2):
                    label_color = ''
                    if not schedule[i][2]:
                        label_color = '%s' % str(Params().get_lecture_color())
                    elif schedule[i][2] == 1:
                        label_color = '%s' % \
                                      str(Params().get_laboratory_color())
#                    elif schedule[i][2] == 2:
                    else:  # FIX: need color when lesson without type
                        label_color = '%s' % str(Params().get_practice_color())

                    label_template = '<span color="%s">%s</span>'
                    create_label('<span color="%s">%d.</span>' %
                                 (label_color, i),
                        0, 1, attach, attach + 1)
                    create_label(label_template % (label_color,
                        '-'.join(Schedule().get_lessons_time()[i])),
                        1, 2, attach, attach + 1)
                    create_label(label_template %
                                 (label_color, schedule[i][1]),
                        2, 3, attach, attach + 1, 'left')
                    create_label(label_template %
                                 (label_color, schedule[i][3]),
                        3, 4, attach, attach + 1)
                    attach = create_label(label_template %
                                          (label_color, schedule[i][4]),
                        4, 5, attach, attach + 1, 'right')

        table.show()

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
    print 'Scheduler is running.\nLook at your desktop!'
    instance = Scheduler()
    try:
        gtk.main()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
