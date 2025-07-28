import kvutil
import unittest
import re
import os
import sys
import datetime
import json
import dateutil

# set to true when debugging
debug_file = False

# logging
import kvlogger
config=kvlogger.get_config('t_kvutil.log')
kvlogger.dictConfig(config)
logger=kvlogger.getLogger(__name__)

# set the module version number
AppVersion = '1.30'

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

def clear_argv( ):
    sys.argv=sys.argv[:1]

def generate_test_filenames( startfilename='t_kvutil_tst', ext_range=4):
    fname_list = []
    for i in range(ext_range):
        fname_list.append('{}.{:03d}'.format(startfilename, i))

    return fname_list

def file_teardown(  startfilename='t_kvutil_tst', ext_range=4, disp_msg=True):
    if disp_msg:
        logger.info('removing files from startfilename:%s:ext_range:%d', startfilename,ext_range)
    for fname in generate_test_filenames( startfilename, ext_range ):
        if os.path.exists(fname):
            os.remove(fname)

def file_setup(  startfilename='t_kvutil_tst', ext_range=4, disp_msg=True):
    if disp_msg:
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
        file_setup( tst_filename, tst_ext_range, disp_msg=False )

    # tear down features
    @classmethod
    def tearDownClass(cls):
        file_teardown( tst_filename, tst_ext_range, disp_msg=False )

    # the function name: def strtobool(val):
    def test_strtobool_p01_true(self):
        for v in ['y', 'yes', 't', 'true', 'on', '1']:
            self.assertTrue(kvutil.strtobool(v))
    def test_strtobool_p02_false(self):
        for v in ['n', 'no', 'f', 'false', 'off', '0']:
            self.assertFalse(kvutil.strtobool(v))

    # command line parsing
    def test_kv_parse_command_line_p01_config_none(self):
        optiondictconfig = { 'test1' : { } }
        clear_argv()
        set_argv(1,'invalid=invalid') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': None} )
    def test_kv_parse_command_line_p02_config_default(self):
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        clear_argv()
        set_argv(1,'invalid=invalid') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': 12} )
    def test_kv_parse_command_line_p03_config_set_type_bool(self):
        if debug_file:
            print('-'*80)
            print('test_kv_parse_command_line_p03_config_set_type_bool')
        optiondictconfig = { 'test1' : { 'value' : False, 'type' : 'bool' } }
        clear_argv()
        set_argv(1,'test1=yes') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': True} )
        set_argv(1,'test1=true') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': True} )
        set_argv(1,'test1=1') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': True} )
        set_argv(1,'test1=no') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': False} )
        set_argv(1,'test1=false') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': False} )
        set_argv(1,'test1=0') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': False} )
        if debug_file:
            print('test_kv_parse_command_line_p03_config_set_type_bool')
    def test_kv_parse_command_line_p04_config_set_type_int(self):
        optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
        clear_argv()
        set_argv(1,'test1=15') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': 15} )
    def test_kv_parse_command_line_p05_config_set_type_float(self):
        optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'float' } }
        clear_argv()
        set_argv(1,'test1=15.25') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': 15.25} )
        set_argv(1,'test1=-15.25') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': -15.25} )
        set_argv(1,'test1=15') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': 15.0} )
        set_argv(1,'test1=.001') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': 0.001} )
    def test_kv_parse_command_line_p06_config_set_type_dir(self):
        optiondictconfig = { 'outdir' : { 'type' : 'dir' } }
        clear_argv()
        set_argv(1,'outdir=c:/temp') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'outdir': 'c:\\temp'} )
    def test_kv_parse_command_line_p07_config_set_type_listr(self):
        optiondictconfig = { 'names' : { 'type' : 'liststr' } }
        clear_argv()
        set_argv(1,'names=ken,debbie,bob,jill') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'names': ['ken','debbie','bob','jill']} )
        set_argv(1,'names=ken') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'names': ['ken']} )
    def test_kv_parse_command_line_p08_config_set_type_date_slashes(self):
        optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
        clear_argv()
        set_argv(1,'onlygtdate=01/01/2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=1/1/2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=01/01/19') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'onlygtdate': datetime.datetime(2019,1,1)} )
    def test_kv_parse_command_line_p09_config_set_type_date_dashes(self):
        optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
        clear_argv()
        set_argv(1,'onlygtdate=01-01-2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=1-1-2019') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=01-01-19') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'onlygtdate': datetime.datetime(2019,1,1)} )
    def test_kv_parse_command_line_p10_config_set_type_date_YMD(self):
        optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
        clear_argv()
        set_argv(1,'onlygtdate=2019-01-01') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'onlygtdate': datetime.datetime(2019,1,1)} )
        set_argv(1,'onlygtdate=20190101') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'onlygtdate': datetime.datetime(2019,1,1)} )
    def test_kv_parse_command_line_p11_config_set_type_inlist(self):
        optiondictconfig = { 'log_level' : { 'inlist' : 'date', 'valid' : ['DEBUG','INFO','WARNING','ERROR','CRITICAL'] } }
        clear_argv()
        set_argv(1,'log_level=DEBUG') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'log_level': 'DEBUG'} )
    def test_kv_parse_command_line_p12_config_required(self):
        optiondictconfig = { 'test1' : { 'required' : True, 'type' : 'bool' }, 'AppVersion' : { 'value' : '1.01' } }
        clear_argv()
        set_argv(1,'test1=0') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1': False, 'AppVersion' : '1.01'} )
    def test_kv_parse_command_line_p13_config_default_config_setting(self):
        optiondictconfig = { 'AppVersion' : { 'value' : '1.01' } }
        clear_argv()
        set_argv(1,'log_level=DEBUG') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'log_level': 'DEBUG', 'AppVersion' : '1.01'} )
    def test_kv_parse_command_line_p14_config_keymapdict(self):
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        keymapdict = { 'invalid' : 'test1' }
        clear_argv()
        set_argv(1,'invalid=invalid') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, keymapdict=keymapdict ), {'test1' : 'invalid'} )
    def test_kv_parse_command_line_p15_config_conf_json_cmdline_single(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        clear_argv()
        set_argv(1,'conf_json=t_kvutil.json') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'conf_json': ['t_kvutil.json'], 'test1' : 'conf_json_loaded'} )
        kvutil.remove_filename('t_kvutil.json')
    def test_kv_parse_command_line_p16_config_conf_json_cmdline_multiple(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        conf_json= { 'test2' : 'conf_json_loaded' }
        with open('t_kvutil2.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 }, 'test2' : { 'value' : 12 } }
        clear_argv()
        set_argv(1,'conf_json=t_kvutil.json,t_kvutil2.json') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'conf_json': ['t_kvutil.json', 't_kvutil2.json'], 'test1' : 'conf_json_loaded', 'test2' : 'conf_json_loaded'} )
        kvutil.remove_filename('t_kvutil.json')
        kvutil.remove_filename('t_kvutil2.json')
    def test_kv_parse_command_line_p17_config_conf_json_optiondictconfig_single_list(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 }, 'conf_json' : { 'value' : ['t_kvutil.json'] }, 'set_cmd' : {} }
        clear_argv()
        set_argv(1,'set_cmd=cmd') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'conf_json': ['t_kvutil.json'], 'test1' : 'conf_json_loaded', 'set_cmd' : 'cmd'} )
        kvutil.remove_filename('t_kvutil.json')
    def test_kv_parse_command_line_p18_config_conf_json_optiondictconfig_single_value(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 }, 'conf_json' : { 'value' : 't_kvutil.json' }, 'set_cmd' : {}}
        clear_argv()
        set_argv(1,'set_cmd=cmd') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'conf_json': ['t_kvutil.json'], 'test1' : 'conf_json_loaded', 'set_cmd' : 'cmd'} )
        kvutil.remove_filename('t_kvutil.json')
    def test_kv_parse_command_line_p19_config_conf_json_optiondictconfig_multiple_list(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        conf_json= { 'test2' : 'conf_json_loaded' }
        with open('t_kvutil2.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 }, 'test2' : { 'value' : 12 }, 'conf_json' : { 'value' : ['t_kvutil.json', 't_kvutil2.json'] }, 'set_cmd' : {}}
        clear_argv()
        set_argv(1,'set_cmd=cmd') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'conf_json': ['t_kvutil.json', 't_kvutil2.json'], 'test1' : 'conf_json_loaded', 'test2' : 'conf_json_loaded', 'set_cmd' : 'cmd'} )
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
        clear_argv()
        set_argv(1,'set_cmd=cmd') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'conf_json': ['t_kvutil.json', 't_kvutil2.json'], 'test1' : 'value_override', 'set_cmd' : 'cmd'} )
        kvutil.remove_filename('t_kvutil.json')
        kvutil.remove_filename('t_kvutil2.json')
    def test_kv_parse_command_line_p21_config_conf_json_cmdline_override(self):
        conf_json= { 'test1' : 'conf_json_loaded' }
        with open('t_kvutil.json', 'w') as json_conf:
            json.dump(conf_json, json_conf)
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        clear_argv()
        set_argv(1,'conf_json=t_kvutil.json') # push value onto command line (string)
        set_argv(2,'test1=cmdline_loaded') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'conf_json': ['t_kvutil.json'], 'test1' : 'cmdline_loaded'} )
        kvutil.remove_filename('t_kvutil.json')
        clear_argv()
    def test_kv_parse_command_line_p22_config_conf_json_cmdline_single_not_exist(self):
        optiondictconfig = { 'test1' : { 'value' : 12 } }
        set_argv(1,'conf_json=t_kvutil2.json') # push value onto command line (string)
        kvutil.remove_filename('t_kvutil2.json')
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False ), {'test1' : 12 } )

    # passing skipcmdlineargs = True
    def test_kv_parse_command_line_p30_skipcmdlineargs_config_set_type_int(self):
        optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' }}
        if debug_file:
            print('\n\ntest_kv_parse_command_line_p30_skipcmdlineargs_config_set_type_int')
            print('cfg:', optiondictconfig)
            print(kvutil.kv_parse_command_line( optiondictconfig, skipcmdlineargs=True ))
        clear_argv()
        set_argv(1,'test1=15') # push value onto command line (string)
        self.assertEqual(kvutil.kv_parse_command_line( optiondictconfig, skipcmdlineargs=True ), {'test1': 12} )

    # additional tests to add
    # passing cc_cfg
    # passing cc_args
        
    def test_kv_parse_command_line_f01_config_required_missing(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'required' : True, 'type' : 'bool' }, 'AppVersion' : { 'value' : '1.01' } }
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f02_config_set_type_bool_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'boolfield' : { 'type' : 'bool' } }
            clear_argv()
            set_argv(1,'boolfield=01:01:2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f03_config_set_type_int_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
            clear_argv()
            set_argv(1,'test1=ken') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f04_config_set_type_int_bad02(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
            clear_argv()
            set_argv(1,'test1=True') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f05_config_set_type_int_bad03(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'test1' : { 'value' : 12, 'type' : 'int' } }
            clear_argv()
            set_argv(1,'test1=1.67') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f06_config_set_type_float_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'floatfield' : { 'type' : 'float' } }
            set_argv(1,'floatfield=string') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f07_config_set_type_float_bad02(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'floatfield' : { 'type' : 'float' } }
            clear_argv()
            set_argv(1,'floatfield=2019-01-01') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f08_config_set_type_date_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
            clear_argv()
            set_argv(1,'onlygtdate=01:01:2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f09_config_set_type_date_bad02(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
            clear_argv()
            set_argv(1,'onlygtdate=13-01-2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f10_config_set_type_date_bad03(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
            clear_argv()
            set_argv(1,'onlygtdate=12-32-2019') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f11_config_set_type_date_bad04(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'onlygtdate' : { 'type' : 'date' } }
            clear_argv()
            set_argv(1,'onlygtdate=string') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f12_config_set_type_inlist_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'AppVersion' : { 'value' : '1.01' } }
            clear_argv()
            set_argv(1,'log_level=NOTINLIST') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f12_config_set_type_inlist_bad01(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'no_valid_defined' : { 'value' : '1.01', 'type' : 'inlist' } }
            clear_argv()
            set_argv(1,'no_valid_defined=fail') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )
    def test_kv_parse_command_line_f13_config_raise_error_unknown_value(self):
        with self.assertRaises(Exception) as context:
            optiondictconfig = { 'valid_defined' : { 'value' : '1.01' } }
            clear_argv()
            set_argv(1,'no_valid_defined=fail') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, raise_error=True )
    def test_kv_parse_command_line_f14_config_missing_conf_json(self):
        with self.assertRaises(Exception) as context:
            kvutil.remove_filename('t_kvutil.json')
            optiondictconfig = { 'test1' : { 'value' : 12 }, 'conf_mustload' : True }
            clear_argv()
            set_argv(1,'conf_json=t_kvutil.json') # push value onto command line (string)
            kvutil.kv_parse_command_line( optiondictconfig, disp_msg=False )

    # hashmap setting
    def test_set_when_not_set_p01_key2_not_exist(self):
        self.assertEqual(kvutil.set_when_not_set( { 'key1' : { 'key3' : 'value3'} }, 'key1', 'key2', 'value2' ), True )

    # the function name: def kv_parse_command_line_display(optiondictconfig, defaultoptions=None, optiondict=None, tblfmt=False, debug=False):
    def test_kv_parse_command_line_display_p01_pass(self):
        optiondictconfig={}
        kvutil.kv_parse_command_line_display(optiondictconfig)
        self.assertEqual(optiondictconfig, {})

    # the function name: def remove_filename(filename, calledfrom='', debug=False, maxretry=20):
    def test_remove_filename_p01_pass(self):
        # create a filename to be removed
        fname = 'tst_remove_filename.txt'
        with open(fname, 'a') as fp:
            fp.write('thing')
        self.assertTrue(os.path.exists(fname))
        kvutil.remove_filename(fname)
        self.assertFalse(os.path.exists(fname))
        
        
    ########################################
    # the function name: def remove_dir(dirname, calledfrom='', debug=False, maxretry=20):
    # def test_remove_dir_p01_pass(self):
    ########################################
    # the function name: def dir_remove(dirname, calledfrom='', debug=False, maxretry=20):
    # def test_dir_remove_p01_pass(self):
        
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

    ########################################
    # prior function: filename_split
    # the function name: def filename_splitall(path):
    def test_filename_splitall_p01_pass(self):
        result = ('\\dir1\\dir2\\dir3\\dir4', 'fname', '.ext')
        self.assertEqual(kvutil.filename_split('/dir1/dir2/dir3/dir4/fname.ext'), result)

    
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
        self.assertEqual(kvutil.filename_proper( 'requirements.txt' ), os.path.normpath('./requirements.txt') )
    def test_filename_proper_p02_abspath_filename(self):
        self.assertEqual(kvutil.filename_proper( os.environ.get('USERPROFILE')+'/Dropbox/LinuxShare/python/tools/requirements.txt' ), os.path.normpath( os.environ.get('USERPROFILE')+'/Dropbox/LinuxShare/python/tools/requirements.txt') )
    def test_filename_proper_p03_relpath_filename(self):
        self.assertEqual(kvutil.filename_proper( '../../python/tools/requirements.txt' ), os.path.normpath('../../python/tools/requirements.txt') )
    def test_filename_proper_p04_filename_dir(self):
        self.assertEqual(kvutil.filename_proper( 'requirements.txt', file_dir='./'), os.path.normpath('./requirements.txt'))
    def test_filename_proper_p05_filename_dir_write_check(self):
        self.assertEqual(kvutil.filename_proper( 'requirements.txt', file_dir='./', write_check=True), os.path.normpath('./requirements.txt'))
    def test_filename_proper_p06_filename_dir_create_dir(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', file_dir='./createdir', create_dir=True), os.path.normpath('./createdir/ken.txt'))
        os.rmdir('./createdir')  #remove folder that was created
    def test_filename_proper_p07_filename_dir_create_absdir(self):
        self.assertEqual(kvutil.filename_proper( 'ken.txt', file_dir='c:/createdir/level2', create_dir=True), os.path.normpath('c:/createdir/level2/ken.txt'))
        os.rmdir('c:/createdir/level2')  #remove folder that was created
        os.rmdir('c:/createdir')  #remove folder that was created
    def test_filename_proper_f01_abspath_filename(self):
        with self.assertRaises(Exception) as context:
            kvutil.filename_proper( 'C:/Users/ken/Dropbox/LinuxShare/PerlPlay/templates/missingdir/ken.txt' )
        #self.assertTrue('This is broken' in context.exception)

    # the function name: def filename_remove(filename, calledfrom='', debug=False, maxretry=20):
    def test_filename_remove_p01_pass(self):
        # create a filename to be removed
        fname = 'tst_remove_filename.txt'
        with open(fname, 'a') as fp:
            fp.write('thing')
        self.assertTrue(os.path.exists(fname))
        kvutil.filename_remove(fname)
        self.assertFalse(os.path.exists(fname))

    # filename unique
    def test_filename_unique_p01_filename(self):
        self.assertEqual(kvutil.filename_unique('uniquefname.txt'), os.path.normpath('./uniquefname.txt'))
    def test_filename_unique_po2_filedict_datecnt(self):
        re_file = re.compile(r't_kvcsvtest-\d+v\d+\.csv')
        self.assertTrue(re_file.match(kvutil.filename_unique( { 'base_filename' : 't_kvcsvtest', 'file_ext' : '.csv', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )))
    def test_filename_unique_po3_filedict_cnt(self):
        self.assertEqual(kvutil.filename_unique( { 'base_filename' : 't_kvcsvtest', 'file_ext' : '.csv', 'overwrite' : True, 'forceuniq' : True } ), 't_kvcsvtestv01.csv')
    def test_filename_unique_p04_filename_exists(self):
        self.assertEqual(kvutil.filename_unique('{}.{:03d}'.format(tst_filename, 0)), os.path.normpath('{}v01.{:03d}'.format(tst_filename, 0)))
    def test_filename_unique_p05_filename_output_dir(self):
        self.assertEqual(kvutil.filename_unique('uniquefname.txt', filename_href={'file_path': 'xlsx'}), os.path.normpath('xlsx/uniquefname.txt'))

        
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



    # the function name: def functionName(callBackNumber=1):
    def test_functionName_p01_pass(self):
        pass
    
    ########################################
    # the function name: def loggingAppStart(logger, optiondict, pgm=None):
    def test_loggingAppStart_p01_pass(self):
        pass
    
    ########################################
    # the function name: def scriptinfo():
    def test_scriptinfo_p01_pass(self):
        # print('SCRIPT INFO')
        # print(kvutil.scriptinfo())
        result = {
            'name': 't_kvutil.py',
            'source': 't_kvutil.py',
            'dir': 'C:\\Users\\KenVenner\\Dropbox\\LinuxShare\\python\\tools'
        }
        # self.assertEqual(kvutil.scriptinfo(), result)
        self.assertEqual(True, True)

    # the function name: def load_json_file_to_dict(filename):
    def test_load_json_file_to_dict_p01_pass(self):
        optiondict = {
            'key1': '1',
            'val1': '1',
            'val2': '2',
            'val3': '3'
        }
        filename = 'tst_kv_json.json'
        kvutil.dump_dict_to_json_file(filename, optiondict)
        self.assertTrue(os.path.exists(filename))
        # now read it back in
        read_dict = kvutil.load_json_file_to_dict(filename)
        self.assertEqual(optiondict, read_dict)
        # now remove the file
        kvutil.remove_filename(filename)
        
    ########################################
    # the function name: def dump_dict_to_json_file(filename, optiondict):
    def test_dump_dict_to_json_file_p01_pass(self):
        optiondict = {
            'key1': '1',
            'val1': '1',
            'val2': '2',
            'val3': '3'
        }
        filename = 'tst_kv_json.json'
        kvutil.dump_dict_to_json_file(filename, optiondict)
        self.assertTrue(os.path.exists(filename))
        # now remove the file
        kvutil.remove_filename(filename)
    

    # test the conversion of dict to list of dict
    def test_dict2update_list_p01_dict(self):
        in_dict = {'a':1, 'b':2}
        fulllist = [
            {'Field': 'a', 'CurrentValue': 1, 'NewValue': ''},
            {'Field': 'b', 'CurrentValue': 2, 'NewValue': ''}
        ]
        self.assertEqual(kvutil.dict2update_list(in_dict), fulllist)
    def test_dict2update_list_p02_follow_order(self):
        in_dict = {'b': 2, 'a':1}
        fulllist = [
            {'Field': 'b', 'CurrentValue': 2, 'NewValue': ''},
            {'Field': 'a', 'CurrentValue': 1, 'NewValue': ''}
        ]
        self.assertEqual(kvutil.dict2update_list(in_dict), fulllist)
    def test_dict2update_list_p03_follow_set_order(self):
        in_dict = {'b': 2, 'a':1}
        fulllist = [
            {'Field': 'a', 'CurrentValue': 1, 'NewValue': ''},
            {'Field': 'b', 'CurrentValue': 2, 'NewValue': ''}
        ]
        self.assertEqual(kvutil.dict2update_list(in_dict, sorted_flds=['a', 'b']), fulllist)
    def test_dict2update_list_p04_set_columns(self):
        in_dict = {'a':1, 'b':2}
        fulllist = [
            {'NewField': 'a', 'NewCurrentValue': 1, 'NewNewValue': ''},
            {'NewField': 'b', 'NewCurrentValue': 2, 'NewNewValue': ''}
        ]
        col_names = {'Field': 'NewField', 'CurrentValue': 'NewCurrentValue', 'NewValue': 'NewNewValue'}
        self.assertEqual(kvutil.dict2update_list(in_dict, col_names=col_names), fulllist)
    def test_dict2update_list_p05_set_column(self):
        in_dict = {'a':1, 'b':2}
        fulllist = [
            {'NewField': 'a', 'CurrentValue': 1, 'NewValue': ''},
            {'NewField': 'b', 'CurrentValue': 2, 'NewValue': ''}
        ]
        col_names = {'Field': 'NewField'}
        self.assertEqual(kvutil.dict2update_list(in_dict, col_names=col_names), fulllist)
    def test_dict2update_list_p06_set_column_invalid(self):
        in_dict = {'a':1, 'b':2}
        fulllist = [
            {'Field': 'a', 'CurrentValue': 1, 'NewValue': ''},
            {'Field': 'b', 'CurrentValue': 2, 'NewValue': ''}
        ]
        col_names = {'FieldBad': 'NewField'}
        self.assertEqual(kvutil.dict2update_list(in_dict, col_names=col_names), fulllist)
       

    # True if any element is populated - any_field_is_populated(rec, copy_fields)
    def test_any_field_is_populated_p01_empty(self):
        rec = {'col1': 'val1',  'col2': 'val2',  'col3': '',  'col4': ''}
        copy_fields = ['col3', 'col4']
        self.assertEqual(kvutil.any_field_is_populated(rec, copy_fields), False)

    def test_any_field_is_populated_p02_empty_string(self):
        rec = {'col1': 'val1',  'col2': 'val2',  'col3': ' ',  'col4': ''}
        copy_fields = ['col3', 'col4']
        self.assertEqual(kvutil.any_field_is_populated(rec, copy_fields), True)

    def test_any_field_is_populated_p03_string(self):
        rec = {'col1': 'val1',  'col2': 'val2',  'col3': 'k',  'col4': ''}
        copy_fields = ['col3', 'col4']
        self.assertEqual(kvutil.any_field_is_populated(rec, copy_fields), True)

    def test_any_field_is_populated_p04_value_int(self):
        rec = {'col1': 'val1',  'col2': 'val2',  'col3': 1,  'col4': ''}
        copy_fields = ['col3', 'col4']
        self.assertEqual(kvutil.any_field_is_populated(rec, copy_fields), True)

    def test_any_field_is_populated_p05_zero_int(self):
        rec = {'col1': 'val1',  'col2': 'val2',  'col3': 0,  'col4': ''}
        copy_fields = ['col3', 'col4']
        self.assertEqual(kvutil.any_field_is_populated(rec, copy_fields), True)

    def test_any_field_is_populated_p06_value_float(self):
        rec = {'col1': 'val1',  'col2': 'val2',  'col3': 1.0,  'col4': ''}
        copy_fields = ['col3', 'col4']
        self.assertEqual(kvutil.any_field_is_populated(rec, copy_fields), True)

    def test_any_field_is_populated_p07_zero_float(self):
        rec = {'col1': 'val1',  'col2': 'val2',  'col3': 0.0,  'col4': ''}
        copy_fields = ['col3', 'col4']
        self.assertEqual(kvutil.any_field_is_populated(rec, copy_fields), True)


    # populate field with value when blank
    def test_set_blank_field_values_p01_empty(self):
        rec = [{'col1': 'val1',  'col2': 'val2',  'col3': '',  'col4': ''}]
        result = [{'col1': 'val1',  'col2': 'val2',  'col3': 'set_col3',  'col4': 'set_col4'}]
        set_blank_fields = {'col3': 'set_col3', 'col4': 'set_col4'}
        kvutil.set_blank_field_values(rec, set_blank_fields)
        self.assertEqual(rec, result)
    def test_set_blank_field_values_p02_filled(self):
        rec = [{'col1': 'val1',  'col2': 'val2',  'col3': 'col3',  'col4': 'col4'}]
        result = [{'col1': 'val1',  'col2': 'val2',  'col3': 'col3',  'col4': 'col4'}]
        set_blank_fields = {'col3': 'set_col3', 'col4': 'set_col4'}
        kvutil.set_blank_field_values(rec, set_blank_fields)
        self.assertEqual(rec, result)
    def test_set_blank_field_values_p03_filled_space(self):
        rec = [{'col1': 'val1',  'col2': 'val2',  'col3': '  ',  'col4': '  '}]
        result = [{'col1': 'val1',  'col2': 'val2',  'col3': '  ',  'col4': '  '}]
        set_blank_fields = {'col3': 'set_col3', 'col4': 'set_col4'}
        kvutil.set_blank_field_values(rec, set_blank_fields)
        self.assertEqual(rec, result)


    # populate field with value when blank
    def test_convert_hyperlink_field_values_p01_empty(self):
        rec = [{'col1': 'val1',  'col2': 'val2',  'col3': '',  'col4': ''}]
        result = [{'col1': 'val1',  'col2': 'val2',  'col3': '',  'col4': ''}]
        hyperlink_fields = ['col3', 'col4']
        kvutil.convert_hyperlink_field_values(rec, hyperlink_fields)
        self.assertEqual(rec, result)
    def test_convert_hyperlink_field_values_p02_filled(self):
        rec = [{'col1': 'val1',  'col2': 'val2',  'col3': '=HYPERLINK(the_link_3)',  'col4': '=HYPERLINK(the_link_4)'}]
        result = [{'col1': 'val1',  'col2': 'val2',  'col3': 'the_link_3',  'col4': 'the_link_4'}]
        hyperlink_fields = ['col3', 'col4']
        kvutil.convert_hyperlink_field_values(rec, hyperlink_fields)
        self.assertEqual(rec, result)
    def test_convert_hyperlink_field_values_p03_bad_col(self):
        rec = [{'col1': 'val1',  'col2': 'val2',  'col3': '=HYPERLINK(the_link_3)',  'col4': '=HYPERLINK(the_link_4)'}]
        result = [{'col1': 'val1',  'col2': 'val2',  'col3': 'the_link_3',  'col4': '=HYPERLINK(the_link_4)'}]
        hyperlink_fields = ['col3', 'col5']
        kvutil.convert_hyperlink_field_values(rec, hyperlink_fields)
        self.assertEqual(rec, result)


    # create_multi_key_lookup(src_data, fldlist)
    def test_create_multi_key_lookup_p01_2keys(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        fldlist = ['col1', 'col2']
        result =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val4'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val14'}}
        }
        self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist), result)
    def test_create_multi_key_lookup_p02_1key(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        fldlist = ['col1']
        result =  {
            'val1': {'col1': 'val1',
                     'col2': 'val2',
                     'col3': 'val3',
                     'col4': 'val4'},
            'val11': {'col1': 'val11',
                      'col2': 'val12',
                      'col3': 'val13',
                      'col4': 'val14'}
        }
        self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist), result)
    def test_create_multi_key_lookup_p03_3keys(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        fldlist = ['col1', 'col2', 'col3']
        result = {
            'val1': {'val2': {'val3': {'col1': 'val1',
                                       'col2': 'val2',
                                       'col3': 'val3',
                                       'col4': 'val4'}}},
            'val11': {'val12': {'val13': {'col1': 'val11',
                                          'col2': 'val12',
                                          'col3': 'val13',
                                          'col4': 'val14'}}}
        }
        self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist), result)
    def test_create_multi_key_lookup_p04_3keys_same(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val14'}
        ]
        fldlist = ['col1', 'col2', 'col3']
        result = {
            'val1': {'val2': {'val3': {'col1': 'val1',
                                       'col2': 'val2',
                                       'col3': 'val3',
                                       'col4': 'val14'}}}
        }
        self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist), result)
    def test_create_multi_key_lookup_p05_skip_empty(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': '', 'col4': ''}
        ]
        fldlist = ['col1', 'col2']
        copy_fields = ['col3', 'col4']
        result = {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val4'}}
        }
        self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist, copy_fields), result)
    def test_create_multi_key_lookup_p06_skip_empty_one_filled(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': '',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': '', 'col4': ''}
        ]
        fldlist = ['col1', 'col2']
        copy_fields = ['col3', 'col4']
        result = {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': '',
                              'col4': 'val4'}}
        }
        self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist, copy_fields), result)
    def test_create_multi_key_lookup_f01_key_not_in_rec(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': '',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': '', 'col4': ''}
        ]
        fldlist = ['col1', 'cola']
        copy_fields = ['col3', 'col4']
        result = {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': '',
                              'col4': 'val4'}}
        }
        with self.assertRaises(Exception) as context:
            self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist, copy_fields, disp_msg=False), result)
    def test_create_multi_key_lookup_f02_copy_not_in_rec(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': '',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': '', 'col4': ''}
        ]
        fldlist = ['col1', 'col2']
        copy_fields = ['cola', 'col4']
        result = {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': '',
                              'col4': 'val4'}}
        }
        with self.assertRaises(Exception) as context:
            self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist, copy_fields, disp_msg=False), result)
    def test_create_multi_key_lookup_f03_copyfld_not_list(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': '',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': '', 'col4': ''}
        ]
        fldlist = ['col1', 'col2']
        copy_fields = 'cola'
        result = {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': '',
                              'col4': 'val4'}}
        }
        with self.assertRaises(Exception) as context:
            self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist, copy_fields, disp_msg=False), result)
    def test_create_multi_key_lookup_f04_None_key_flds(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        fldlist = None
        result =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val4'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val14'}}
        }
        with self.assertRaises(Exception) as context:
            self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist, disp_msg=False), result)
    def test_create_multi_key_lookup_f05_key_not_list(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        fldlist = 'col1'
        result =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val4'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val14'}}
        }
        with self.assertRaises(Exception) as context:
            self.assertEqual(kvutil.create_multi_key_lookup(src_data, fldlist, disp_msg=False), result)
        
            
    ########################################
    # prior function: create_multi_key_lookup
    # the function name: def create_multi_key_lookup_excel(excel_dict, fldlist, copy_fields=None):
    # def test_create_multi_key_lookup_excel_p01_pass(self):

    # copy_matched_data_cnt(dst_data, src_lookup, key_fields, copy_fields)
    def test_copy_matched_data_cnt_p01_2keys(self):
        dst_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'col2']
        copy_fields = ['col4']
        src_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val44'}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val44'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val44'}
        ]
        matched_cnt, updated_cnt = kvutil.copy_matched_data_cnt(dst_data, src_lookup, key_fields, copy_fields, disp_msg=False)
        self.assertEqual(matched_cnt, 2)
        self.assertEqual(updated_cnt, 2)
        self.assertEqual(dst_data, result)
    
    def test_copy_matched_data_cnt_p02_2keys_1matches(self):
        dst_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'col2']
        copy_fields = ['col4']
        src_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val14'}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val44'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        matched_cnt, updated_cnt = kvutil.copy_matched_data_cnt(dst_data, src_lookup, key_fields, copy_fields, disp_msg=False)
        self.assertEqual(matched_cnt, 2)
        self.assertEqual(updated_cnt, 1)
        self.assertEqual(dst_data, result)

    def test_copy_matched_data_cnt_p03_2keys_1matches_col3diff(self):
        dst_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'col2']
        copy_fields = ['col4']
        src_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': '',
                                'col4': 'val14'}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val44'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        matched_cnt, updated_cnt = kvutil.copy_matched_data_cnt(dst_data, src_lookup, key_fields, copy_fields, disp_msg=False)
        self.assertEqual(matched_cnt, 2)
        self.assertEqual(updated_cnt, 1)
        self.assertEqual(dst_data, result)
        
    def test_copy_matched_data_cnt_p04_2keys_1matches_col3diff_none_space(self):
        dst_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': None}
        ]
        key_fields = ['col1', 'col2']
        copy_fields = ['col4']
        src_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': '',
                                'col4': ''}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val44'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': ''}
        ]
        matched_cnt, updated_cnt = kvutil.copy_matched_data_cnt(dst_data, src_lookup, key_fields, copy_fields, disp_msg=False)
        self.assertEqual(matched_cnt, 2)
        self.assertEqual(updated_cnt, 1)
        self.assertEqual(dst_data, result)
    
    # copy_matched_data(dst_data, src_lookup, key_fields, copy_fields)
    def test_copy_matched_data_p01_2keys(self):
        dst_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'col2']
        copy_fields = ['col4']
        src_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val44'}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val44'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val44'}
        ]
        self.assertEqual(kvutil.copy_matched_data(dst_data, src_lookup, key_fields, copy_fields, disp_msg=False), 2)
        self.assertEqual(dst_data, result)
    def test_copy_matched_data_f01_copy_fld_not_there(self):
        dst_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'col2']
        copy_fields = ['cola']
        src_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val44'}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val44'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val44'}
        ]
        with self.assertRaises(Exception) as context:
            self.assertEqual(kvutil.copy_matched_data(dst_data, src_lookup, key_fields, copy_fields, disp_msg=False), 2)
            self.assertEqual(dst_data, result)
    def test_copy_matched_data_f02_copy_fld_not_list(self):
        dst_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'col2']
        copy_fields = 'cola'
        src_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val44'}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val44'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val44'}
        ]
        with self.assertRaises(Exception) as context:
            self.assertEqual(kvutil.copy_matched_data(dst_data, src_lookup, key_fields, copy_fields, disp_msg=False), 2)
            self.assertEqual(dst_data, result)
    def test_copy_matched_data_f03_key_fld_not_there(self):
        dst_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'cola']
        copy_fields = ['col4']
        src_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val44'}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val44'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val44'}
        ]
        with self.assertRaises(Exception) as context:
            self.assertEqual(kvutil.copy_matched_data(dst_data, src_lookup, key_fields, copy_fields, disp_msg=False), 2)
            self.assertEqual(dst_data, result)
    def test_copy_matched_data_f04_key_fld_not_list(self):
        dst_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = 'cola'
        copy_fields = ['col4']
        src_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val44'}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val44'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val44'}
        ]
        with self.assertRaises(Exception) as context:
            self.assertEqual(kvutil.copy_matched_data(dst_data, src_lookup, key_fields, copy_fields, disp_msg=False), 2)
            self.assertEqual(dst_data, result)

    # the function name: def diff_matched_data(dst_data, src_lookup, key_fields, diff_fields=None, exc_fields=None):
    def test_diff_matched_data_p01_pass(self):
        # they all match - no differences
        dst_data = [
            {'key': '1', 'val1': '1', 'val2': '2', 'val3': '3'},
            {'key': '2', 'val1': '2', 'val2': '3', 'val3': '4'}
        ]
        src_lookup = {
            '1': {'key': '1', 'val1': '1', 'val2': '2', 'val3': '3'},
            '2': {'key': '2', 'val1': '2', 'val2': '3', 'val3': '4'}
        }
        key_fields=['key']
        results = kvutil.diff_matched_data(dst_data, src_lookup, key_fields)
        self.assertEqual(results, [])
        
    def test_diff_matched_data_p02_val3_diff(self):
        # they all match - no differences
        dst_data = [
            {'key': '1', 'val1': '1', 'val2': '2', 'val3': '3'},
            {'key': '2', 'val1': '2', 'val2': '3', 'val3': '4'}
        ]
        src_lookup = {
            '1': {'key': '1', 'val1': '1', 'val2': '2', 'val3': '4'},
            '2': {'key': '2', 'val1': '2', 'val2': '3', 'val3': '5'}
        }
        key_fields=['key']
        results = kvutil.diff_matched_data(dst_data, src_lookup, key_fields)
        expected_results = [
            {'key': '1', 'fld': 'val3', 'src_value': '4', 'dst_value': '3'},
            {'key': '2', 'fld': 'val3', 'src_value': '5', 'dst_value': '4'}
        ]
        self.assertEqual(results, expected_results)
        
    def test_diff_matched_data_p03_val2_val3_diff(self):
        # they all match - no differences
        dst_data = [
            {'key': '1', 'val1': '1', 'val2': '2', 'val3': '3'},
            {'key': '2', 'val1': '2', 'val2': '3', 'val3': '4'}
        ]
        src_lookup = {
            '1': {'key': '1', 'val1': '1', 'val2': '4', 'val3': '4'},
            '2': {'key': '2', 'val1': '2', 'val2': '5', 'val3': '5'}
        }
        key_fields=['key']
        results = kvutil.diff_matched_data(dst_data, src_lookup, key_fields)
        expected_results = [
            {'key': '1', 'fld': 'val2', 'dst_value': '2', 'src_value': '4'},
            {'key': '1', 'fld': 'val3', 'dst_value': '3', 'src_value': '4'},
            {'key': '2', 'fld': 'val2', 'dst_value': '3', 'src_value': '5'},
            {'key': '2', 'fld': 'val3', 'dst_value': '4', 'src_value': '5'}
        ]
        if debug_file:
            print(results)
        self.assertEqual(results, expected_results)

    def test_diff_matched_data_p04_val2_val3_only_val3_diff(self):
        # they all match - no differences
        dst_data = [
            {'key': '1', 'val1': '1', 'val2': '2', 'val3': '3'},
            {'key': '2', 'val1': '2', 'val2': '3', 'val3': '4'}
        ]
        src_lookup = {
            '1': {'key': '1', 'val1': '1', 'val2': '4', 'val3': '4'},
            '2': {'key': '2', 'val1': '2', 'val2': '5', 'val3': '5'}
        }
        key_fields=['key']
        results = kvutil.diff_matched_data(dst_data, src_lookup, key_fields, diff_fields=['val3'])
        expected_results = [
            {'key': '1', 'fld': 'val3', 'dst_value': '3', 'src_value': '4'},
            {'key': '2', 'fld': 'val3', 'dst_value': '4', 'src_value': '5'}
        ]
        self.assertEqual(results, expected_results)
        
    def test_diff_matched_data_p05_val2_val3_excl_val2_diff(self):
        # they all match - no differences
        dst_data = [
            {'key': '1', 'val1': '1', 'val2': '2', 'val3': '3'},
            {'key': '2', 'val1': '2', 'val2': '3', 'val3': '4'}
        ]
        src_lookup = {
            '1': {'key': '1', 'val1': '1', 'val2': '4', 'val3': '4'},
            '2': {'key': '2', 'val1': '2', 'val2': '5', 'val3': '5'}
        }
        key_fields=['key']
        results = kvutil.diff_matched_data(dst_data, src_lookup, key_fields, exc_fields=['val2'])
        expected_results = [
            {'key': '1', 'fld': 'val3', 'dst_value': '3', 'src_value': '4'},
            {'key': '2', 'fld': 'val3', 'dst_value': '4', 'src_value': '5'}
        ]
        self.assertEqual(results, expected_results)
        
    def test_diff_matched_data_p06_val2_val3_excl_val2_val3_diff(self):
        # they all match - no differences
        dst_data = [
            {'key': '1', 'val1': '1', 'val2': '2', 'val3': '3'},
            {'key': '2', 'val1': '2', 'val2': '3', 'val3': '4'}
        ]
        src_lookup = {
            '1': {'key': '1', 'val1': '1', 'val2': '4', 'val3': '4'},
            '2': {'key': '2', 'val1': '2', 'val2': '5', 'val3': '5'}
        }
        key_fields=['key']
        results = kvutil.diff_matched_data(dst_data, src_lookup, key_fields, exc_fields=['val2','val3'])
        expected_results = [
        ]
        self.assertEqual(results, expected_results)
        

    # extract_unmatched_data(src_data, dst_lookup, key_fields)
    def test_extract_unmatched_data_p01_2keys(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'col2']
        dst_lookup =  {
            'vala': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'valb': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val44'}}
        }
        result = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        res = kvutil.extract_unmatched_data(src_data, dst_lookup, key_fields)
        self.assertEqual(src_data, result)
    def test_extract_umatched_data_p02_2keys_1match(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'col2']
        copy_fields = ['col4']
        dst_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'valz': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val44'}}
        }
        result = [
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        res = kvutil.extract_unmatched_data(src_data, dst_lookup, key_fields)
        self.assertEqual(res, result)
    def test_extract_unmatched_data_f01_2keys(self):
        src_data = [
            {'col1': 'val1',  'col2': 'val2',  'col3': 'val3',  'col4': 'val4'},
            {'col1': 'val11', 'col2': 'val12', 'col3': 'val13', 'col4': 'val14'}
        ]
        key_fields = ['col1', 'col2']
        dst_lookup =  {
            'val1': {'val2': {'col1': 'val1',
                              'col2': 'val2',
                              'col3': 'val3',
                              'col4': 'val44'}},
            'val11': {'val12': {'col1': 'val11',
                                'col2': 'val12',
                                'col3': 'val13',
                                'col4': 'val44'}}
        }
        result = [
        ]
        res = kvutil.extract_unmatched_data(src_data, dst_lookup, key_fields)
        self.assertEqual(res, result)
        
    
if __name__ == '__main__':
    logger.info('STARTUP(v%s)%s', AppVersion, '-'*40)
    logger.info('kvutil(v%s)%s', kvutil.AppVersion, '-'*40)
    unittest.main()
