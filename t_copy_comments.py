import kvutil
import t_kvutil
import sys

import pprint

import copy_comments

import unittest

import time
import copy
import os


# logging
import kvlogger
config=kvlogger.get_config('t_kvcsv.log')
kvlogger.dictConfig(config)
logger=kvlogger.getLogger(__name__)

# set up data that is used by these tests
base_optiondict = {
    'AppVersion': '1.09',
    'col_width': None,
    'copy_fields': ['Comment',
                    'NewPORequestorID',
                    'NewPORequestorName',
                    'NewPORequestorEmail'],
    'debug': False,
    'dst_dir': None,
    'dst_fname': '2024-05-04-PO-IT-Cleanup.xlsx',
    'dst_ws': None,
    'dump_recs': False,
    'force_copy_flds': False,
    'format_cell': True,
    'format_output': True,
    'hyperlink_fields': [],
    'internal_copy_fields': [],
    'json_cfg_filename': 't_copy_comments.json',
    'key_fields': ['Purchasing Document', 'Item'],
    'out_dir': None,
    'out_fname': '2024-05-04-PO-IT-Cleanup-v02.xlsx',
    'out_fname_append': '',
    'out_ws': None,
    'rmv_fname': '',
    'rmv_fname_append': '',
    'set_blank_fields': None,
    'src_dir': '/bin',
    'src_fname': '2024-04-23-PO-IT-Cleanup-v02.xlsx',
    'src_width': True,
    'src_ws': None
}



