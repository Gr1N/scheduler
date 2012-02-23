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
datasingletons.py - Params and SQL singletons for scheduler
"""

import os.path
import shelve
import pygtk
pygtk.require('2.0')
import gtk
from datetime import date


def _singleton(cls):
    """ Singleton instance.
    """
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


def _check_app_dir():
    """ Chech directory at ~/.config/scheduler
    and if directory not exists, create it.
    """
    if not os.path.exists(os.path.expanduser('~/.config/scheduler')):
        os.mkdir(os.path.expanduser('~/.config/scheduler'))


@_singleton
class Params:
    """ Params singleton include all variables and operations
    who works with scheduler settings.
    """

    def __init__(self):
        """ Class initializer.
        """
        _check_app_dir()
        if os.path.exists(os.path.expanduser('~/.config/scheduler/params')):
            self._use_existing_params()
        else:
            self._use_default_params()

    def _use_default_params(self):
        """ Initialize default params and save it.
        """
        self.params = {
            # Desktop window params
            'pos': (100, 100),
            'lock_pos': False,
            # Font params
            'default_font': 'Sans 12',
            # Colors params
            'lecture_color': '#009566660000',
            'laboratory_color': '#987600000000',
            'practice_color': '#188820eda89b',
            'day_color': '#000000000000',
            # View schedule settings
            'view_sch': [True] * 6
        }
        self.save_params()

    def _use_existing_params(self):
        """ Initialize params from file.
        """
        sh = shelve.open(os.path.expanduser('~/.config/scheduler/params'))
        self.params = sh['params']
        sh.close()

    def save_params(self):
        """ Save params dict to file.
        """
        sh = shelve.open(os.path.expanduser('~/.config/scheduler/params'))
        sh['params'] = self.params
        sh.close()

    def get_pos(self):
        """ Get window position.
        """
        return self.params['pos']

    def set_pos(self, pos):
        """ Set wondow position.
        """
        self.params['pos'] = pos
        self.save_params()

    def get_lock_pos(self):
        """ Get lock_pos flag.
        """
        return self.params['lock_pos']

    def set_lock_pos(self, lock_pos):
        """ Set lock_pos flag.
        """
        self.params['lock_pos'] = lock_pos
        self.save_params()

    def get_default_font(self):
        """ Get default font.
        """
        return self.params['default_font']

    def set_default_font(self, font):
        """ Set default font.
        """
        self.params['default_font'] = font

    def get_lecture_color(self):
        """ Get lecture color.
        """
        return gtk.gdk.Color(self.params['lecture_color'])

    def set_lecture_color(self, color):
        """ Set lecture color.
        """
        self.params['lecture_color'] = str(color)

    def get_laboratory_color(self):
        """ Get laboratory color.
        """
        return gtk.gdk.Color(self.params['laboratory_color'])

    def set_labaratory_color(self, color):
        """ Set laboratory color.
        """
        self.params['laboratory_color'] = str(color)

    def get_practice_color(self):
        """ Get practice color.
        """
        return gtk.gdk.Color(self.params['practice_color'])

    def set_practice_color(self, color):
        """ Set practice color.
        """
        self.params['practice_color'] = str(color)

    def get_day_color(self):
        """ Get day color.
        """
        return gtk.gdk.Color(self.params['day_color'])

    def set_day_color(self, color):
        """ Set day color.
        """
        self.params['day_color'] = str(color)

    def get_view_sch(self):
        """ Get scheduler view settings.
        """
        return self.params['view_sch']

    def set_view_sch(self, view_sch):
        """ Set scheduler view settings.
        """
        self.params['view_sch'] = view_sch


@_singleton
class Schedule:
    """ DataBase singleton inlude all variables and operations
    who works with schedule in database.
    """

    def __init__(self):
        """ Class initializer.
        """
        _check_app_dir()
        if os.path.exists(os.path.expanduser('~/.config/scheduler/schedule')):
            self._use_existing_schedule()
            self.update_current_week()
        else:
            self._use_default_schedule()

    def _use_default_schedule(self):
        """ Initialize default schedule and save it.
        """
        gen_day = lambda: [[[-1, '', -1, '', '']] * 8] * 4
        self.schedule = {
            'current_week': [1, date.today().isocalendar()[1]],
            'lessons_time': [
                ['8:00', '9:35'],
                ['9:45', '11:20'],
                ['11:40', '13:15'],
                ['13:25', '15:00'],
                ['15:20', '16:55'],
                ['17:05', '18:40'],
                ['18:45', '20:20'],
                ['20:25', '22:00']
            ],
            'schedule': {
                'Monday': gen_day(),
                'Thuesday': gen_day(),
                'Wednesday': gen_day(),
                'Thursday': gen_day(),
                'Friday': gen_day(),
                'Saturday': gen_day()
            },
            'subgroup': -1
        }
        self.save_schedule()

    def _use_existing_schedule(self):
        """ Load existing schedule from file.
        """
        sh = shelve.open(os.path.expanduser('~/.config/scheduler/schedule'))
        self.schedule = sh['schedule']
        sh.close()

    def save_schedule(self):
        """ Save params dict to file.
        """
        sh = shelve.open(os.path.expanduser('~/.config/scheduler/schedule'))
        sh['schedule'] = self.schedule
        sh.close()

    def update_current_week(self):
        """ Update current week. Week range: 1-4.
        """
        if self.schedule['current_week'][1] != date.today().isocalendar()[1]:
            cw = self.schedule['current_week'][0]
            for i in range(date.today().isocalendar()[1] -
                           self.schedule['current_week'][1]):
                if cw != 4:
                    cw += 1
                else:
                    cw = 1
            self.schedule['current_week'] = [cw, date.today().isocalendar()[1]]

    def get_current_week(self):
        """ Get current week.
        """
        return self.schedule['current_week'][0]

    def set_current_week(self, week):
        """ Set current week.
        """
        self.schedule['current_week'] = [week, date.today().isocalendar()[1]]

    def get_lessons_time(self):
        """ Get lessons time.
        """
        return self.schedule['lessons_time']

    def set_lessons_time(self, lessons_time):
        """ Set lessons time.
        """
        self.schedule['lessons_time'] = lessons_time

    def get_schedule(self, day, week):
        """ Get schedule by day and week.
        """
        return self.schedule['schedule'][day][week]

    def set_schedule(self, day, week, schedule):
        """ Set schedule by day and week.
        """
        self.schedule['schedule'][day][week] = schedule

    def get_subgroup(self):
        """ Get num of subgroup.
        """
        return self.schedule['subgroup']

    def set_subgroup(self, subgroup):
        """ Set num of subgroup.
        """
        self.schedule['subgroup'] = subgroup


if __name__ == '__main__':
    print __doc__.strip()
