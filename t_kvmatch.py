import kvmatch
import unittest

import datetime
import re
import os

# logging
import kvlogger
config=kvlogger.get_config('t_kvmatch.log')
kvlogger.dictConfig(config)
logger=kvlogger.getLogger(__name__)


rowdict = { 'Company' : 'Test', 'Wine' : 'Yummy', 'Price' : 10.00, 'ProcessDate' : datetime.datetime(2020, 1, 1, 0, 0)}

record = ['Col1','Col2','Col3']
nonrecord = ['bad1','bad2','bad3']
xlat_dict = { 'Col1' : 'Ken1', 'Col2' : 'Ken2', 'Col3' : 'Ken3' }
xlat_dict_lower = { 'Col1' : 'Ken1', 'Col2' : 'Ken2', 'col3' : 'Ken3' }
kenlist = ['Ken1', 'Ken2', 'Ken3' ]
badoptiondict = {
    'no_case'        : 'nocase',
    'max_row'        : 'maxrows',
    'max_rows'       : 'maxrows',
    'uniquecolumn'   : 'unique_column',
    'uniquecolumns'  : 'unique_column',
    'unique_columns' : 'unique_column',
    'nowarning'      : 'no_warnings',
    'nowarnings'     : 'no_warnings',
    'no_warning'     : 'no_warnings',
}


