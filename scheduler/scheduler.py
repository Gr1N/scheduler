#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import sys

from desktopwindow import DesktopWindow
from schedulermenu import SchedulerMenu
from datasingletons import Params


class Scheduler:
    """ Widget, which shows a schedule into your desktop
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

    def _initialize_gui(self):  # TODO: make schedule view
        """ Initialize GUI for view schedule.
        """
        box = gtk.HBox()
        self.window.add(box)

        label = gtk.Label('Schedule')
        box.pack_start(label, expand=True)

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
