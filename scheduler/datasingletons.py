#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
datasingletons.py - Params and SQL singletons for scheduler
Copyright 2012, Grishko Nikita, grin.minsk@gmail.com
"""

import os.path
import shelve


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
        self.params = {'pos': (100, 100),
                       'lock_pos': False}
        self._save_params()

    def _use_existing_params(self):
        """ Initialize params from file.
        """
        sh = shelve.open(os.path.expanduser('~/.config/scheduler/params'))
        self.params = sh['params']
        sh.close()

    def _save_params(self):
        """ Save params dict ti file.
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
        self._save_params()

    def get_lock_pos(self):
        """ Get lock_pos flag.
        """
        return self.params['lock_pos']

    def set_lock_pos(self, lock_pos):
        """ Set lock_pos flag.
        """
        self.params['lock_pos'] = lock_pos
        self._save_params()


@_singleton
class DataBase:
    """ DataBase singleton inlude all variables and operations
    who works with schedule in database.
    """
    pass


if __name__ == '__main__':
#    print Params().get_pos()
    print __doc__.strip()