class TestKVMatch(unittest.TestCase):

    def test_build_multifield_key_p01_single_string(self):
        self.assertEqual( kvmatch.build_multifield_key( rowdict, ['Company'] ), 'Test' )
    def test_build_multifield_key_p02_multiplestrings(self):
        self.assertEqual( kvmatch.build_multifield_key( rowdict, ['Company','Wine'] ), 'Test|Yummy' )
    def test_build_multifield_key_p03_string_number(self):
        self.assertEqual( kvmatch.build_multifield_key( rowdict, ['Company','Price'] ), 'Test|10.0' )
    def test_build_multifield_key_p04_string_date(self):
        self.assertEqual( kvmatch.build_multifield_key( rowdict, ['Company','ProcessDate'] ), 'Test|2020-01-01 00:00:00' )
    def test_build_multifield_key_p05_single_string_string(self):
        self.assertEqual( kvmatch.build_multifield_key( rowdict, 'Company' ), 'Test' )
    def test_build_multifield_key_p02_multiplestrings_joinchar(self):
        self.assertEqual( kvmatch.build_multifield_key( rowdict, ['Company','Wine'], joinchar=':' ), 'Test:Yummy' )
    def test_build_multifield_key_f01_missing_key(self):
        with self.assertRaises(Exception) as context:
            kvmatch.build_multifield_key( rowdict, ['Company','Missing'] )
    def test_build_multifield_key_f02_empty_dictkeys(self):
        with self.assertRaises(Exception) as context:
            kvmatch.build_multifield_key( rowdict, [] )
    def test_build_multifield_key_f03_empty_string_dictkeys(self):
        with self.assertRaises(Exception) as context:
            kvmatch.build_multifield_key( rowdict, '' )

    def test_badoptiondict_check_p01_bad_key(self):
        self.assertEqual( len( kvmatch.badoptiondict_check( 'test_badoptiondict_check_p01_bad_key', {'no_case' : True}, badoptiondict, True)), 1)
    def test_badoptiondict_check_f01_no_bad_key(self):
        self.assertEqual( len( kvmatch.badoptiondict_check( 'test_badoptiondict_check_f01_no_bad_key', {'nocase' : True}, badoptiondict , True)), 0)
    def test_badoptiondict_check_f01_missing_key_die(self):
        with self.assertRaises(Exception) as context:
            kvmatch.badoptiondict_check( 'test_badoptiondict_check_p01_bad_key', {'no_case' : True}, badoptiondict, True, dieonbadoption=True )

        
    def test_init_p01_simple(self):
        self.assertIsInstance( kvmatch.MatchRow( ['Col1'] ), kvmatch.MatchRow )
    def test_init_p02_xlat(self):
        self.assertIsInstance( kvmatch.MatchRow( ['Col1'], xlat_dict ), kvmatch.MatchRow )
    def test_init_f01_no_req_col(self):
        with self.assertRaises(Exception) as context:
            kvmatch.MatchRow()
    def test_init_f02_req_col_not_list(self):
        with self.assertRaises(Exception) as context:
            kvmatch.MatchRow('Col1')
    def test_init_f03_xlatdict_not_dict(self):
        with self.assertRaises(Exception) as context:
            kvmatch.MatchRow(['Col1'], 'xlatdict')
    def test_init_f04_optiondict_not_dict(self):
        with self.assertRaises(Exception) as context:
            kvmatch.MatchRow(['Col1'], optiondict='optiondict')

    def test_init_p01_init_optiondict_warning(self):
        self.assertIsInstance( kvmatch.MatchRow( ['Col1'], optiondict={'no_case' : True, 'no_warnings' : True} ), kvmatch.MatchRow )
    def test_init_p02_init_optiondict_warning_returned_value(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'no_case' : True, 'no_warnings' : True} )
        self.assertEqual( p.warning_msg[0], kvmatch.badoption_msg('kvmatch:MatchRow:__init__', 'no_case', badoptiondict['no_case']) )
    def test_init_p03_init_optiondict_warning_invalid_optiondict_nodie(self):
        tempdict = dict(badoptiondict)
        tempdict['no_warnings'] = True
        #print('tempdict:', tempdict)
        p = kvmatch.MatchRow( ['Col1'], optiondict=tempdict )
        self.assertEqual( len(p.warning_msg), len(badoptiondict.keys()))
    def test_init_f01_init_optiondict_warning_invalid_optiondict_die(self):
        tempdict = dict(badoptiondict)
        tempdict['no_warnings'] = True
        tempdict['dieonbadoption'] = True
        #print('tempdict:', tempdict)
        with self.assertRaises(Exception) as context:
            p = kvmatch.MatchRow( ['Col1'], optiondict=tempdict )


    def test_init_p01_init_optiondict_nocase(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'nocase' : True, 'no_warnings' : True} )
        self.assertEqual( p.nocase, True )
    def test_init_p01_init_optiondict_unique_column(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'unique_column' : True, 'no_warnings' : True} )
        self.assertEqual( p.unique_column, True )
    def test_init_p01_init_optiondict_maxrows(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'maxrows' : 2, 'no_warnings' : True} )
        self.assertEqual( p.maxrows, 2 )
    def test_init_p01_init_optiondict_dieonbadoption(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'dieonbadoption' : True, 'no_warnings' : True} )
        self.assertEqual( p.dieonbadoption, True )


    def test_init_p01_init_optiondict_xlat(self):
        p = kvmatch.MatchRow( ['Col1'], xlat_dict )
        self.assertEqual( p._xlatdict, xlat_dict )
        self.assertEqual( p._xlatdict_lower, {} )
    def test_init_p02_init_optiondict_xlat_nocase(self):
        p = kvmatch.MatchRow( ['Col1'], xlat_dict, optiondict={'nocase': True} )
        xlat_dict_lower = {x.lower():y for (x,y) in xlat_dict.items()}
        self.assertEqual( p._xlatdict, xlat_dict_lower )
        xlat_dict_lower = {x.lower():y.lower() for (x,y) in xlat_dict.items()}
        self.assertEqual( p._xlatdict_lower, xlat_dict_lower )



    def test_remappedRow_p01_nothing(self):
        p = kvmatch.MatchRow( ['Col1'] )
        self.assertEqual( p.remappedRow( record ), record )
    def test_remappedRow_p02_blankfld(self):
        p = kvmatch.MatchRow( ['Col1'] )
        templist = record + ['']
        result   = record + ['blank001']
        self.assertEqual( p.remappedRow( templist, debug=False ), result )
    def test_remappedRow_p03_xlat(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict )
        self.assertEqual( p.remappedRow( record, debug=False ), kenlist )
    def test_remappedRow_p04_xlat_mismatched_case(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict )
        mismatch = kenlist[0:3] + record[-1:-1]
        self.assertEqual( p.remappedRow( record, debug=False ), mismatch )
    def test_remappedRow_p05_xlat_nocase(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict_lower, {'nocase' : True} )
        self.assertEqual( p.remappedRow( record, debug=False ), kenlist )


    def test_matchRowList_p01_simple(self):
        p = kvmatch.MatchRow( ['Col1'] )
        self.assertTrue( p.matchRowList( record, debug=False ) )
    def test_matchRowList_p02_longer(self):
        p = kvmatch.MatchRow( record )
        self.assertTrue( p.matchRowList( record, debug=False ) )
    def test_matchRowList_p03_longer_xlat(self):
        templist = kenlist[:2]
        templist.append( record[2] )
        p = kvmatch.MatchRow( templist, xlat_dict )
        self.assertTrue( p.matchRowList( record, debug=False ) )
    def test_matchRowList_p04_longer_xlat_nocase(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict, {'nocase' : True} )
        self.assertTrue( p.matchRowList( record, debug=False ) )
    def test_matchRowList_p06_find_row_in_list(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict, {'nocase' : True, 'startrow' : 2 } )
        tempdata = [nonrecord] * 4
        tempdata.append(kenlist)
        tempdata.append(record)
        # print(tempdata)
        for data in tempdata:
            if p.matchRowList( data, debug=False ):
                if False:
                    print('matching record:', data)
                    print('final header:', p._data_mapped)
                break
        self.assertTrue( p.matchRowList( data, debug=False ) )
    def test_matchRowList_p07_not_find_row_in_list(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict, {'nocase' : True, 'maxrows' : 3 } )
        tempdata = [nonrecord] * 4
        tempdata.append(kenlist)
        tempdata.append(record)
        # print(tempdata)
        for data in tempdata:
            if p.matchRowList( data, debug=False ):
                print('matching record:', data)
                print('final header:', p._data_mapped)
                break
            if p.search_exceeded:
                break
        self.assertTrue( p.search_exceeded )
    def test_matchRowList_f01_longer_not_unique(self):
        p = kvmatch.MatchRow( record, optiondict={'unique_column' : True} )
        tempdata = record[:] + record[:1]
        self.assertFalse( p.matchRowList( tempdata, debug=False ) )
        self.assertTrue( p.search_failed )
        self.assertTrue( p.error_msg.startswith('Row found with duplicate column headers:') ) 

if __name__ == '__main__':
    unittest.main()
