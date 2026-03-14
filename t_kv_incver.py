import kv_incver as k
import kvutil
import unittest
import datetime
import os
import re

__version__ = '1.01'

# input build version data set that has different ways the string can be found
build_match_lines = '''BuildVersion='3'
BuildVersion ='3'
BuildVersion = '3'
BuildVersion  =  '3'
  BuildVersion='3'
BuildVersion = '3'  ## Comments'''

UPDATEDBUILDVERSION = 'BuildVersion = \'4\''
OLDBUILDVERSION = 3
NEWBUILDVERSION = 4


major_minor_match_lines_version = '''__version__ = \'1.2\'
__version__=\'1.2\'
__version__    =    \'1.2\'
__version__=\'1.2\'    ## comments'''

major_minor_match_lines_appversion = '''AppVersion = \'1.2\'
AppVersion=\'1.2\'
AppVersion    =    \'1.2\''''


major_minor_match_lines_at_version = '''@version : 1.2
@version:1.2
@version :1.2
@version    :    1.2
@version:1.2    ## comments'''

major_minor_match_lines_at_version_quote = '''@version : \'1.2\'
@version:\'1.2\'
@version :\'1.2\'
@version    :    \'1.2\'
@version:\'1.2\'    ## comments'''

major_minor_match_lines_optversion = '''\'AppVersion\': {
\'AppVersion' : {
\'AppVersion':{
\'AppVersion':{  '''

major_minor_match_lines_optvalue = '''    \'value\': \'1.2\',
    \'value' : \'1.2\',
    \'value' : \'1.2\' ,
        \'value': \'1.2\',
        \'value': \'1.2\' ,
    \'value' : \'1.2\',  # comments'''



OLDAPPVERSIONMINOR = '1.2'
NEWAPPVERSIONMINOR = '1.03'

file_create_test_lines = '''__version__ = '1.2'
@version: 1.2
@version: \'1.2\'
AppVersion = \'1.2\''''

file_create_header_lines = '''

# test file header

'''
file_create_footer_lines = '''
BuildVersion = \'9\'
# footer lines
# more footer lines
# eof
'''

