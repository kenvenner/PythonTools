import kvutil
import t_kvutil
import sys

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
        

    ########################################
    # the function name: def test_optiondict_must_set(optiondict):
    def test_test_optiondict_must_set_p01_outdir_sets_rmvdir(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # override values for the test
        optiondict['rmv_dir'] = None
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['rmv_dir'], optiondict['src_dir'])
    def test_test_optiondict_must_set_p02_outdir_notsets_rmvdir(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # override values for the test
        optiondict['rmv_dir'] = 'it_set'
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['rmv_dir'], 'it_set/')
    def test_test_optiondict_must_set_p03_srcdir_sets_rmv_out_dst_dir(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # override values for the test
        optiondict['rmv_dir'] = None
        optiondict['out_dir'] = None
        optiondict['dst_dir'] = None
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['rmv_dir'], optiondict['src_dir'])
        self.assertEqual(optiondict['dst_dir'], optiondict['src_dir'])
        self.assertEqual(optiondict['out_dir'], optiondict['src_dir'])
    def test_test_optiondict_must_set_p03_srcdir_nosets_rmv_out_dst_dir(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # override values for the test
        optiondict['rmv_dir'] = 'it_set'
        optiondict['out_dir'] = 'it_set'
        optiondict['dst_dir'] = 'it_set'
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['rmv_dir'], 'it_set/')
        self.assertEqual(optiondict['dst_dir'], 'it_set/')
        self.assertEqual(optiondict['out_dir'], 'it_set/')
    def test_test_optiondict_must_set_p04_fix_dir_endings(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # override values for the test
        optiondict['src_dir'] = 'it_set\\'
        optiondict['rmv_dir'] = 'it_set\\'
        optiondict['out_dir'] = 'it_set\\'
        optiondict['dst_dir'] = 'it_set\\'
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['src_dir'], 'it_set/')
        self.assertEqual(optiondict['rmv_dir'], 'it_set/')
        self.assertEqual(optiondict['dst_dir'], 'it_set/')
        self.assertEqual(optiondict['out_dir'], 'it_set/')
    def test_test_optiondict_must_set_p05_fix_space_no_dir(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # override values for the test
        optiondict['src_dir'] = 'it_set '
        optiondict['rmv_dir'] = 'it_set '
        optiondict['out_dir'] = 'it_set '
        optiondict['dst_dir'] = 'it_set '
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['src_dir'], 'it_set/')
        self.assertEqual(optiondict['rmv_dir'], 'it_set/')
        self.assertEqual(optiondict['dst_dir'], 'it_set/')
        self.assertEqual(optiondict['out_dir'], 'it_set/')
    def test_test_optiondict_must_set_p06_fix_space_with_dir(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # override values for the test
        optiondict['src_dir'] = 'it_set\\ '
        optiondict['rmv_dir'] = 'it_set\\ '
        optiondict['out_dir'] = 'it_set\\ '
        optiondict['dst_dir'] = 'it_set\\ '
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['src_dir'], 'it_set/')
        self.assertEqual(optiondict['rmv_dir'], 'it_set/')
        self.assertEqual(optiondict['dst_dir'], 'it_set/')
        self.assertEqual(optiondict['out_dir'], 'it_set/')
    def test_test_optiondict_must_set_p07_calc_outfname(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # set override value
        optiondict['out_fname_append'] = '_out'
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['out_fname'], 'dstfname_out.xlsx')
    def test_test_optiondict_must_set_p07_calc_rmvfname(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # set override value
        optiondict['rmv_fname_append'] = '_out'
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['rmv_fname'], 'dstfname_out.xlsx')
    def test_test_optiondict_must_set_p07_calc_rmvfname_rmvuniqtype(self):
        # get the defaults
        t_kvutil.set_argv(1,'test=test')
        optiondict = kvutil.kv_parse_command_line( copy_comments.optiondictconfig ) # , keymapdict=keymapdict )
        # set fnames
        optiondict['src_fname'] = 'srcfname.xlsx'
        optiondict['dst_fname'] = 'dstfname.xlsx'
        # set override value
        optiondict['rmv_fname_append'] = '_out'
        optiondict['rmv_fname_uniqtype'] = 'cnt'
        optiondict['rmv_dir'] = '.'
        # set the command line
        copy_comments.test_optiondict_must_set(optiondict)
        self.assertEqual(optiondict['rmv_fname'], 'dstfname_outv01.xlsx')


if __name__ == '__main__':
    unittest.main()

#eof
