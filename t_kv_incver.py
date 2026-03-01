import kv_incver as k
import unittest
import datetime
import os
import re

__version__ = '1.01'

build_match_lines = '''BuildVersion='3'
BuildVersion ='3'
BuildVersion = '3'
BuildVersion  =  '3'
  BuildVersion='3'
BuildVersion = '3'  ## Comments'''


class TestKVIncver(unittest.TestCase):

    def test_build_version_update_p01_found_not_found_earlier(self):
        for line in build_match_lines.split('\n'):
            bld_version_found=False
            new_bld_version=''
            line_new, bld_version_found_new, bld_version_old, bld_version_new, new_bld_version_new = k.build_version_update(line, bld_version_found, new_bld_version)
            self.assertTrue(bld_version_found_new)
            self.assertEqual(new_bld_version_new, 'BuildVersion = \'4\'')
            self.assertEqual(bld_version_old, 3)
            self.assertEqual(bld_version_new, 4)
    def test_build_version_update_p02_found_earlier(self):
        for line in build_match_lines.split('\n'):
            bld_version_found=True
            new_bld_version='BuildVersion = \'4\''
            line_new, bld_version_found_new, bld_version_old, bld_version_new, new_bld_version_new = k.build_version_update(line, bld_version_found, new_bld_version)
            self.assertTrue(bld_version_found_new)
            self.assertEqual(new_bld_version_new, 'BuildVersion = \'4\'')
            self.assertEqual(bld_version_old, 3)
            self.assertEqual(bld_version_new, 4)
    def test_build_version_update_p03_found_earlier_different_version(self):
        for line in build_match_lines.split('\n'):
            bld_version_found=True
            new_bld_version='BuildVersion = \'4\''
            # first run to change
            line, bld_version_found, bld_version_old, bld_version_new, new_bld_version = k.build_version_update(line, bld_version_found, new_bld_version)
            # second run to show diffeent line and impact
            line_new, bld_version_found_new, bld_version_old, bld_version_new, new_bld_version_new = k.build_version_update(line, bld_version_found, new_bld_version)
            self.assertTrue(bld_version_found_new)
            self.assertEqual(new_bld_version_new, 'BuildVersion = \'4\'')
            self.assertEqual(bld_version_old, 4)
            self.assertEqual(bld_version_new, 4)
if __name__ == '__main__':
    unittest.main()
