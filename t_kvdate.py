import kvdate
import unittest
import re
import os
import sys
import datetime
import json
import dateutil


# logging
import kvlogger
config=kvlogger.get_config('t_kvutil.log')
kvlogger.dictConfig(config)
logger=kvlogger.getLogger(__name__)

# set the module version number
AppVersion = '1.03'

# global variables
tst_filename='t_kvdate_tst'
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

def generate_test_filenames( startfilename='t_kvdate_tst', ext_range=4):
    fname_list = []
    for i in range(ext_range):
        fname_list.append('{}.{:03d}'.format(startfilename, i))

    return fname_list

def file_teardown(  startfilename='t_kvdate_tst', ext_range=4):
    logger.info('removing files from startfilename:%s:ext_range:%d', startfilename,ext_range)
    for fname in generate_test_filenames( startfilename, ext_range ):
        if os.path.exists(fname):
            os.remove(fname)

def file_setup(  startfilename='t_kvdate_tst', ext_range=4):
    logger.info('creating files from startfilename:%s:ext_range:%d', startfilename, ext_range)
    for fname in generate_test_filenames( startfilename, ext_range ):
        if not os.path.exists(fname):
            with open( fname, 'w' ) as t:
                pass
        

        
# test class
class TestKvdateFilenames(unittest.TestCase):
    # set up features
    @classmethod
    def setUpClass(cls):
        file_setup( tst_filename, tst_ext_range )

    # tear down features
    @classmethod
    def tearDownClass(cls):
        file_teardown( tst_filename, tst_ext_range )


    # the function name: def current_timezone_string():
    def test_current_timezone_string_p01_pass(self):
        pass
        
    def test_datetime2utcdatetime_p01_datetime_2_utc(self):
        n_dt = datetime.datetime(2016,1,1,11,30)
        utc_dt = datetime.datetime(2016, 1, 1, 19, 30, tzinfo=dateutil.tz.UTC)
        self.assertEqual(kvdate.datetime2utcdatetime(n_dt), utc_dt)
    def test_datetime2utcdatetime_p02_datetime_2_utc_set_tz(self):
        n_dt = datetime.datetime(2016,1,1,11,30)
        tz = 'US/Eastern'
        utc_dt = datetime.datetime(2016, 1, 1, 16, 30, tzinfo=dateutil.tz.UTC)
        self.assertEqual(kvdate.datetime2utcdatetime(n_dt, tz), utc_dt)
    
    # datetime from string
    def test_datetime_from_str_p01_zero_padded(self):
        self.assertEqual(kvdate.datetime_from_str('01/01/19'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('01/01/2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('01-01-19'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('01-01-2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('2019-01-01'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('20190101'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('01-Jan-2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('01-Jan-19'), datetime.datetime(2019, 1, 1) )

    def test_datetime_from_str_p02_notzero_padded(self):
        self.assertEqual(kvdate.datetime_from_str('1/1/19'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('1/1/2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('1-1-19'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('1-1-2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('2019-1-1'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('1-Jan-2019'), datetime.datetime(2019, 1, 1) )
        self.assertEqual(kvdate.datetime_from_str('1-Jan-19'), datetime.datetime(2019, 1, 1) )

    def test_datetime_from_str_p03_blank_stripblank(self):
        self.assertEqual(kvdate.datetime_from_str('', True),'' )

    def test_datetime_from_str_p04_match_ts_maintain(self):
        self.assertEqual(kvdate.datetime_from_str('2021-12-31'), datetime.datetime(2021, 12, 31))
        self.assertEqual(kvdate.datetime_from_str('2021-12-31 00:00:00'), datetime.datetime(2021, 12, 31))
        self.assertEqual(kvdate.datetime_from_str('12/31/2021'), datetime.datetime(2021, 12, 31))
        self.assertEqual(kvdate.datetime_from_str('2021-12-31T00:00:00Z'), datetime.datetime(2021, 12, 31))
        self.assertEqual(kvdate.datetime_from_str('31-Dec-2021 00:00'), datetime.datetime(2021, 12, 31, 0, 0))
        self.assertEqual(kvdate.datetime_from_str('31-Dec-2021 01:01'), datetime.datetime(2021, 12, 31, 1, 1))
        self.assertEqual(kvdate.datetime_from_str('31-Dec-21 00:00'), datetime.datetime(2021, 12, 31, 0, 0))
        self.assertEqual(kvdate.datetime_from_str('31-Dec-21 01:01'), datetime.datetime(2021, 12, 31, 1, 1))
    
    def test_datetime_from_str_f01_invalid_date(self):
        with self.assertRaises(Exception) as context:
            kvdate.datetime_from_str('20/1/19')

    def test_datetime_from_str_f02_no_matching_format(self):
        with self.assertRaises(Exception) as context:
            kvdate.datetime_from_str('1/1/20019')

    def test_datetime_from_str_f03_blank(self):
        with self.assertRaises(Exception) as context:
            kvdate.datetime_from_str('')

    # datetimezone from string
    def test_datetimezone_from_str_p01_zero_padded_no_colon_neg_TZ(self):
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01 01:01:01.0101-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))))
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01 01:01:01-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01T01:01:01.0101-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01T01:01:01-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )

    def test_datetimezone_from_str_p02_zero_padded_colon_neg_TZ(self):
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01 01:01:01.0101-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01 01:01:01-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01T01:01:01.0101-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01T01:01:01-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )

    def test_datetimezone_from_str_p03_zero_padded_no_colon_pos_TZ(self):
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01 01:01:01.0101+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))))
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01 01:01:01+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01T01:01:01.0101+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01T01:01:01+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )

    def test_datetimezone_from_str_p04_zero_padded_colon_pos_TZ(self):
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01 01:01:01.0101+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01 01:01:01+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01T01:01:01.0101+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-01-01T01:01:01+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )

    def test_datetimezone_from_str_p05_nonzero_padded_no_colon_neg_TZ(self):
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1 01:01:01.0101-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))))
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1 01:01:01-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1T01:01:01.0101-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1T01:01:01-0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )

    def test_datetimezone_from_str_p06_nonzero_padded_colon_neg_TZ(self):
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1 01:01:01.0101-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1 01:01:01-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1T01:01:01.0101-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1T01:01:01-07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(-1, 61200))) )

    def test_datetimezone_from_str_p07_nonzero_padded_no_colon_pos_TZ(self):
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1 01:01:01.0101+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))))
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1 01:01:01+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1T01:01:01.0101+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1T01:01:01+0700'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )

    def test_datetimezone_from_str_p08_nonzero_padded_colon_pos_TZ(self):
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1 01:01:01.0101+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1 01:01:01+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1T01:01:01.0101+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, 10100, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )
        self.assertEqual(kvdate.datetimezone_from_str('2019-1-1T01:01:01+07:00'), datetime.datetime(2019, 1, 1, 1, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(0, 25200))) )

    def test_datetimezone_from_str_p09_blank_stripblank(self):
        self.assertEqual(kvdate.datetimezone_from_str('', True),'' )

    def test_datetimezone_from_str_f01_invalid_date(self):
        with self.assertRaises(Exception) as context:
            kvdate.datetimezone_from_str('2019-19-01 01:01:01.0101-0700')

    def test_datetimezone_from_str_f02_no_matching_format(self):
        with self.assertRaises(Exception) as context:
            kvdate.datetimezone_from_str('20019-19-01 01:01:01.0101-0700')

    def test_datetimezone_from_str_f03_blank(self):
        with self.assertRaises(Exception) as context:
            kvdate.datetimezone_from_str('')


    # def test_valid_tz_string
    def test_valid_tz_string_p01_valid(self):
        self.assertTrue(kvdate.valid_tz_string('US/Eastern'))
        self.assertFalse(kvdate.valid_tz_string('US/Invalid'))

    # def test_show_timezones
    def test_show_timezones_p01_us_zones(self):
        us_tz = [
            'US/Alaska',
            'US/Aleutian',
            'US/Arizona',
            'US/Central',
            'US/East-Indiana',
            'US/Eastern',
            'US/Hawaii',
            'US/Indiana-Starke',
            'US/Michigan',
            'US/Mountain',
            'US/Pacific',
#            'US/Pacific-New', # this disappeared on 2024-09-01
            'US/Samoa',
        ]
        self.assertEqual(kvdate.show_timezones('US'), us_tz)

        
    # def test_functionName_p01_simple(self):
    # def test_loggingAppStart_p01_something(self):
    # def test_scriptinfo_p01_something(self):

    # def test_load_json_file_to_dict()
    # def test_dump_dict_to_json_file( optiondict, filename ):
    

if __name__ == '__main__':
    logger.info('STARTUP(v%s)%s', AppVersion, '-'*40)
    logger.info('kvdate(v%s)%s', kvdate.AppVersion, '-'*40)
    unittest.main()
