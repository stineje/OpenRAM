#!/usr/bin/env python2.7
"""
Run a regresion test on a 4 bank SRAM
"""

import unittest
from header import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()

#@unittest.skip("SKIPPING 20_sram_test")


class sram_4bank_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import sram

        debug.info(1, "Testing sample 8bit, 128word SRAM, 4 banks")
        a = sram.sram(word_size=8, num_words=128, num_banks=4, name="test_sram1")
        OPTS.check_lvsdrc = True
        self.local_check(a)

    def local_check(self, a):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        a.sp_write(tempspice)
        a.gds_write(tempgds)

        self.assertFalse(calibre.run_drc(a.name, tempgds))
        self.assertFalse(calibre.run_lvs(a.name, tempgds, tempspice))
        #self.assertFalse(calibre.run_pex(a.name, tempgds, tempspice, output=OPTS.openram_temp+"temp_pex.sp"))

        os.remove(tempspice)
        os.remove(tempgds)

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
