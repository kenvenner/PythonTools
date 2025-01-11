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
    'max_row'        : 'max_rows',
    'maxrow'         : 'max_rows',
    'maxrows'        : 'max_rows',
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

    # the function name: def badoption_msg(func, val, val2):
    def test_badoption_msg_p01_pass(self):
        self.assertEqual( kvmatch.badoption_msg('test_badoption_msg_p01_pass', 'val', 'val2'), 'test_badoption_msg_p01_pass:possible mistyped optiondict key [val] could be [val2]')
    def test_badoption_msg_p02_fixed_pass(self):
        self.assertEqual( kvmatch.badoption_msg('test_badoption_msg_p02_fixed_pass', 'val', 'val2', fixed=True), 'test_badoption_msg_p02_fixed_pass:possible mistyped optiondict key [val] could be [val2] - this was fixed')
    def test_badoption_msg_p03_not_fixed_pass(self):
        self.assertEqual( kvmatch.badoption_msg('test_badoption_msg_p03_not_fixed_pass', 'val', 'val2', fixed=False), 'test_badoption_msg_p03_not_fixed_pass:possible mistyped optiondict key [val] could be [val2] - this was NOT fixed')

    # the function name:
    def test_badoptiondict_check_p01_bad_key(self):
        optiondict = {'no_case' : True}
        result=kvmatch.badoptiondict_check( 'test_badoptiondict_check_p01_bad_key', optiondict, badoptiondict, True )
        self.assertEqual( len( result ), 1)
        self.assertFalse( 'nocase' in optiondict )
    def test_badoptiondict_check_p02_bad_key_fixed(self):
        optiondict = {'no_case' : True}
        result=kvmatch.badoptiondict_check( 'test_badoptiondict_check_p02_bad_key', optiondict, badoptiondict, True, fix_missing=True )
        self.assertEqual( len( result ), 1)
        self.assertTrue( 'nocase' in optiondict )
    def test_badoptiondict_check_p03_bad_key_not_fixed(self):
        optiondict = {'no_case' : True, 'nocase' : False}
        result=kvmatch.badoptiondict_check( 'test_badoptiondict_check_p03_bad_not_fixed_key', optiondict, badoptiondict, True, fix_missing=True )
        self.assertEqual( len( result ), 1)
        self.assertEqual( result[0], 'test_badoptiondict_check_p03_bad_not_fixed_key:possible mistyped optiondict key [no_case] could be [nocase] - this was NOT fixed' )
        self.assertTrue( 'nocase' in optiondict )
        self.assertFalse( optiondict['nocase'] )
    def test_badoptiondict_check_f01_no_bad_key(self):
        self.assertEqual( len( kvmatch.badoptiondict_check( 'test_badoptiondict_check_f01_no_bad_key', {'nocase' : True}, badoptiondict , True)), 0)
    def test_badoptiondict_check_f01_missing_key_die(self):
        with self.assertRaises(Exception) as context:
            kvmatch.badoptiondict_check( 'test_badoptiondict_check_p01_bad_key', {'no_case' : True}, badoptiondict, True, dieonbadoption=True )


    def test_MatchRow___init___p01_simple(self):
        self.assertIsInstance( kvmatch.MatchRow( ['Col1'] ), kvmatch.MatchRow )
    def test_MatchRow___init___p02_xlat(self):
        self.assertIsInstance( kvmatch.MatchRow( ['Col1'], xlat_dict ), kvmatch.MatchRow )
    def test_MatchRow___init___f01_no_req_col(self):
        with self.assertRaises(Exception) as context:
            kvmatch.MatchRow()
    def test_MatchRow___init___f02_req_col_not_list(self):
        with self.assertRaises(Exception) as context:
            kvmatch.MatchRow('Col1')
    def test_MatchRow___init___f03_xlatdict_not_dict(self):
        with self.assertRaises(Exception) as context:
            kvmatch.MatchRow(['Col1'], 'xlatdict')
    def test_MatchRow___init___f04_optiondict_not_dict(self):
        with self.assertRaises(Exception) as context:
            kvmatch.MatchRow(['Col1'], optiondict='optiondict')
    def test_MatchRow___init___f05_optiondict2_not_dict(self):
        with self.assertRaises(Exception) as context:
            kvmatch.MatchRow(['Col1'], optiondict2='optiondict2')

    def test_MatchRow___init___p01_init_optiondict_warning(self):
        self.assertIsInstance( kvmatch.MatchRow( ['Col1'], optiondict={'no_case' : True, 'no_warnings' : True} ), kvmatch.MatchRow )
    def test_MatchRow___init___p02_init_optiondict_warning_returned_value(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'no_case' : True, 'no_warnings' : True} )
        self.assertEqual( p.warning_msg[0], kvmatch.badoption_msg('kvmatch:MatchRow:__init__', 'no_case', badoptiondict['no_case']) )
    def test_MatchRow___init___p03_init_optiondict_warning_invalid_optiondict_no_die(self):
        tempdict = dict(badoptiondict)
        tempdict['no_warnings'] = True
        #print('tempdict:', tempdict)
        p = kvmatch.MatchRow( ['Col1'], optiondict=tempdict )
        self.assertEqual( len(p.warning_msg), len(badoptiondict.keys()))
    def test_MatchRow___init___f01_init_optiondict_warning_invalid_optiondict_die_no_fix(self):
        tempdict = dict(badoptiondict)
        tempdict['no_warnings'] = True
        tempdict['dieonbadoption'] = True
        # don't fix these flagged error out
        tempdict['fix_missing'] = False
        #print('tempdict:', tempdict)
        with self.assertRaises(Exception) as context:
            p = kvmatch.MatchRow( ['Col1'], optiondict=tempdict )
    def test_MatchRow___init___f02_init_optiondict_warning_invalid_optiondict_die_fix(self):
        tempdict = dict(badoptiondict)
        tempdict['no_warnings'] = True
        tempdict['dieonbadoption'] = True
        # don't fix these flagged error out
        tempdict['fix_missing'] = True
        #print('tempdict:', tempdict)
        with self.assertRaises(Exception) as context:
            p = kvmatch.MatchRow( ['Col1'], optiondict=tempdict )


    def test_MatchRow___init___p01_init_optiondict_nocase(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'nocase' : True, 'no_warnings' : True} )
        self.assertEqual( p.nocase, True )
    def test_MatchRow___init___p01_init_optiondict_unique_column(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'unique_column' : True, 'no_warnings' : True} )
        self.assertEqual( p.unique_column, True )
    def test_MatchRow___init___p01_init_optiondict_maxrows(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'max_rows' : 2, 'no_warnings' : True} )
        self.assertEqual( p.max_rows, 2 )
    def test_MatchRow___init___p01_init_optiondict_dieonbadoption(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'dieonbadoption' : True, 'no_warnings' : True} )
        self.assertEqual( p.dieonbadoption, True )


    def test_MatchRow___init___p01_init_optiondict_xlat(self):
        p = kvmatch.MatchRow( ['Col1'], xlat_dict )
        self.assertEqual( p._xlatdict, xlat_dict )
        self.assertEqual( p._xlatdict_lower, {} )
    def test_MatchRow___init___p02_init_optiondict_xlat_nocase(self):
        p = kvmatch.MatchRow( ['Col1'], xlat_dict, optiondict={'nocase': True} )
        xlat_dict_lower = {x.lower():y for (x,y) in xlat_dict.items()}
        self.assertEqual( p._xlatdict, xlat_dict_lower )
        xlat_dict_lower = {x.lower():y.lower() for (x,y) in xlat_dict.items()}
        self.assertEqual( p._xlatdict_lower, xlat_dict_lower )


    # the function name:     def reset(self):
    def test_MatchRow_reset_p01_pass(self):
        p = kvmatch.MatchRow( ['Col1'] )
        p.reset()
        self.assertEqual( p._near_match_count, {} )
        self.assertEqual( p.rowcount, 0 )
        self.assertEqual( p._data, [] )
        self.assertEqual( p.search_failed, False )
        self.assertEqual( p.search_exceeded, False )
        self.assertEqual( p.error_msg, '')
        
    ########################################
    # the function name:     def setupForMatch(self):
    def test_MatchRow_setupForMatch_p01_pass(self):
        p = kvmatch.MatchRow( ['Col1'] )
        p.setupForMatch()
        self.assertEqual( p._header_row, [] )
        self.assertEqual( p._match_columns, 0 )
        self.assertEqual( p._match_count, {'Col1': 0} )
    def test_MatchRow_setupForMatch_p02_lower(self):
        p = kvmatch.MatchRow( ['Col1'], optiondict={'nocase': True})
        p.setupForMatch()
        self.assertEqual( p._header_row, [] )
        self.assertEqual( p._match_columns, 0 )
        self.assertEqual( p._match_count, {'col1': 0} )


    def test_MatchRow_remappedRow_p01_nothing(self):
        p = kvmatch.MatchRow( ['Col1'] )
        self.assertEqual( p.remappedRow( record ), record )
    def test_MatchRow_remappedRow_p02_blankfld(self):
        p = kvmatch.MatchRow( ['Col1'] )
        templist = record + ['']
        result   = record + ['blank001']
        self.assertEqual( p.remappedRow( templist, debug=False ), result )
    def test_MatchRow_remappedRow_p03_xlat(self):
        # find required columns that may not be in the file
        # but by using xlatdict you convert columns with xlatdict to get to the list of required columns
        p = kvmatch.MatchRow( kenlist, xlat_dict )
        self.assertEqual( p.remappedRow( record, debug=False ), kenlist )
    def test_MatchRow_remappedRow_p04_xlat_mismatched_case(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict )
        mismatch = kenlist[0:3] + record[-1:-1]
        self.assertEqual( p.remappedRow( record, debug=False ), mismatch )
    def test_MatchRow_remappedRow_p05_xlat_nocase(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict_lower, {'nocase' : True} )
        self.assertEqual( p.remappedRow( record, debug=False ), kenlist )


    # the function name:     def _unique_values(self, data, debug=False):
    def test_MatchRow__unique_values_p01_pass(self):
        p = kvmatch.MatchRow( ['Col1'] )
        data = [1,2,3,4,5]
        self.assertEqual( p._unique_values(data), [] )
    def test_MatchRow__unique_values_p02_non_unique(self):
        p = kvmatch.MatchRow( ['Col1'] )
        data = [1,2,2,3,4,5]
        self.assertEqual( p._unique_values(data), [2] )
    def test_MatchRow__unique_values_p03_non_unique_multi(self):
        p = kvmatch.MatchRow( ['Col1'] )
        data = [1,2,2,3,3,3,4,4,5]
        self.assertEqual( p._unique_values(data), [2,3,4] )
    def test_MatchRow__unique_values_p04_non_unique_multi(self):
        p = kvmatch.MatchRow( ['Col1'] )
        data = [1,2,3,4,5,2,3,4,2,3,4]
        self.assertEqual( p._unique_values(data), [2,3,4] )
        

    def test_MatchRow_matchRowList_p01_simple(self):
        p = kvmatch.MatchRow( ['Col1'] )
        self.assertTrue( p.matchRowList( record, debug=False ) )
    def test_MatchRow_matchRowList_p02_longer(self):
        p = kvmatch.MatchRow( record )
        self.assertTrue( p.matchRowList( record, debug=False ) )
    def test_MatchRow_matchRowList_p03_longer_xlat(self):
        templist = kenlist[:2]
        templist.append( record[2] )
        p = kvmatch.MatchRow( templist, xlat_dict )
        self.assertTrue( p.matchRowList( record, debug=False ) )
    def test_MatchRow_matchRowList_p04_longer_xlat_nocase(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict, {'nocase' : True} )
        self.assertTrue( p.matchRowList( record, debug=False ) )
    def test_MatchRow_matchRowList_p06_find_row_in_list(self):
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
    def test_MatchRow_matchRowList_p07_not_find_row_in_list(self):
        p = kvmatch.MatchRow( kenlist, xlat_dict, {'nocase' : True, 'max_rows' : 3 } )
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
    def test_MatchRow_matchRowList_f01_longer_not_unique(self):
        p = kvmatch.MatchRow( record, optiondict={'unique_column' : True} )
        tempdata = record[:] + record[:1]
        self.assertFalse( p.matchRowList( tempdata, debug=False ) )
        self.assertTrue( p.search_failed )
        self.assertTrue( p.error_msg.startswith('Row found with duplicate column headers:') ) 

if __name__ == '__main__':
    unittest.main()
