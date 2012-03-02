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
excelparser.py - Excel files parser for scheduler
"""

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import xlrd

from datasingletons import Schedule


class ExcelParser:
    """ Class contains file chooser and parser for excel files.
    """

    def __init__(self):
        """ Class initializer.
        """
        dialog = gtk.FileChooserDialog("Open..", None,
            gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL,
                                           gtk.RESPONSE_CANCEL,
                                           gtk.STOCK_OPEN,
                                           gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("Microsoft Excel")
        filter.add_mime_type("application/vnd.ms-excel")
        filter.add_pattern("*.xls")
        filter.add_pattern("*.xlsx")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            try:
                self._parse_excel_file(dialog.get_filename())
                Schedule().save_schedule()
            except xlrd.biffh.XLRDError, e:
                print e
                builder = gtk.Builder()
                builder.add_from_file('ui-glade/excelparsererrordialog.glade')
                erdialog = builder.get_object('excelparsererrordialog')
                erdialog.run()
                erdialog.hide()

        dialog.destroy()

    def _parse_excel_file(self, filename):
        """ Parse excel file and put data to 'Schedule' singleton.
        """
        book = xlrd.open_workbook(filename)
        sheet = book.sheet_by_index(0)

        def get_day(day):
            if day == 'пн':
                return 'Monday'
            elif day == 'вт':
                return 'Tuesday'
            elif day == 'ср':
                return 'Wednesday'
            elif day == 'чт':
                return 'Thursday'
            elif day == 'пт':
                return 'Friday'
            elif day == 'сб':
                return 'Saturday'

        def get_weeks(weeks):
            if weeks == '':
                return [0, 1, 2, 3]
            else:
                weeks = weeks.split(',')
                for i in range(len(weeks)):
                    weeks[i] = int(weeks[i]) - 1
                return weeks

        def get_lesson_index(unknown_time):
            times = Schedule().get_lessons_time()
            unknown_time = unknown_time.split('-')[0]
            for time in times:
                if unknown_time in time:
                    return times.index(time)

        def get_subgroup(subgroup):
            if subgroup == '':
                return 2
            else:
                return int(subgroup) - 1

        def get_type(ltype):
            if ltype == 'лк':
                return 0
            elif ltype == 'лр':
                return 1
            elif ltype == 'пз':
                return 2
            elif ltype == '':
                return -1

        schedule = Schedule().get_all_schedule()
        for currentRow in range(3, sheet.nrows):
            if get_subgroup(sheet.cell_value(currentRow, 3)) == \
               Schedule().get_subgroup() or \
               get_subgroup(sheet.cell_value(currentRow, 3)) == 2:
                day = get_day(sheet.cell_value(currentRow, 0))
                lesson_index = get_lesson_index(sheet.cell_value(
                    currentRow, 2))
                for week in get_weeks(sheet.cell_value(currentRow, 1)):
                    schedule[day][week][lesson_index] = [
                        get_subgroup(sheet.cell_value(currentRow, 3)),
                        sheet.cell_value(currentRow, 4),
                        get_type(sheet.cell_value(currentRow, 5)),
                        sheet.cell_value(currentRow, 6),
                        sheet.cell_value(currentRow, 7)
                    ]
        Schedule().set_all_schedule(schedule)


if __name__ == '__main__':
    print __doc__.strip()
