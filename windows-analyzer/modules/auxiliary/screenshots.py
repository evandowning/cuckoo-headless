# Copyright (C) 2012-2013 Claudio Guarnieri.
# Copyright (C) 2014-2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import logging
import StringIO
import threading
import time
import os

from lib.api.screenshot import Screenshot
from lib.common.abstracts import Auxiliary
from lib.common.results import NetlogFile

log = logging.getLogger(__name__)

SHOT_DELAY = 1

# Skip the following area when comparing screen shots.
# Example for 800x600 screen resolution.
# SKIP_AREA = ((735, 575), (790, 595))
SKIP_AREA = None

class Screenshots(threading.Thread, Auxiliary):
    """Take screenshots."""

    def __init__(self, options={}, analyzer=None):
        threading.Thread.__init__(self)
        Auxiliary.__init__(self, options, analyzer)
        self.do_run = True

    def stop(self):
        """Stop screenshotting."""
        self.do_run = False

    def run(self):
        """Run screenshotting.
        @return: operation status.
        """
        if "screenshots" in self.options:
            self.do_run = int(self.options["screenshots"])

        scr = Screenshot()

        # TODO We should also send the action "pillow" so that the Web
        # Interface can adequately inform the user about this missing library.
        if not scr.have_pil():
            log.info(
                "Python Image Library (either PIL or Pillow) is not "
                "installed, screenshots are disabled."
            )
            return False

        img_counter = 0
        img_last = None

        while self.do_run:
            time.sleep(SHOT_DELAY)

            try:
                img_current = scr.take()
            except IOError as e:
                log.error("Cannot take screenshot: %s", e)
                continue

            if img_last and scr.equal(img_last, img_current, SKIP_AREA):
                continue

            img_counter += 1

            # workaround as PIL can't write to the socket file object :(
            tmpio = StringIO.StringIO()
            img_current.save(tmpio, format="JPEG")
            tmpio.seek(0)

            # evan - instead of uploading it, store it in the stuff folder
            f = os.path.join(os.getcwd(),'stuff','shots')
            if not os.path.exists(f):
                os.makedirs(f)

            upload_path = os.path.join(f,'{0}.jpg'.format(img_counter))
            with open(upload_path,'wb') as fw:
                for chunk in tmpio:
                    fw.write(chunk)
            
            # now upload to host from the StringIO
#           nf = NetlogFile()
#           nf.init("shots/%04d.jpg" % img_counter)

#           for chunk in tmpio:
#               nf.sock.sendall(chunk)

#           nf.close()

            img_last = img_current

        return True