# Testing class
class TestCopyComment(unittest.TestCase):
        

    def test_validate_inputs_p01_disp_msg_set_true(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set a value to just get a value set
        optiondict['dst_fname'] = 'something'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        self.assertTrue(optiondict['disp_msg'])
        
    def test_validate_inputs_p02_disp_msg_not_set_false(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # remove the setting
        del optiondict['disp_msg']
        # set the command line
        copy_comments.validate_inputs(optiondict)
        self.assertFalse(optiondict['disp_msg'])
        
    def test_validate_inputs_p03_src_dir_not(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # clear the value
        optiondict['src_dir'] = ''
        # set a value to just get a value set
        optiondict['dst_fname'] = 'something'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        # check all things match
        for fld in ('src_dir', 'dst_dir', 'out_dir', 'rmv_dir', 'add_dir', 'fmt_dir'):
            self.assertEqual(optiondict[fld], './')
        
    def test_validate_inputs_p04_out_dir_set_rmv_add_not(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # clear the value
        optiondict['out_dir'] = 'outdir'
        # set a value to just get a value set
        optiondict['dst_fname'] = 'something'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        self.assertEqual(optiondict['add_dir'], optiondict['out_dir'])
        self.assertEqual(optiondict['rmv_dir'], optiondict['out_dir'])
        
    def test_validate_inputs_p05_dst_dir_set_rmv_add_not(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # clear the value
        optiondict['dst_dir'] = 'dstdir'
        # set a value to just get a value set
        optiondict['dst_fname'] = 'something'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        self.assertEqual(optiondict['add_dir'], optiondict['dst_dir'])
        self.assertEqual(optiondict['rmv_dir'], optiondict['dst_dir'])
        
    def test_validate_inputs_p06_both_out_dst_dir_set_rmv_add_not(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # clear the value
        optiondict['out_dir'] = 'outdir'
        optiondict['dst_dir'] = 'dstdir'
        # set a value to just get a value set
        optiondict['dst_fname'] = 'something'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        self.assertEqual(optiondict['add_dir'], optiondict['out_dir'])
        self.assertEqual(optiondict['rmv_dir'], optiondict['out_dir'])
        
    def test_validate_inputs_p07_src_set_some_others_not(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # clear the value
        optiondict['src_dir'] = 'srcdir'
        # set a value to just get a value set
        optiondict['dst_fname'] = 'something'
        # set other values
        setflds = ('out_dir', 'rmv_dir', 'add_dir', 'fmt_dir')
        add_rmv_flds = ('add_dir', 'rmv_dir')
        for fld in setflds:
            optiondict[fld] = 'diffdir'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        # check all things match
        for fld in ('src_dir', 'dst_dir', 'out_dir', 'rmv_dir', 'add_dir', 'fmt_dir'):
            if fld in setflds:
                self.assertEqual(optiondict[fld], 'diffdir/')
            elif ('dst_dir' in setflds or 'out_dir' in setflds) and fld in add_rmv_flds:
                # add remove track dst or out
                self.assertEqual(optiondict[fld], 'diffdir/')
            else:
                self.assertEqual(optiondict[fld], 'srcdir/')
        
    def test_validate_inputs_p08_src_set_some_others_not(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # clear the value
        optiondict['src_dir'] = 'srcdir'
        # set a value to just get a value set
        optiondict['dst_fname'] = 'something'
        # set other values
        setflds = ('dst_dir', 'fmt_dir')
        add_rmv_flds = ('add_dir', 'rmv_dir')
        for fld in setflds:
            optiondict[fld] = 'diffdir'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        # check all things match
        for fld in ('src_dir', 'dst_dir', 'out_dir', 'rmv_dir', 'add_dir', 'fmt_dir'):
            if fld in setflds:
                self.assertEqual(optiondict[fld], 'diffdir/')
            elif ('dst_dir' in setflds or 'out_dir' in setflds) and fld in add_rmv_flds:
                # add remove track dst or out
                self.assertEqual(optiondict[fld], 'diffdir/')
            else:
                self.assertEqual(optiondict[fld], 'srcdir/')
        
    def test_validate_inputs_p09_src_set_some_others_not(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # clear the value
        optiondict['src_dir'] = 'srcdir'
        # set a value to just get a value set
        optiondict['dst_fname'] = 'something'
        # set other values
        setflds = ('add_dir', 'fmt_dir')
        add_rmv_flds = ('add_dir', 'rmv_dir')
        for fld in setflds:
            optiondict[fld] = 'diffdir'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        # check all things match
        for fld in ('src_dir', 'dst_dir', 'out_dir', 'rmv_dir', 'add_dir', 'fmt_dir'):
            if fld in setflds:
                self.assertEqual(optiondict[fld], 'diffdir/')
            elif ('dst_dir' in setflds or 'out_dir' in setflds) and fld in add_rmv_flds:
                # add remove track dst or out
                self.assertEqual(optiondict[fld], 'diffdir/')
            else:
                self.assertEqual(optiondict[fld], 'srcdir/')
        
    def test_validate_inputs_p10_default_fname_valid(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # make sure there is a value for this defautl_fname
        optiondict['dst_fname'] = 'default-filename.txt'
        # set the command line
        self.assertTrue(copy_comments.validate_inputs(optiondict))
        
    def test_validate_inputs_p11_default_fname_invalid(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        optiondict['default_fname'] = 'invalid'
        # make sure there is a value for this defautl_fname
        optiondict['dst_fname'] = 'default-filename.txt'
        # set the command line
        self.assertFalse(copy_comments.validate_inputs(optiondict))
        self.assertTrue('error_msg' in optiondict)
        
    def test_validate_inputs_p12_set_append_fname(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        # set the command line
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set the default filename
        optiondict['dst_fname'] = 'default-filename.txt'
        # set the append variable
        for fld in ['rmv', 'add', 'out']:
             optiondict[fld+'_fname_append'] = '-001'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        # check values
        for fld in ['rmv', 'add', 'out']:
             self.assertEqual(optiondict[fld+'_fname'], 'default-filename-001.txt')

        
    def test_validate_inputs_p13_src_fname_glob_set(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        # set the command line
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set the default filename
        optiondict['dst_fname'] = 'default-filename.txt'
        # set the default glob
        optiondict['src_fname_glob'] = 't_copy_comments*.py'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        # check values
        self.assertEqual(optiondict['src_fname'], 't_copy_comments.py')

        
    def test_validate_inputs_p14_dst_fname_glob_set(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        # set the command line
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set the default filename
        optiondict['dst_fname'] = 'default-filename.txt'
        # set the default glob
        optiondict['dst_fname_glob'] = 't_copy_comments*.py'
        # set the command line
        copy_comments.validate_inputs(optiondict)
        # check values
        self.assertEqual(optiondict['dst_fname'], 't_copy_comments.py')

    def test_validate_inputs_p15_key_fields_not_set(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set the default filename
        optiondict['dst_fname'] = 'default-filename.txt'
        # remove key_fields from the dict
        del optiondict['key_fields']
        # set the command line
        self.assertFalse(copy_comments.validate_inputs(optiondict))
        self.assertTrue('error_msg' in optiondict)
        
    def test_validate_inputs_p16_key_fields_not_list(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set the default filename
        optiondict['dst_fname'] = 'default-filename.txt'
        # key_fields not list
        optiondict['key_fields'] = 'string'
        # set the command line
        self.assertFalse(copy_comments.validate_inputs(optiondict))
        self.assertTrue('error_msg' in optiondict)
        
    def test_validate_inputs_p17_key_fields_is_list(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set the default filename
        optiondict['dst_fname'] = 'default-filename.txt'
        # key_fields not list
        optiondict['key_fields'] = ['fld1', 'fld2']
        # set the command line
        self.assertTrue(copy_comments.validate_inputs(optiondict))

    # def test_validate_inputs_p20-thru-p30_internal_copy_fields_tests(self):
    # def test_validate_inputs_p30-thru-p40_internal_compare_fields_tests(self):

    
    def test_validate_inputs_p41_force_copy_flds_not_copy_flds(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set the default filename
        optiondict['dst_fname'] = 'default-filename.txt'
        # key_fields not list
        optiondict['force_copy_flds'] = True
        # set the command line
        self.assertFalse(copy_comments.validate_inputs(optiondict))
        self.assertTrue('error_msg' in optiondict)
        
    def test_validate_inputs_p42_force_copy_flds_copy_flds_not_list(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set the default filename
        optiondict['dst_fname'] = 'default-filename.txt'
        # key_fields not list
        optiondict['force_copy_flds'] = True
        optiondict['copy_fields'] = 'string'
        # set the command line
        self.assertFalse(copy_comments.validate_inputs(optiondict))
        self.assertTrue('error_msg' in optiondict)
        
        
    def test_validate_inputs_p43_force_copy_flds_copy_flds_empty_list(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set the default filename
        optiondict['dst_fname'] = 'default-filename.txt'
        # key_fields not list
        optiondict['force_copy_flds'] = True
        optiondict['copy_fields'] = []
        # set the command line
        self.assertFalse(copy_comments.validate_inputs(optiondict))
        self.assertTrue('error_msg' in optiondict)
        
        
    def test_load_records_f01_wrong_srctype(self):
        with self.assertRaises(Exception) as context:
            t_kvutil.set_argv(1,'test=test')
            optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
            # set the default filename
            optiondict['dst_fname'] = 'default-filename.txt'
            # process the command line
            copy_comments.validate_inputs(optiondict)
            # now load the records
            copy_comments.load_records(optiondict, 'badvalue')

    def test_load_records_f02_missing_src_dir(self):
        with self.assertRaises(Exception) as context:
            t_kvutil.set_argv(1,'test=test')
            optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
            # set the default filename
            optiondict['dst_fname'] = 'default-filename.txt'
            # process the command line
            copy_comments.validate_inputs(optiondict)
            # remove dir
            del optiondict['src_dir']
            # now load the records
            copy_comments.load_records(optiondict, 'src')

    def test_load_records_f03_missing_src_fname(self):
        with self.assertRaises(Exception) as context:
            t_kvutil.set_argv(1,'test=test')
            optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
            # set the default filename
            optiondict['dst_fname'] = 'default-filename.txt'
            # process the command line
            copy_comments.validate_inputs(optiondict)
            # remove dir
            del optiondict['src_fname']
            # now load the records
            copy_comments.load_records(optiondict, 'src')

    def test_validate_missing_columns_p01_all_columns_there(self):
        optiondict = {'req_cols': ['a','b','c']}
        loaded_data = [{'a':1, 'b': 2, 'c': 3, 'd': 4}]
        self.assertEqual(copy_comments.validate_missing_columns(loaded_data, optiondict, 'req_cols'), [])
        
    def test_validate_missing_columns_p02_missing_columns(self):
        optiondict = {'req_cols': ['a','b','e', 'f']}
        loaded_data = [{'a':1, 'b': 2, 'c': 3, 'd': 4}]
        self.assertEqual(copy_comments.validate_missing_columns(loaded_data, optiondict, 'req_cols'), ['e', 'f'])


    def test_validate_src_to_dst_actions_p01_set_actions_in_optiondict(self):
        optiondict = {'key_fields': ['a','b']}
        src_data = []
        dst_data = []
        matched_recs, updated_recs, src_lookup = copy_comments.src_to_dst_actions(src_data, dst_data, optiondict)
        for fld in ['copy_fields', 'internal_copy_fields', 'internal_compare_fields']:
            self.assertTrue(fld in optiondict)
            self.assertTrue(optiondict[fld] is None)
        self.assertEqual(matched_recs, 0)
        self.assertEqual(updated_recs, 0)
        self.assertEqual(src_lookup, {})

    def test_validate_src_to_dst_actions_p02_set_actions_create_lookup(self):
        optiondict = {'key_fields': ['a','b']}
        src_data = [{'a': 1, 'b': 2, 'c': 3}, {'a':2, 'b': 2, 'c': 3}]
        dst_data = []
        src_result = {1: {2: {'a': 1, 'b': 2, 'c': 3}}, 2: {2: {'a': 2, 'b': 2, 'c': 3}}}
        matched_recs, updated_recs, src_lookup = copy_comments.src_to_dst_actions(src_data, dst_data, optiondict)
        for fld in ['copy_fields', 'internal_copy_fields', 'internal_compare_fields']:
            self.assertTrue(fld in optiondict)
            self.assertTrue(optiondict[fld] is None)
        self.assertEqual(matched_recs, 0)
        self.assertEqual(updated_recs, 0)
        self.assertEqual(src_lookup, src_result)
        
            
    def test_validate_src_to_dst_actions_p03_internal_copy_src_not_blank(self):
        optiondict = {
            'key_fields': ['a','b'],
            'internal_copy_fields':[
                {'src': 'd', 'dst': 'c', 'src_not_blank': True}
            ]
        }
        src_data = [{'a': 1, 'b': 2, 'c': 3, 'd': ''}, {'a':2, 'b': 2, 'c': 3, 'd': 4}]
        dst_data = [{'a': 1, 'b': 2, 'c': 3, 'd': ''}, {'a':2, 'b': 2, 'c': 3, 'd': 4}]
        dst_result = [{'a': 1, 'b': 2, 'c': 3, 'd': ''}, {'a':2, 'b': 2, 'c': 4, 'd': 4}]
        matched_recs, updated_recs, src_lookup = copy_comments.src_to_dst_actions(src_data, dst_data, optiondict)
        self.assertEqual(dst_data, dst_result)
        
    def test_validate_src_to_dst_actions_p04_internal_copy_is_blank_no_update(self):
        optiondict = {
            'key_fields': ['a','b'],
            'internal_copy_fields':[
                {'src': 'd', 'dst': 'c', 'is_blank': True}
            ]
        }
        src_data = [{'a': 1, 'b': 2, 'c': 3, 'd': ''}, {'a':2, 'b': 2, 'c': 3, 'd': 4}]
        dst_data = [{'a': 1, 'b': 2, 'c': 3, 'd': ''}, {'a':2, 'b': 2, 'c': 3, 'd': 4}]
        dst_result = [{'a': 1, 'b': 2, 'c': 3, 'd': ''}, {'a':2, 'b': 2, 'c': 3, 'd': 4}]
        matched_recs, updated_recs, src_lookup = copy_comments.src_to_dst_actions(src_data, dst_data, optiondict)
        self.assertEqual(dst_data, dst_result)
        
            
    def test_validate_src_to_dst_actions_p05_internal_copy_is_blank_update(self):
        optiondict = {
            'key_fields': ['a','b'],
            'internal_copy_fields':[
                {'src': 'd', 'dst': 'c', 'is_blank': True}
            ]
        }
        src_data = [{'a': 1, 'b': 2, 'c': 3, 'd': ''}, {'a':2, 'b': 2, 'c': 3, 'd': 4}]
        dst_data = [{'a': 1, 'b': 2, 'c': '', 'd': None}, {'a':2, 'b': 2, 'c': '', 'd': 4}]
        dst_result = [{'a': 1, 'b': 2, 'c': None, 'd': None}, {'a':2, 'b': 2, 'c': 4, 'd': 4}]
        matched_recs, updated_recs, src_lookup = copy_comments.src_to_dst_actions(src_data, dst_data, optiondict)
        self.assertEqual(dst_data, dst_result)
        
            
    def test_validate_src_to_dst_actions_p06_internal_copy_is_blank_src_not_blank_update(self):
        optiondict = {
            'key_fields': ['a','b'],
            'internal_copy_fields':[
                {'src': 'd', 'dst': 'c', 'is_blank': True, 'src_not_blank': True}
            ]
        }
        src_data = [{'a': 1, 'b': 2, 'c': 3, 'd': ''}, {'a':2, 'b': 2, 'c': 3, 'd': 4}]
        dst_data = [{'a': 1, 'b': 2, 'c': '', 'd': None}, {'a':2, 'b': 2, 'c': '', 'd': 4}]
        dst_result = [{'a': 1, 'b': 2, 'c': '', 'd': None}, {'a':2, 'b': 2, 'c': 4, 'd': 4}]
        matched_recs, updated_recs, src_lookup = copy_comments.src_to_dst_actions(src_data, dst_data, optiondict)
        self.assertEqual(dst_data, dst_result)
        
            
    def test_validate_src_to_dst_actions_f01_missing_key_fields(self):
        with self.assertRaises(Exception) as context:
            # now load the records
            optiondict = {}
            src_data = [{'a': 1, 'b': 2, 'c': 3}, {'a':2, 'b': 2, 'c': 3}]
            dst_data = []
            src_result = {1: {2: {'a': 1, 'b': 2, 'c': 3}}, 2: {2: {'a': 2, 'b': 2, 'c': 3}}}
            matched_recs, updated_recs, src_lookup = copy_comments.src_to_dst_actions(src_data, dst_data, optiondict)

    def test_validate_src_to_dst_actions_f02_key_fields_wrong_type(self):
        with self.assertRaises(Exception) as context:
            # now load the records
            optiondict = {'key_fields': 'string'}
            src_data = [{'a': 1, 'b': 2, 'c': 3}, {'a':2, 'b': 2, 'c': 3}]
            dst_data = []
            src_result = {1: {2: {'a': 1, 'b': 2, 'c': 3}}, 2: {2: {'a': 2, 'b': 2, 'c': 3}}}
            matched_recs, updated_recs, src_lookup = copy_comments.src_to_dst_actions(src_data, dst_data, optiondict)


if __name__ == '__main__':
    unittest.main()

#eof
