__author__ = 'rautahir'

import logging

def createlogger(name, level=None):
    l = logging.getLogger(name)
    l.handlers = []
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter("%(levelname)s %(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(message)s")
    log_handler.setFormatter(log_formatter)
    l.addHandler(log_handler)
    if (level):
        l.setLevel(level)
    l.propagate = False
    return l