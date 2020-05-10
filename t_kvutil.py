import kvutil
import unittest
import re
import os
import sys
import datetime

# set the module version number
AppVersion = '1.12'


# utility to create/set/update commmand line passed in parameters
def set_argv( position, value ):
    for pos in range(len(sys.argv),position+1):
        sys.argv.append('arg%02d'%pos)
    sys.argv[position] = value
        
# test class
class TestKVUtilFilenames(unittest.TestCase):
    def test_kv_parse_command_line_p01_config_none(self):
        optiondictconfig = { 'test1' : { } }
        set_argv(1,'invalid=invalid') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': None} )
    def test_kv_parse_command_line_p02_config_default(self):
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        set_argv(1,'invalid=invalid') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': 12} )
    def test_kv_parse_command_line_p03_config_set_type_int(self):
        optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
        set_argv(1,'test1=15') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': 15} )
    def test_kv_parse_command_line_p04_config_set_type_float(self):
        optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'float' } }
        set_argv(1,'test1=15') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': 15.0} )
    def test_kv_parse_command_line_p05_config_set_type_bool(self):
        optiondictconfig = { 'test1' : { 'value' : False, 'type' : 'bool' } }
        set_argv(1,'test1=yes') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': True} )
        set_argv(1,'test1=true') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': True} )
        set_argv(1,'test1=1') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': True} )
        set_argv(1,'test1=no') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': False} )
        set_argv(1,'test1=false') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': False} )
        set_argv(1,'test1=0') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': False} )
    def test_kv_parse_command_line_p06_config_set_type_dir(self):
        optiondictconfig = { 'outdir' : { 'type' : 'dir' } }
        set_argv(1,'outdir=c:/temp') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'outdir': 'c:\\temp'} )
    def test_kv_parse_command_line_p07_config_set_type_listr(self):
        optiondictconfig = { 'names' : { 'type' : 'liststr' } }
        set_argv(1,'names=ken,debbie,bob,jill') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'names': ['ken','debbie','bob','jill']} )
    def test_kv_parse_command_line_p08_config_set_type_date(self):
        optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
        set_argv(1,'onlygtdate=01/01/2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
    def test_kv_parse_command_line_p09_config_set_type_date_dashes(self):
        optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
        set_argv(1,'onlygtdate=01-01-2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
    def test_kv_parse_command_line_p10_config_required(self):
        optiondictconfig = { 'test1' : { 'required' : True, 'type' : 'bool' }, 'AppVersion' : { 'value' : '1.01' } }
        set_argv(1,'test1=0') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': False, 'AppVersion' : '1.01'} )
    def test_kv_parse_command_line_f01_config_required_missing(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'required' : True, 'type' : 'bool' }, 'AppVersion' : { 'value' : '1.01' } }
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f02_config_set_type_int_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
            set_argv(1,'test1=ken') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f03_config_set_type_int_bad02(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
            set_argv(1,'test1=True') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f04_config_set_type_int_bad03(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
            set_argv(1,'test1=1.67') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f05_config_set_type_date_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
            set_argv(1,'onlygtdate=01:01:2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f06_config_set_type_bool_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'boolfield' : { 'type' : 'bool' } }
            set_argv(1,'boolfield=01:01:2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f07_config_set_type_float_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'floatfield' : { 'type' : 'float' } }
            set_argv(1,'floatfield=string') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )

    def test_set_when_not_set_p01_key2_not_exist(self):
        self.assertEqual(kvutil.set_when_not_set( { 'key1' : { 'key3' : 'value3'} }, 'key1', 'key2', 'value2' ), True )

    def test_filename_maxmin_p01_pm_forward(self):
        self.assertEqual(kvutil.filename_maxmin( 'kv*.py' ), 'kvcsv.py')
    def test_filename_maxmin_p02_pm_reverse(self):
        self.assertEqual(kvutil.filename_maxmin( 'kv*.py', reverse=True ), 'kvxls.py' )

    def test_filename_split_p01_filename_only(self):
        self.assertEqual(kvutil.filename_split('filename.ext'), ('.','filename', '.ext'))
    def test_filename_split_p02_filename_path(self):
        self.assertEqual(kvutil.filename_split('/path/filename.ext'), (os.path.normpath('/path'),'filename','.ext'))
    def test_filename_split_p03_filename_path_win(self):
        self.assertEqual(kvutil.filename_split(r'\path\filename.ext'), (os.path.normpath('/path'),'filename','.ext'))
    def test_filename_split_p04_filename_path_no_ext(self):
        self.assertEqual(kvutil.filename_split('/path/filename'), (os.path.normpath('/path'),'filename',''))
    def test_filename_split_p05_filename_path_double_ext(self):
        self.assertEqual(kvutil.filename_split('/path/filename.zip.bak'), (os.path.normpath('/path'),'filename.zip','.bak'))
    def test_filename_split_p06_filename_long_path(self):
        self.assertEqual(kvutil.filename_split('/path/path2/path3/path4/filename.ext'), (os.path.normpath('/path/path2/path3/path4'),'filename','.ext'))
    def test_filename_split_p07_filename_blank(self):
        self.assertEqual(kvutil.filename_split(''), (os.path.normpath(''),'',''))

    def test_filename_list_p01_simple_filename(self):
        self.assertEqual(kvutil.filename_list( 'ken.txt', None, None ), ['ken.txt']) 
    def test_filename_list_p02_simple_filename_path(self):
        self.assertEqual(kvutil.filename_list( 'ken/ken.txt', None, None ), ['ken/ken.txt']) 
    def test_filename_list_p03_simple_filename_nopath(self):
        self.assertEqual(kvutil.filename_list( 'ken/ken.txt', None, None, strippath=True ), ['ken.txt']) 
    def test_filename_list_p04_simple_filelist(self):
        self.assertEqual(kvutil.filename_list( None, ['ken.txt','ken2.txt'], None, None ), ['ken.txt','ken2.txt']) 
    def test_filename_list_p05_simple_filename_filelist(self):
        self.assertEqual(kvutil.filename_list( 'ken3.txt', ['ken.txt','ken2.txt'], None, None ), ['ken.txt','ken2.txt','ken3.txt']) 
    def test_filename_list_p06_simple_fileglob(self):
        self.assertEqual(kvutil.filename_list( None, None, 'kvcsv.*', None ), ['kvcsv.py']) 
    def test_filename_list_p06_simple_fileglob_dir(self):
        self.assertEqual(kvutil.filename_list( None, None, '..\\tools\\kvcsv.*', None ), ['..\\tools\\kvcsv.py']) 
    def test_filename_list_p06_simple_fileglob_dir_notpath(self):
        self.assertEqual(kvutil.filename_list( None, None, '..\\tools\\kvcsv.*', True ), ['kvcsv.py']) 


    def test_file_proper_p01_simple_filename(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt' ), os.path.normpath('./ken.txt') )
    def test_file_proper_p02_abspath_filename(self):
        self.assertEqual(kvutil.filename_proper( os.environ.get('USERPROFILE')+'/Dropbox/LinuxShare/PerlPlay/templates/ken.txt' ), os.path.normpath( os.environ.get('USERPROFILE')+'/Dropbox/LinuxShare/PerlPlay/templates/ken.txt') )
    def test_file_proper_p03_relpath_filename(self):
        self.assertEqual(kvutil.filename_proper( '../../PerlPlay/templates/ken.txt' ), os.path.normpath('../../PerlPlay/templates/ken.txt') )
    def test_file_proper_p04_filename_dir(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', dir='./' ), os.path.normpath('./ken.txt') )
    def test_file_proper_p05_filename_dir_write_check(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', dir='./', write_check=True ), os.path.normpath('./ken.txt') )
    def test_file_proper_p06_filename_dir_create_dir(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', dir='./createdir', create_dir=True ), os.path.normpath('./createdir/ken.txt') )
        os.rmdir('./createdir')  #remove folder that was created
    def test_file_proper_p07_filename_dir_create_absdir(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', dir='c:/createdir/level2', create_dir=True ), os.path.normpath('c:/createdir/level2/ken.txt') )
        os.rmdir('c:/createdir/level2')  #remove folder that was created
        os.rmdir('c:/createdir')  #remove folder that was created
    def test_file_proper_f01_abspath_filename(self):
        with self.assertRaises(Exception) as context:
            kvutil.filename_proper( 'C:/Users/ken/Dropbox/LinuxShare/PerlPlay/templates/missingdir/ken.txt' )
        #self.assertTrue('This is broken' in context.exception)

    def test_filename_unique_p01_filename(self):
        self.assertEqual(kvutil.filename_unique('uniquefname.txt'), os.path.normpath('./uniquefname.txt'))
    def test_filename_unique_po2_filedict_datecnt(self):
        re_file = re.compile('t_kvcsvtest-\d+v\d+\.csv')
        self.assertTrue(re_file.match(kvutil.filename_unique( { 'base_filename' : 't_kvcsvtest', 'file_ext' : '.csv', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )))
    def test_filename_unique_po3_filedict_cnt(self):
        self.assertEqual(kvutil.filename_unique( { 'base_filename' : 't_kvcsvtest', 'file_ext' : '.csv', 'overwrite' : True, 'forceuniq' : True } ), 't_kvcsvtestv01.csv')
    def test_filename_unique_p04_filename_exists(self):
        self.assertEqual(kvutil.filename_unique('kev_tsv.pm'), os.path.normpath('./kev_tsvv01.pm'))
        

    def test_slurp_p01_simple(self):
        filename  = 't_kvutil_slurp_test.txt'
        fullstr = ''
        # build the file to be read in
        with open( filename, 'w' ) as t:
            for line in range(0,5):
                linestr = str(line) + '\n'
                fullstr += linestr
                t.write(linestr)
        # now read in the filen and validate it matches expectations
        self.assertEqual(kvutil.slurp(filename), fullstr)
        # now remove the temporary file
        kvutil.remove_filename(filename)

    def test_read_list_from_file_lines_p01_simple(self):
        filename  = 't_kvutil_RLFF_test.txt'
        fulllist = []
        # build the file to be read in
        with open( filename, 'w' ) as t:
            for line in range(0,5):
                linestr = str(line) + '\n'
                fulllist.append(linestr.strip('\n'))
                t.write(linestr)
        # now read in the filen and validate it matches expectations
        self.assertEqual(kvutil.read_list_from_file_lines(filename), fulllist)
        # now remove the temporary file
        kvutil.remove_filename(filename)
    def test_read_list_from_file_lines_p02_stripblank(self):
        filename  = 't_kvutil_RLFF_test.txt'
        fulllist = []
        # build the file to be read in
        with open( filename, 'w' ) as t:
            maxiter = 3
            for i in range(3):
                for line in range(0,maxiter):
                    linestr = str(line + i*maxiter) + '\n'
                    fulllist.append(linestr.strip('\n'))
                    t.write(linestr)
                # inject blank lines
                for line in range(2):
                    t.write('\n')
        # now read in the filen and validate it matches expectations
        self.assertEqual(kvutil.read_list_from_file_lines(filename, stripblank=True), fulllist)
        # now remove the temporary file
        kvutil.remove_filename(filename)


    def test_datetime_from_str_p01_zero_padded(self):
        self.assertEqual(kvutil.datetime_from_str('01/01/19'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvutil.datetime_from_str('01/01/2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvutil.datetime_from_str('01-01-19'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvutil.datetime_from_str('01-01-2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvutil.datetime_from_str('2019-01-01'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvutil.datetime_from_str('20190101'), datetime.datetime(2019, 1, 1) )

    def test_datetime_from_str_p02_notzero_padded(self):
        self.assertEqual(kvutil.datetime_from_str('1/1/19'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvutil.datetime_from_str('1/1/2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvutil.datetime_from_str('1-1-19'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvutil.datetime_from_str('1-1-2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvutil.datetime_from_str('2019-1-1'), datetime.datetime(2019, 1, 1) )

    def test_datetime_from_str_f01_invalid_date(self):
        with self.assertRaises(Exception) as context:
            kvutil.datetime_from_str('20/1/19')

    def test_datetime_from_str_f02_no_matching_format(self):
        with self.assertRaises(Exception) as context:
            kvutil.datetime_from_str('1/1/20019')

        


if __name__ == '__main__':
    unittest.main()
