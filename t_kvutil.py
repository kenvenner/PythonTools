import kvutil
import unittest
import re
import os
import sys
import datetime
import json


# logging
import kvlogger
config=kvlogger.get_config('t_kvutil.log')
kvlogger.dictConfig(config)
logger=kvlogger.getLogger(__name__)

# set the module version number
AppVersion = '1.19'

# global variables
tst_filename='t_kvutil_tst'
tst_ext_range=4
tst_day = datetime.datetime.today().day
tst_path = '.' + os.path.sep
tst_log_fmt_file='{}{:02d}.log'
tst_log_fmt_fullfile='{}{}{:02d}.log'
tst_prepend='pre-'
tst_append='-post'

# utility to create/set/update commmand line passed in parameters
def set_argv( position, value ):
    for pos in range(len(sys.argv),position+1):
        sys.argv.append('arg%02d'%pos)
    sys.argv[position] = value

def generate_test_filenames( startfilename='t_kvutil_tst', ext_range=4):
    fname_list = []
    for i in range(ext_range):
        fname_list.append('{}.{:03d}'.format(startfilename, i))

    return fname_list

def file_teardown(  startfilename='t_kvutil_tst', ext_range=4):
    logger.info('removing files from startfilename:%s:ext_range:%d', startfilename,ext_range)
    for fname in generate_test_filenames( startfilename, ext_range ):
        if os.path.exists(fname):
            os.remove(fname)

def file_setup(  startfilename='t_kvutil_tst', ext_range=4):
    logger.info('creating files from startfilename:%s:ext_range:%d', startfilename, ext_range)
    for fname in generate_test_filenames( startfilename, ext_range ):
        if not os.path.exists(fname):
            with open( fname, 'w' ) as t:
                pass
        

        
