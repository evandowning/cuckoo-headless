# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2016 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import ctypes
import logging

from lib.common.defines import KERNEL32, SYSTEMTIME
from lib.common.results import NetlogHandler

log = logging.getLogger()

def init_logging():
    """Initialize logger."""
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")

    # evan: log to both console and to file
    logfn = os.path.join(os.getcwd(),'stuff','analysis.log')
   
    fileHandler = logging.FileHandler(logfn)
    fileHandler.setFormatter(formatter)
    log.addHandler(fileHandler)
   
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    log.addHandler(consoleHandler)

# evan: not needed anymore
#   nh = NetlogHandler()
#   nh.setFormatter(formatter)
#   log.addHandler(nh)

    log.setLevel(logging.DEBUG)

def set_clock(clock):
    st = SYSTEMTIME()
    st.wYear = clock.year
    st.wMonth = clock.month
    st.wDay = clock.day
    st.wHour = clock.hour
    st.wMinute = clock.minute
    st.wSecond = clock.second
    st.wMilliseconds = 0
    KERNEL32.SetLocalTime(ctypes.byref(st))