class TestKVIncver(unittest.TestCase):

    def test_build_version_update_p01_found_not_found_earlier(self):
        # for each line type - we find one instance of the buildversion line and update it
        # and we HAVE NEVER seen a buildversoin line before
        # so new_bld_version is passed in as an empty
        for line in build_match_lines.split('\n'):
            bld_version_found=False
            new_bld_version=''
            line_new, bld_version_found_new, bld_version_old, bld_version_new, new_bld_version_new = k.build_version_update(line, bld_version_found, new_bld_version)
            self.assertTrue(line_new, line.replace('3', '4'))
            self.assertTrue(bld_version_found_new)
            self.assertEqual(bld_version_old, OLDBUILDVERSION)
            self.assertEqual(bld_version_new, NEWBUILDVERSION)
            self.assertEqual(new_bld_version_new, UPDATEDBUILDVERSION)
    def test_build_version_update_p02_found_earlier(self):
        # for each line type - we find one instance of the buildversion line and update it
        # and we HAVE seen a buildversoin line before
        # so new_bld_version is passed in as the prior found value
        for line in build_match_lines.split('\n'):
            bld_version_found=True
            new_bld_version=UPDATEDBUILDVERSION
            line_new, bld_version_found_new, bld_version_old, bld_version_new, new_bld_version_new = k.build_version_update(line, bld_version_found, new_bld_version)
            self.assertTrue(line_new, line.replace('3', '4'))
            self.assertTrue(bld_version_found_new)
            self.assertEqual(bld_version_old, OLDBUILDVERSION)
            self.assertEqual(bld_version_new, NEWBUILDVERSION)
            self.assertEqual(new_bld_version_new, UPDATEDBUILDVERSION)
    def test_build_version_update_p03_found_earlier_different_version(self):
        for line in build_match_lines.split('\n'):
            bld_version_found=True
            new_bld_version=UPDATEDBUILDVERSION
            # first run to change
            line, bld_version_found, bld_version_old, bld_version_new, new_bld_version = k.build_version_update(line, bld_version_found, new_bld_version)
            # second run to show diffeent line and impact
            line_new, bld_version_found_new, bld_version_old, bld_version_new, new_bld_version_new = k.build_version_update(line, bld_version_found, new_bld_version)
            self.assertTrue(line_new, line.replace('3', '4'))
            self.assertTrue(bld_version_found_new)
            self.assertEqual(bld_version_old, NEWBUILDVERSION)
            self.assertEqual(bld_version_new, NEWBUILDVERSION)
            self.assertEqual(new_bld_version_new, UPDATEDBUILDVERSION)
    def test_build_version_update_p04_not_found_not_found_earlier(self):
        line = 'Not a line that should match'
        bld_version_found=False
        new_bld_version=''
        # first run to change
        line_new, bld_version_found_new, bld_version_old, bld_version_new, new_bld_version_new = k.build_version_update(line, bld_version_found, new_bld_version)
        self.assertTrue(line_new, line)
        self.assertFalse(bld_version_found_new)
        self.assertEqual(bld_version_new, None)
        self.assertEqual(bld_version_old, None)
        self.assertEqual(new_bld_version_new, new_bld_version)
    def test_build_version_update_p04_not_found_found_earlier(self):
        line = 'Not a line that should match'
        bld_version_found=True
        new_bld_version=UPDATEDBUILDVERSION
        # first run to change
        line_new, bld_version_found_new, bld_version_old, bld_version_new, new_bld_version_new = k.build_version_update(line, bld_version_found, new_bld_version)
        self.assertTrue(line_new, line)
        self.assertTrue(bld_version_found_new)
        self.assertEqual(bld_version_new, None)
        self.assertEqual(bld_version_old, None)
        self.assertEqual(new_bld_version_new, new_bld_version)


    def test_major_minor_version_update_p01__match_version_found__version__(self):
        for line in major_minor_match_lines_version.split('\n'):
            version_found = True
            opt_ver_found = False  ## we did not previously find a opt_ver_found values
            new_app_ver = NEWAPPVERSIONMINOR
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)
            
    def test_major_minor_version_update_p02__match_version_found_at_version(self):
        for line in major_minor_match_lines_at_version.split('\n'):
            version_found = True
            opt_ver_found = False  ## we did not previously find a opt_ver_found values
            new_app_ver = NEWAPPVERSIONMINOR
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)
                                                                                        
    def test_major_minor_version_update_p03__match_optversion_found(self):
        for line in major_minor_match_lines_optversion.split('\n'):
            version_found = True
            opt_ver_found = False
            new_app_ver = NEWAPPVERSIONMINOR

            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertTrue(opt_ver_found_new)
            self.assertFalse(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)
                                                                                        
            
    def test_major_minor_version_update_p04__match_optvalue_found(self):
        for line in major_minor_match_lines_optvalue.split('\n'):
            version_found = True
            opt_ver_found = True
            new_app_ver = NEWAPPVERSIONMINOR
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)
                                                                                        
            
    def test_major_minor_version_update_p05__match_version_found_next_line(self):
        for line in major_minor_match_lines_optvalue.split('\n'):
            version_found = True
            opt_ver_found = True
            new_app_ver = NEWAPPVERSIONMINOR

            line_between = "    'notall': True,"
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line_between, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertTrue(opt_ver_found_new)
            self.assertFalse(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)
                                                                                        
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)

    def test_major_minor_version_update_p06__match_appversion_found__version__(self):
        for line in major_minor_match_lines_appversion.split('\n'):
            version_found = True
            opt_ver_found = False  ## we did not previously find a opt_ver_found values
            new_app_ver = NEWAPPVERSIONMINOR
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)

    def test_major_minor_version_update_p11__match_version_not_found_version__(self):
        for line in major_minor_match_lines_version.split('\n'):
            version_found = False
            opt_ver_found = False  ## we did not previously find a opt_ver_found values
            new_app_ver = ''
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)

    def test_major_minor_version_update_p12__match_version_not_foundat_version(self):
        for line in major_minor_match_lines_at_version.split('\n'):
            version_found = False
            opt_ver_found = False  ## we did not previously find a opt_ver_found values
            new_app_ver = ''
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)
                                                                                        
    def test_major_minor_version_update_p13__match_optversion_not_found(self):
        for line in major_minor_match_lines_optversion.split('\n'):
            version_found = False
            opt_ver_found = False
            new_app_ver = ''

            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertFalse(version_found_new)
            self.assertTrue(opt_ver_found_new)
            self.assertFalse(version_changed_new)
            self.assertEqual(new_app_ver_new, '')
                                                                                        
            
    def test_major_minor_version_update_p14__match_optvalue_not_found(self):
        for line in major_minor_match_lines_optvalue.split('\n'):
            version_found = False
            opt_ver_found = True
            new_app_ver = ''
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)
                                                                                        
            
    def test_major_minor_version_update_p15__match_version_not_found_next_line(self):
        for line in major_minor_match_lines_optvalue.split('\n'):
            version_found = False
            opt_ver_found = True
            new_app_ver = ''

            line_between = "    'notall': True,"
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line_between, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertFalse(version_found_new)
            self.assertTrue(opt_ver_found_new)
            self.assertFalse(version_changed_new)
            self.assertEqual(new_app_ver_new, '')
                                                                                        
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)

    def test_major_minor_version_update_p16__match_appversion_not_found__version__(self):
        for line in major_minor_match_lines_appversion.split('\n'):
            version_found = False
            opt_ver_found = False  ## we did not previously find a opt_ver_found values
            new_app_ver = ''
            
            line_new, version_found_new, opt_ver_found_new, new_app_ver_new, version_changed_new = k.major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, debug=False)

            self.assertTrue(version_found_new)
            self.assertFalse(opt_ver_found_new)
            self.assertTrue(version_changed_new)
            self.assertEqual(new_app_ver_new, NEWAPPVERSIONMINOR)

    def test_calc_new_app_ver_p01_major(self):
        m = re.search(r'(((\d+)\.(\d+)))', NEWAPPVERSIONMINOR)
        new_app_ver = k.calc_new_app_ver(m, True)
        self.assertEqual(new_app_ver, '2.01')
        
    def test_calc_new_app_ver_p02_minor(self):
        m = re.search(r'(((\d+)\.(\d+)))', NEWAPPVERSIONMINOR)
        new_app_ver = k.calc_new_app_ver(m, False)
        self.assertEqual(new_app_ver, '1.04')
        
    def test_calc_new_app_ver_p03_minor_large(self):
        m = re.search(r'(((\d+)\.(\d+)))', '1.99')
        new_app_ver = k.calc_new_app_ver(m, False)
        self.assertEqual(new_app_ver, '1.100')
        
    def test_calc_new_app_ver_p04_major_large(self):
        m = re.search(r'(((\d+)\.(\d+)))', '1.99')
        new_app_ver = k.calc_new_app_ver(m, True)
        self.assertEqual(new_app_ver, '2.01')
        

    def test_update_file_version_p01_minor_app(self):
        for line in file_create_test_lines.split('\n'):
            # create a file to be updated
            file_tmp = 'kvincver_test.txt'
            with open(file_tmp, 'w') as f:
                f.write(file_create_header_lines)
                f.write(line)
                f.write(file_create_footer_lines)
                new_file_expected_content = file_create_header_lines + line.replace('1.2', '1.03') + file_create_footer_lines
            major_update=False
            build_only=False
            test=False
            debug=False
            # call the routine
            appVer, newAppVer, filename, file_bak, bldVer, newBldVer = k.update_file_version(file_tmp, major_update, build_only, test, debug)

            # self.assertEqual(appVer, '1.2')
            self.assertEqual(newAppVer, '1.03')
            self.assertEqual(filename, file_tmp)
            self.assertEqual(bldVer, '')
            self.assertEqual(newBldVer, '')

            # read in the file and validate
            file_content = kvutil.slurp(file_tmp)
            self.assertEqual(file_content, new_file_expected_content)
            
            # remove the temp file
            kvutil.remove_filename(file_tmp)
            
    def test_update_file_version_p01_major_app(self):
        for line in file_create_test_lines.split('\n'):
            # create a file to be updated
            file_tmp = 'kvincver_test.txt'
            with open(file_tmp, 'w') as f:
                f.write(file_create_header_lines)
                f.write(line)
                f.write(file_create_footer_lines)
                new_file_expected_content = file_create_header_lines + line.replace('1.2', '2.01') + file_create_footer_lines
            major_update=True
            build_only=False
            test=False
            debug=False
            # call the routine
            appVer, newAppVer, filename, file_bak, bldVer, newBldVer = k.update_file_version(file_tmp, major_update, build_only, test, debug)

            # self.assertEqual(appVer, '1.2')
            self.assertEqual(newAppVer, '2.01')
            self.assertEqual(filename, file_tmp)
            self.assertEqual(bldVer, '')
            self.assertEqual(newBldVer, '')

            # read in the file and validate
            file_content = kvutil.slurp(file_tmp)
            self.assertEqual(file_content, new_file_expected_content)
            
            # remove the temp file
            kvutil.remove_filename(file_tmp)
            
    def test_update_file_version_p01_buildversion_app(self):
        for line in file_create_test_lines.split('\n'):
            # create a file to be updated
            file_tmp = 'kvincver_test.txt'
            with open(file_tmp, 'w') as f:
                f.write(file_create_header_lines)
                f.write(line)
                f.write(file_create_footer_lines)
                new_file_expected_content = file_create_header_lines + line + file_create_footer_lines.replace('9', '10')
            major_update=False
            build_only=True
            test=False
            debug=False
            # call the routine
            appVer, newAppVer, filename, file_bak, bldVer, newBldVer = k.update_file_version(file_tmp, major_update, build_only, test, debug)

            # self.assertEqual(appVer, '1.2')
            self.assertEqual(newAppVer, '')
            self.assertEqual(bldVer, '9')
            self.assertEqual(newBldVer, '10')
            self.assertEqual(filename, file_tmp)

            # read in the file and validate
            file_content = kvutil.slurp(file_tmp)
            self.assertEqual(file_content, new_file_expected_content)
            
            # remove the temp file
            kvutil.remove_filename(file_tmp)
            

if __name__ == '__main__':
    unittest.main()