# test class
class TestKVUtilFilenames(unittest.TestCase):
    # set up features
    @classmethod
    def setUpClass(cls):
        file_setup( tst_filename, tst_ext_range )

    # tear down features
    @classmethod
    def tearDownClass(cls):
        file_teardown( tst_filename, tst_ext_range )


    # command line parsing
    def test_kv_parse_command_line_p01_config_none(self):
        optiondictconfig = { 'test1' : { } }
        set_argv(1,'invalid=invalid') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': None} )
    def test_kv_parse_command_line_p02_config_default(self):
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        set_argv(1,'invalid=invalid') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': 12} )
    def test_kv_parse_command_line_p03_config_set_type_bool(self):
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
    def test_kv_parse_command_line_p04_config_set_type_int(self):
        optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
        set_argv(1,'test1=15') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': 15} )
    def test_kv_parse_command_line_p05_config_set_type_float(self):
        optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'float' } }
        set_argv(1,'test1=15.25') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': 15.25} )
        set_argv(1,'test1=-15.25') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': -15.25} )
        set_argv(1,'test1=15') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': 15.0} )
        set_argv(1,'test1=.001') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': 0.001} )
    def test_kv_parse_command_line_p06_config_set_type_dir(self):
        optiondictconfig = { 'outdir' : { 'type' : 'dir' } }
        set_argv(1,'outdir=c:/temp') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'outdir': 'c:\\temp'} )
    def test_kv_parse_command_line_p07_config_set_type_listr(self):
        optiondictconfig = { 'names' : { 'type' : 'liststr' } }
        set_argv(1,'names=ken,debbie,bob,jill') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'names': ['ken','debbie','bob','jill']} )
        set_argv(1,'names=ken') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'names': ['ken']} )
    def test_kv_parse_command_line_p08_config_set_type_date_slashes(self):
        optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
        set_argv(1,'onlygtdate=01/01/2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=1/1/2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=01/01/19') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
    def test_kv_parse_command_line_p09_config_set_type_date_dashes(self):
        optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
        set_argv(1,'onlygtdate=01-01-2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=1-1-2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=01-01-19') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
    def test_kv_parse_command_line_p10_config_set_type_date_YMD(self):
        optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
        set_argv(1,'onlygtdate=2019-01-01') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=20190101') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'onlygtdate': datetime.datetime(2019,1,1)} )
    def test_kv_parse_command_line_p11_config_set_type_inlist(self):
        optiondictconfig = { 'log_level' : { 'inlist' : 'date', 'valid' : ['DEBUG','INFO','WARNING','ERROR','CRITICAL'] } }
        set_argv(1,'log_level=DEBUG') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'log_level': 'DEBUG'} )
    def test_kv_parse_command_line_p12_config_required(self):
        optiondictconfig = { 'test1' : { 'required' : True, 'type' : 'bool' }, 'AppVersion' : { 'value' : '1.01' } }
        set_argv(1,'test1=0') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'test1': False, 'AppVersion' : '1.01'} )
    def test_kv_parse_command_line_p13_config_default_config_setting(self):
        optiondictconfig = { 'AppVersion' : { 'value' : '1.01' } }
        set_argv(1,'log_level=DEBUG') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'log_level': 'DEBUG', 'AppVersion' : '1.01'} )
    def test_kv_parse_command_line_p14_config_keymapdict(self):
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        keymapdict = { 'invalid' : 'test1' }
        set_argv(1,'invalid=invalid') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, keymapdict=keymapdict ), {'test1' : 'invalid'} )
    def test_kv_parse_command_line_p15_config_conf_json_cmdline_single(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        set_argv(1,'conf_json=t_kvutil.json') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'conf_json': ['t_kvutil.json'], 'test1' : 'conf_json_loaded'} )
        kvutil.remove_filename('t_kvutil.json')
    def test_kv_parse_command_line_p16_config_conf_json_cmdline_multiple(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        conf_json= { 'test2' : 'conf_json_loaded' }
        with open('t_kvutil2.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 }, 'test2' : { 'value' : 12 } }
        set_argv(1,'conf_json=t_kvutil.json,t_kvutil2.json') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'conf_json': ['t_kvutil.json', 't_kvutil2.json'], 'test1' : 'conf_json_loaded', 'test2' : 'conf_json_loaded'} )
        kvutil.remove_filename('t_kvutil.json')
        kvutil.remove_filename('t_kvutil2.json')
    def test_kv_parse_command_line_p17_config_conf_json_optiondictconfig_single_list(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 }, 'conf_json' : { 'value' : ['t_kvutil.json'] }, 'set_cmd' : {} }
        set_argv(1,'set_cmd=cmd') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'conf_json': ['t_kvutil.json'], 'test1' : 'conf_json_loaded', 'set_cmd' : 'cmd'} )
        kvutil.remove_filename('t_kvutil.json')
    def test_kv_parse_command_line_p18_config_conf_json_optiondictconfig_single_value(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 }, 'conf_json' : { 'value' : 't_kvutil.json' }, 'set_cmd' : {}}
        set_argv(1,'set_cmd=cmd') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'conf_json': ['t_kvutil.json'], 'test1' : 'conf_json_loaded', 'set_cmd' : 'cmd'} )
        kvutil.remove_filename('t_kvutil.json')
    def test_kv_parse_command_line_p19_config_conf_json_optiondictconfig_multiple_list(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        conf_json= { 'test2' : 'conf_json_loaded' }
        with open('t_kvutil2.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 }, 'test2' : { 'value' : 12 }, 'conf_json' : { 'value' : ['t_kvutil.json', 't_kvutil2.json'] }, 'set_cmd' : {}}
        set_argv(1,'set_cmd=cmd') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'conf_json': ['t_kvutil.json', 't_kvutil2.json'], 'test1' : 'conf_json_loaded', 'test2' : 'conf_json_loaded', 'set_cmd' : 'cmd'} )
        kvutil.remove_filename('t_kvutil.json')
        kvutil.remove_filename('t_kvutil2.json')
    def test_kv_parse_command_line_p20_config_conf_json_optiondictconfig_multiple_list_valoverride(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        conf_json= { 'test1' : 'value_override' }
        with open('t_kvutil2.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 }, 'conf_json' : { 'value' : ['t_kvutil.json', 't_kvutil2.json'] }, 'set_cmd' : {}}
        set_argv(1,'set_cmd=cmd') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'conf_json': ['t_kvutil.json', 't_kvutil2.json'], 'test1' : 'value_override', 'set_cmd' : 'cmd'} )
        kvutil.remove_filename('t_kvutil.json')
        kvutil.remove_filename('t_kvutil2.json')
    def test_kv_parse_command_line_p21_config_conf_json_cmdline_override(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        set_argv(1,'conf_json=t_kvutil.json') # push value onto command line (string)
        set_argv(2,'test1=cmdline_loaded') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig ), {'conf_json': ['t_kvutil.json'], 'test1' : 'cmdline_loaded'} )
        kvutil.remove_filename('t_kvutil.json')

    def test_kv_parse_command_line_f01_config_required_missing(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'required' : True, 'type' : 'bool' }, 'AppVersion' : { 'value' : '1.01' } }
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f02_config_set_type_bool_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'boolfield' : { 'type' : 'bool' } }
            set_argv(1,'boolfield=01:01:2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f03_config_set_type_int_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
            set_argv(1,'test1=ken') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f04_config_set_type_int_bad02(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
            set_argv(1,'test1=True') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f05_config_set_type_int_bad03(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
            set_argv(1,'test1=1.67') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f06_config_set_type_float_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'floatfield' : { 'type' : 'float' } }
            set_argv(1,'floatfield=string') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f07_config_set_type_float_bad02(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'floatfield' : { 'type' : 'float' } }
            set_argv(1,'floatfield=2019-01-01') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f08_config_set_type_date_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
            set_argv(1,'onlygtdate=01:01:2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f09_config_set_type_date_bad02(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
            set_argv(1,'onlygtdate=13-01-2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f10_config_set_type_date_bad03(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
            set_argv(1,'onlygtdate=12-32-2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f11_config_set_type_date_bad04(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
            set_argv(1,'onlygtdate=string') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f12_config_set_type_inlist_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'AppVersion' : { 'value' : '1.01' } }
            set_argv(1,'log_level=NOTINLIST') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f12_config_set_type_inlist_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'no_valid_defined' : { 'value' : '1.01', 'type' : 'inlist' } }
            set_argv(1,'no_valid_defined=fail') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )
    def test_kv_parse_command_line_f13_config_raise_error_unknown_value(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'valid_defined' : { 'value' : '1.01' } }
            set_argv(1,'no_valid_defined=fail') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, raise_error=True )
    def test_kv_parse_command_line_f14_config_missing_conf_json(self):
        with self.assertRaises(Exception) as context:
            kvutil.remove_filename('t_kvutil.json')
            optiondictconfig = { 'test1' : { 'value' : 12 } }
            set_argv(1,'conf_json=t_kvutil.json') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig )

    # hashmap setting
    def test_set_when_not_set_p01_key2_not_exist(self):
        self.assertEqual(kvutil.set_when_not_set( { 'key1' : { 'key3' : 'value3'} }, 'key1', 'key2', 'value2' ), True )

    # logfile filename
    def test_filename_log_day_of_month_p01_simple(self):
        self.assertEqual(kvutil.filename_log_day_of_month( tst_filename+'.log' ), tst_log_fmt_file.format(tst_filename, tst_day))
    def test_filename_log_day_of_month_p02_fullfilename(self):
        self.assertEqual(kvutil.filename_log_day_of_month( tst_path+tst_filename+'.log' ), tst_log_fmt_fullfile.format(tst_path, tst_filename, tst_day))
    def test_filename_log_day_of_month_p03_ext_override_without_dot(self):
        self.assertEqual(kvutil.filename_log_day_of_month( tst_filename+'.bak', ext_override='log' ), tst_log_fmt_file.format(tst_filename, tst_day))
    def test_filename_log_day_of_month_p04_ext_override_with_dot(self):
        self.assertEqual(kvutil.filename_log_day_of_month( tst_filename+'.bak', ext_override='.log' ), tst_log_fmt_file.format(tst_filename, tst_day))
    def test_filename_log_day_of_month_p05_path_override(self):
        self.assertEqual(kvutil.filename_log_day_of_month( 'badpath/'+tst_filename+'.log', path_override=tst_path), tst_log_fmt_fullfile.format(tst_path, tst_filename, tst_day))
    def test_filename_log_day_of_month_p06_path_override_no_slash(self):
        self.assertEqual(kvutil.filename_log_day_of_month( 'badpath/'+tst_filename+'.log', path_override='.'), tst_log_fmt_fullfile.format(tst_path, tst_filename, tst_day))
    def test_filename_log_day_of_month_p07_current_file_exists_key(self):
        logfile=kvutil.filename_log_day_of_month( tst_filename+'.log' )
        with open( logfile, 'w' ) as t:
            pass
        self.assertTrue( os.path.exists(logfile) )
        kvutil.remove_filename(logfile)
    def test_filename_log_day_of_month_p08_historical_file_exists_remove(self):
        logfile=kvutil.filename_log_day_of_month( tst_filename+'.log' )
        with open( logfile, 'w' ) as t:
            pass
        self.assertTrue( os.path.exists(logfile) )
        stinfo = os.stat(logfile)
        newmtime = stinfo.st_mtime - 60*60*25 # more than a day ago
        os.utime(logfile, (newmtime, newmtime))
        logfile=kvutil.filename_log_day_of_month( tst_filename+'.log' )
        self.assertTrue( not os.path.exists(logfile) )
        kvutil.remove_filename(logfile)
        
    
    # min/max filename
    def test_filename_maxmin_p01_forward(self):
        self.assertEqual(kvutil.filename_maxmin( tst_filename+'*' ), '{}.{:03d}'.format(tst_filename, 0))
    def test_filename_maxmin_p02_reverse(self):
        self.assertEqual(kvutil.filename_maxmin(  tst_filename+'*', reverse=True ), '{}.{:03d}'.format(tst_filename, range(tst_ext_range)[-1]) )
    def test_filename_maxmin_p03_nofiles(self):
        self.assertEqual(kvutil.filename_maxmin( 'no'+tst_filename+'*' ), None)


    # filename_create 
    def test_filename_create_p01_simple(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log' ), os.path.normpath('/test/' + tst_filename+'.log'))
    def test_filename_create_p02_path_blank(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log', path_blank=True ),  os.path.normpath(tst_filename+'.log'))
    def test_filename_create_p03_filename_ext(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log', filename_ext='bak' ), os.path.normpath('/test/' + tst_filename+'.bak'))
    def test_filename_create_p04_filename_ext_with_dot(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log', filename_ext='.bak' ), os.path.normpath('/test/' + tst_filename+'.bak'))
    def test_filename_create_p05_filename_base(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log', filename_base='newbasefilename' ), os.path.normpath('/test/' + 'newbasefilename' + '.log'))
    def test_filename_create_p06_filename_path(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log', filename_path='/newpath/' ), os.path.normpath('/newpath/' + tst_filename+'.log'))
    def test_filename_create_p07_filename_path_no_slash(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log', filename_path='/newpath' ), os.path.normpath('/newpath/' + tst_filename+'.log'))
    def test_filename_create_p08_blank_filename(self):
        self.assertEqual(kvutil.filename_create( '', filename_path='/test/', filename_base=tst_filename, filename_ext='.log' ), os.path.normpath('/test/' + tst_filename+'.log'))
    def test_filename_create_p09_none_filename(self):
        self.assertEqual(kvutil.filename_create( None, filename_path='/test/', filename_base=tst_filename, filename_ext='.log' ), os.path.normpath('/test/' + tst_filename+'.log'))
    def test_filename_create_p10_filename_not_passed_in(self):
        self.assertEqual(kvutil.filename_create( filename_path='/test/', filename_base=tst_filename, filename_ext='.log' ), os.path.normpath('/test/' + tst_filename+'.log'))
    def test_filename_create_p01_simple_prepend(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log', filename_base_prepend=tst_prepend ), os.path.normpath('/test/' + tst_prepend + tst_filename+'.log'))
    def test_filename_create_p01_simple_append(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log', filename_base_append=tst_append ), os.path.normpath('/test/' + tst_filename + tst_append + '.log'))
    def test_filename_create_p01_simple_pre_append(self):
        self.assertEqual(kvutil.filename_create( '/test/' + tst_filename+'.log', filename_base_append=tst_append, filename_base_prepend=tst_prepend ), os.path.normpath('/test/' + tst_prepend+tst_filename+tst_append+'.log'))


    # filename split
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

    #filename splitall

    
    # filename list
    def test_filename_list_p01_simple_filename(self):
        self.assertEqual(kvutil.filename_list( 'ken.txt', None, None ), ['ken.txt']) 
    def test_filename_list_p02_simple_filename_nopath(self):
        self.assertEqual(kvutil.filename_list( 'ken.txt', None, None, strippath=True ), ['ken.txt']) 
    def test_filename_list_p03_simple_pathfilename_path(self):
        self.assertEqual(kvutil.filename_list( 'ken/ken.txt', None, None ), ['ken/ken.txt']) 
    def test_filename_list_p04_simple_pathfilename_nopath(self):
        self.assertEqual(kvutil.filename_list( 'ken/ken.txt', None, None, strippath=True ), ['ken.txt']) 
    def test_filename_list_p05_simple_filenamelist(self):
        self.assertEqual(kvutil.filename_list( None, ['ken.txt','ken2.txt'], None ), ['ken.txt','ken2.txt']) 
    def test_filename_list_p06_simple_filename_filenamelist(self):
        self.assertEqual(kvutil.filename_list( 'ken3.txt', ['ken.txt','ken2.txt'], None ), ['ken.txt','ken2.txt','ken3.txt']) 
    def test_filename_list_p07_simple_pathfilenamelist_path(self):
        self.assertEqual(kvutil.filename_list( None, ['ken/ken.txt','ken2/ken2.txt'], None ), ['ken/ken.txt','ken2/ken2.txt']) 
    def test_filename_list_p08_simple_pathfilenamelist_nopath(self):
        self.assertEqual(kvutil.filename_list( None, ['ken/ken.txt','ken2/ken2.txt'], None, strippath=True ), ['ken.txt','ken2.txt']) 
    def test_filename_list_p09_simple_pathfilename_filenamelist_path(self):
        self.assertEqual(kvutil.filename_list( 'a/ken3.txt', ['b/ken.txt','c/ken2.txt'], None ), ['a/ken3.txt','b/ken.txt','c/ken2.txt']) 
    def test_filename_list_p10_simple_fileglob(self):
        self.assertEqual(kvutil.filename_list( None, None, 'kvutil.*' ), ['kvutil.py'] ) 
    def test_filename_list_p11_simple_fileglob_dir(self):
        self.assertEqual(kvutil.filename_list( None, None, '..\\tools\\kvutil.*' ), ['..\\tools\\kvutil.py']) 
    def test_filename_list_p12_simple_fileglob_dir_notpath(self):
        self.assertEqual(kvutil.filename_list( None, None, '..\\tools\\kvutil.*', strippath=True ), ['kvutil.py']) 
    def test_filename_list_p13_list_excludelist_from_file(self):
        fnamelist='t_kvutil_inc.lst'
        with open(fnamelist, 'w') as out:
            out.write('ken.txt\nken1.txt\nken4.txt\n')
        self.assertEqual(kvutil.filename_list( 'ken.txt', ['ken1.txt','ken2.txt'], None, False, excludelist_filename=fnamelist ), ['ken2.txt'])
        kvutil.remove_filename( fnamelist,'test_filename_list_p09_list_excludelist_from_file' )
    def test_filename_list_p14_list_excludelist_from_file_path(self):
        fnamelist='t_kvutil_inc.lst'
        with open(fnamelist, 'w') as out:
            out.write('a/ken.txt\nb/ken1.txt\nd/ken4.txt\n')
        self.assertEqual(kvutil.filename_list( 'a/ken.txt', ['b/ken1.txt','c/ken2.txt'], None, False, excludelist_filename=fnamelist ), ['c/ken2.txt'])
        kvutil.remove_filename( fnamelist,'test_filename_list_p09_list_excludelist_from_file' )
    def test_filename_list_p15_list_includelist_from_file(self):
        fnamelist='t_kvutil_inc.lst'
        with open(fnamelist, 'w') as out:
            out.write('ken.txt\nken1.txt\nken2.txt\n')
        self.assertEqual(kvutil.filename_list( 'ken.txt', None, False, includelist_filename=fnamelist ), ['ken.txt','ken1.txt','ken2.txt'])
        kvutil.remove_filename( fnamelist,'test_filename_list_p10_list_includelist_from_file' )

    def test_filename_list_p16_simple_filename_and_list(self):
        self.assertEqual(kvutil.filename_list( 'ken.txt', ['ken1.txt','ken2.txt'], None, None ), ['ken.txt','ken1.txt','ken2.txt']) 
    def test_filename_list_p17_simple_filename_and_list_dups(self):
        self.assertEqual(kvutil.filename_list( 'ken.txt', ['ken.txt','ken1.txt','ken2.txt'], None, None ), ['ken.txt','ken1.txt','ken2.txt']) 
    def test_filename_list_p18_simple_filename_and_list_nopath(self):
        self.assertEqual(kvutil.filename_list( 'ken.txt', ['ken1.txt','ken2.txt'], None, True ), ['ken.txt','ken1.txt','ken2.txt']) 
    def test_filename_list_p19_simple_filename_and_list_path(self):
        self.assertEqual(kvutil.filename_list( '../ken.txt', ['../ken1.txt','../ken2.txt'], None ), ['../ken.txt','../ken1.txt','../ken2.txt']) 
    def test_filename_list_p20_simple_filename_and_list_excludelist(self):
        self.assertEqual(kvutil.filename_list( 'ken.txt', ['ken1.txt','ken2.txt'], None, False, excludefilenamelist=['ken.txt','ken1.txt'] ), ['ken2.txt']) 
    def test_filename_list_p21_simple_filename_and_list_excludelist_dups(self):
        self.assertEqual(kvutil.filename_list( 'ken.txt', ['ken1.txt','ken2.txt'], None, False, excludefilenamelist=['ken.txt','ken1.txt','ken.txt'] ), ['ken2.txt']) 
    def test_filename_list_p22_simple_filename_and_list_excludelist_notinlist(self):
        self.assertEqual(kvutil.filename_list( 'ken.txt', ['ken1.txt','ken2.txt'], None, False, excludefilenamelist=['ken.txt','ken1.txt','ken4.txt'] ), ['ken2.txt']) 

        
    # filename proper
    def test_filename_proper_p01_simple_filename(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt' ), os.path.normpath('./ken.txt') )
    def test_filename_proper_p02_abspath_filename(self):
        self.assertEqual(kvutil.filename_proper( os.environ.get('USERPROFILE')+'/Dropbox/LinuxShare/PerlPlay/templates/ken.txt' ), os.path.normpath( os.environ.get('USERPROFILE')+'/Dropbox/LinuxShare/PerlPlay/templates/ken.txt') )
    def test_filename_proper_p03_relpath_filename(self):
        self.assertEqual(kvutil.filename_proper( '../../PerlPlay/templates/ken.txt' ), os.path.normpath('../../PerlPlay/templates/ken.txt') )
    def test_filename_proper_p04_filename_dir(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', dir='./' ), os.path.normpath('./ken.txt') )
    def test_filename_proper_p05_filename_dir_write_check(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', dir='./', write_check=True ), os.path.normpath('./ken.txt') )
    def test_filename_proper_p06_filename_dir_create_dir(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', dir='./createdir', create_dir=True ), os.path.normpath('./createdir/ken.txt') )
        os.rmdir('./createdir')  #remove folder that was created
    def test_filename_proper_p07_filename_dir_create_absdir(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', dir='c:/createdir/level2', create_dir=True ), os.path.normpath('c:/createdir/level2/ken.txt') )
        os.rmdir('c:/createdir/level2')  #remove folder that was created
        os.rmdir('c:/createdir')  #remove folder that was created
    def test_filename_proper_f01_abspath_filename(self):
        with self.assertRaises(Exception) as context:
            kvutil.filename_proper( 'C:/Users/ken/Dropbox/LinuxShare/PerlPlay/templates/missingdir/ken.txt' )
        #self.assertTrue('This is broken' in context.exception)

    # filename unique
    def test_filename_unique_p01_filename(self):
        self.assertEqual(kvutil.filename_unique('uniquefname.txt'), os.path.normpath('./uniquefname.txt'))
    def test_filename_unique_po2_filedict_datecnt(self):
        re_file = re.compile('t_kvcsvtest-\d+v\d+\.csv')
        self.assertTrue(re_file.match(kvutil.filename_unique( { 'base_filename' : 't_kvcsvtest', 'file_ext' : '.csv', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )))
    def test_filename_unique_po3_filedict_cnt(self):
        self.assertEqual(kvutil.filename_unique( { 'base_filename' : 't_kvcsvtest', 'file_ext' : '.csv', 'overwrite' : True, 'forceuniq' : True } ), 't_kvcsvtestv01.csv')
    def test_filename_unique_p04_filename_exists(self):
        self.assertEqual(kvutil.filename_unique('{}.{:03d}'.format(tst_filename, 0)), os.path.normpath('{}v01.{:03d}'.format(tst_filename, 0)))

        
    # cloudpath
    def test_cloudpath_p01_dropbox(self):
        self.assertEqual(kvutil.cloudpath('Dropbox/LinuxShare/python/tools'), os.path.normpath( os.environ.get('USERPROFILE')+'/Dropbox/LinuxShare/python/tools'))
        

    # slurp
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

        
    # read list from file lines
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


    # def test_remove_filename - no test cases created for this function yet
    # def test_remove_dir - no test cases created for this function yet

    # datetime from string
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

    def test_datetime_from_str_p03_blank_stripblank(self):
        self.assertEqual(kvutil.datetime_from_str('', True),'' )

    def test_datetime_from_str_f01_invalid_date(self):
        with self.assertRaises(Exception) as context:
            kvutil.datetime_from_str('20/1/19')

    def test_datetime_from_str_f02_no_matching_format(self):
        with self.assertRaises(Exception) as context:
            kvutil.datetime_from_str('1/1/20019')

    def test_datetime_from_str_f03_blank(self):
        with self.assertRaises(Exception) as context:
            kvutil.datetime_from_str('')

    # datetimezone from string
    def test_datetimezone_from_str_p01_zero_padded_no_colon_neg_TZ(self):
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01 01:01:01.0101-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))))
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01 01:01:01-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01T01:01:01.0101-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01T01:01:01-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )

    def test_datetimezone_from_str_p02_zero_padded_colon_neg_TZ(self):
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01 01:01:01.0101-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01 01:01:01-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01T01:01:01.0101-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01T01:01:01-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )

    def test_datetimezone_from_str_p03_zero_padded_no_colon_pos_TZ(self):
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01 01:01:01.0101+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))))
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01 01:01:01+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01T01:01:01.0101+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01T01:01:01+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )

    def test_datetimezone_from_str_p04_zero_padded_colon_pos_TZ(self):
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01 01:01:01.0101+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01 01:01:01+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01T01:01:01.0101+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-01-01T01:01:01+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )

    def test_datetimezone_from_str_p05_nonzero_padded_no_colon_neg_TZ(self):
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1 01:01:01.0101-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))))
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1 01:01:01-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1T01:01:01.0101-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1T01:01:01-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )

    def test_datetimezone_from_str_p06_nonzero_padded_colon_neg_TZ(self):
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1 01:01:01.0101-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1 01:01:01-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1T01:01:01.0101-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1T01:01:01-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )

    def test_datetimezone_from_str_p07_nonzero_padded_no_colon_pos_TZ(self):
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1 01:01:01.0101+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))))
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1 01:01:01+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1T01:01:01.0101+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1T01:01:01+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )

    def test_datetimezone_from_str_p08_nonzero_padded_colon_pos_TZ(self):
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1 01:01:01.0101+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1 01:01:01+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1T01:01:01.0101+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvutil.datetimezone_from_str('2019-1-1T01:01:01+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )

    def test_datetimezone_from_str_p09_blank_stripblank(self):
        self.assertEqual(kvutil.datetimezone_from_str('', True),'' )

    def test_datetimezone_from_str_f01_invalid_date(self):
        with self.assertRaises(Exception) as context:
            kvutil.datetimezone_from_str('2019-19-01 01:01:01.0101-0700')

    def test_datetimezone_from_str_f02_no_matching_format(self):
        with self.assertRaises(Exception) as context:
            kvutil.datetimezone_from_str('20019-19-01 01:01:01.0101-0700')

    def test_datetimezone_from_str_f03_blank(self):
        with self.assertRaises(Exception) as context:
            kvutil.datetimezone_from_str('')


    # def test_functionName_p01_simple(self):
    # def test_loggingAppStart_p01_something(self):
    # def test_scriptinfo_p01_something(self):
    # def dump_dict_to_json_file( optiondict, filename ):
    

if __name__ == '__main__':
    logger.info('STARTUP(v%s)%s', AppVersion, '-'*40)
    logger.info('kvutil(v%s)%s', kvutil.AppVersion, '-'*40)
    unittest.main()
