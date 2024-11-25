import kvutil

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
    # the function name: def set_optiondict_directories(optiondict):
    def test_test_optiondict_must_set_p01_pass(self):
        optiondict = {
            'src_dir': '/bin1',
            'dst_dir': '/bin2',
            'out_dir': '/bin3',
            'src_fname': 'src_fname',
            'dst_fname': 'dst_fname',
        }
        result = [
        ]
        self.assertEqual(copy_comments.test_optiondict_must_set(optiondict),
                         result)

    def test_test_optiondict_must_set_f01_blank_src_dir(self):
        optiondict = {
            'src_dir': '',
            'dst_dir': '/bin2',
            'out_dir': '/bin3',
            'src_fname': 'src_fname',
            'dst_fname': 'dst_fname',
        }
        result = [
            'ERROR: [src_dir] no value defined in optiondict'
        ]
        self.assertEqual(copy_comments.test_optiondict_must_set(optiondict),
                         result)

    def test_test_optiondict_must_set_f02_blank_dst_dir(self):
        optiondict = {
            'src_dir': '/bin1',
            'dst_dir': '',
            'out_dir': '/bin3',
            'src_fname': 'src_fname',
            'dst_fname': 'dst_fname',
        }
        result = [
            'ERROR: [dst_dir] no value defined in optiondict'
        ]
        self.assertEqual(copy_comments.test_optiondict_must_set(optiondict),
                         result)

    def test_test_optiondict_must_set_f03_missing_src_dir(self):
        optiondict = {
            'dst_dir': '/bin2',
            'out_dir': '/bin3',
            'src_fname': 'src_fname',
            'dst_fname': 'dst_fname',
        }
        result = [
            'ERROR: [src_dir] not defined in optiondict'
        ]
        self.assertEqual(copy_comments.test_optiondict_must_set(optiondict),
                         result)

    def test_test_optiondict_must_set_f04_missin_dst_dir(self):
        optiondict = {
            'src_dir': '/bin1',
            'out_dir': '/bin3',
            'src_fname': 'src_fname',
            'dst_fname': 'dst_fname',
        }
        result = [
            'ERROR: [dst_dir] not defined in optiondict'
        ]
        self.assertEqual(copy_comments.test_optiondict_must_set(optiondict),
                         result)
    def test_test_optiondict_must_set_f05_blank_src_fname(self):
        optiondict = {
            'src_dir': '/bin1',
            'dst_dir': '/bin2',
            'out_dir': '/bin3',
            'src_fname': '',
            'dst_fname': 'dst_fname',
        }
        result = [
            'ERROR: [src_fname] no value defined in optiondict'
        ]
        self.assertEqual(copy_comments.test_optiondict_must_set(optiondict),
                         result)

    def test_test_optiondict_must_set_f02_blank_dst_fname(self):
        optiondict = {
            'src_dir': '/bin1',
            'dst_dir': '/bin2',
            'out_dir': '/bin3',
            'src_fname': 'src_name',
            'dst_fname': '',
        }
        result = [
            'ERROR: [dst_fname] no value defined in optiondict'
        ]
        self.assertEqual(copy_comments.test_optiondict_must_set(optiondict),
                         result)

    def test_test_optiondict_must_set_f03_missing_src_fname(self):
        optiondict = {
            'src_dir': '/bin1',
            'dst_dir': '/bin2',
            'out_dir': '/bin3',
            'dst_fname': 'dst_fname',
        }
        result = [
            'ERROR: [src_fname] not defined in optiondict'
        ]
        self.assertEqual(copy_comments.test_optiondict_must_set(optiondict),
                         result)

    def test_test_optiondict_must_set_f04_missin_dst_fname(self):
        optiondict = {
            'src_dir': '/bin1',
            'dst_dir': '/bin2',
            'out_dir': '/bin3',
            'src_fname': 'src_fname',
        }
        result = [
            'ERROR: [dst_fname] not defined in optiondict'
        ]
        self.assertEqual(copy_comments.test_optiondict_must_set(optiondict),
                         result)

    ########################################
    # the function name: def set_optiondict_directories(optiondict):
    def test_set_optiondict_directories_p01_pass(self):
        optiondict = {
            'src_dir': '/bin1',
            'dst_dir': '/bin2',
            'out_dir': '/bin3',
        }
        resultdict = {
            'src_dir': '/bin1',
            'dst_dir': '/bin2',
            'out_dir': '/bin3',
        }
        copy_comments.set_optiondict_directories(optiondict)
        self.assertEqual(optiondict, resultdict)

    def test_set_optiondict_directories_p02_pass(self):
        optiondict = {
            'src_dir': '/bin1',
            'dst_dir': '',
            'out_dir': '',
        }
        resultdict = {
            'src_dir': '/bin1',
            'dst_dir': '/bin1',
            'out_dir': '/bin1',
        }
        copy_comments.set_optiondict_directories(optiondict)
        self.assertEqual(optiondict, resultdict)

    def test_set_optiondict_directories_p03_pass(self):
        optiondict = {
            'src_dir': '/bin1',
            'dst_dir': '',
            'out_dir': '/bin3',
        }
        resultdict = {
            'src_dir': '/bin1',
            'dst_dir': '/bin1',
            'out_dir': '/bin3',
        }
        copy_comments.set_optiondict_directories(optiondict)
        self.assertEqual(optiondict, resultdict)

    ########################################
    # the function name: def set_optiondict_dir_char(optiondict):
    def test_set_optiondict_dir_char_p01_pass(self):
        optiondict = {
            'src_dir': '/bin',
            'dst_dir': '/bin',
            'out_dir': '/bin',
        }
        resultdict = {
            'src_dir': '/bin/',
            'dst_dir': '/bin/',
            'out_dir': '/bin/'
        }
        copy_comments.set_optiondict_dir_char(optiondict)
        self.assertEqual(optiondict, resultdict)

    def test_set_optiondict_dir_char_p02_pass(self):
        optiondict = {
            'src_dir': '/bin',
            'dst_dir': '/bin/',
            'out_dir': '/bin',
        }
        resultdict = {
            'src_dir': '/bin/',
            'dst_dir': '/bin/',
            'out_dir': '/bin/'
        }
        copy_comments.set_optiondict_dir_char(optiondict)
        self.assertEqual(optiondict, resultdict)

    ########################################
    # the function name: def test_optiondict_out_fname(optiondict):
    def test_test_optiondict_out_fname_p01_pass(self):
        optiondict = {
            'out_fname': 'test.txt',
            'out_fname_append': '',
            'dst_fname': ''
        }
        resultdict = {
            'out_fname': 'test.txt',
            'out_fname_append': '',
            'dst_fname': ''
        }
        copy_comments.test_optiondict_out_fname(optiondict)
        self.assertEqual(optiondict, resultdict)
        
    def test_test_optiondict_out_fname_p02_append(self):
        optiondict = {
            'out_fname': '',
            'out_fname_append': 'map',
            'dst_fname': './test.txt'
        }
        resultdict = {
            'out_fname': './testmap.txt',
            'out_fname_append': 'map',
            'dst_fname': './test.txt'
        }
        copy_comments.test_optiondict_out_fname(optiondict)
        self.assertEqual(optiondict, resultdict)
        
    ########################################
    # the function name: def test_optiondict_rmv_fname(optiondict):
    def test_test_optiondict_rmv_fname_p01_pass(self):
        optiondict = {
            'dst_fname': './test.txt',
            'rmv_fname_append': '_rmv'
        }
        resultdict = {
            'dst_fname': './test.txt',
            'rmv_fname_append': '_rmv',
            'rmv_fname': './test_rmv.txt'
        }
        copy_comments.test_optiondict_rmv_fname(optiondict)
        self.assertEqual(optiondict, resultdict)

    def test_test_optiondict_rmv_fname_p02_no_rmv_fname_append(self):
        optiondict = {
            'dst_fname': './test.txt',
            'rmv_fname_append': ''
        }
        resultdict = {
            'dst_fname': './test.txt',
            'rmv_fname_append': '',
        }
        copy_comments.test_optiondict_rmv_fname(optiondict)
        self.assertEqual(optiondict, resultdict)

    ########################################
    # the function name: def test_optiondict_internal_copy_field(optiondict):
    def test_test_optiondict_internal_copy_field_p01_pass(self):
        optiondict = {
            'internal_copy_fields': [
                {'src': 'src_fld', 'dst': 'dst_fld', 'is_blank': False}
            ]
        }
        resultdict = {
            'internal_copy_fields': [
                {'src': 'src_fld', 'dst': 'dst_fld', 'is_blank': False}
            ]
        }
        copy_comments.test_optiondict_internal_copy_field(optiondict)
        self.assertEqual(optiondict, resultdict)
        
    def test_test_optiondict_internal_copy_field_p02_set_is_blank(self):
        optiondict = {
            'internal_copy_fields': [
                {'src': 'src_fld', 'dst': 'dst_fld'}
            ]
        }
        resultdict = {
            'internal_copy_fields': [
                {'src': 'src_fld', 'dst': 'dst_fld', 'is_blank': True}
            ]
        }
        copy_comments.test_optiondict_internal_copy_field(optiondict)
        self.assertEqual(optiondict, resultdict)
        
    def test_test_optiondict_internal_copy_field_p03_not_filled(self):
        optiondict = {
            'internal_copy_fields': [
            ]
        }
        resultdict = {
            'internal_copy_fields': [
            ]
        }
        copy_comments.test_optiondict_internal_copy_field(optiondict)
        self.assertEqual(optiondict, resultdict)
        
    def test_test_optiondict_internal_copy_field_p03_not_there(self):
        optiondict = {
        }
        resultdict = {
            'internal_copy_fields': [
            ]
        }
        copy_comments.test_optiondict_internal_copy_field(optiondict)
        self.assertEqual(optiondict, resultdict)
        
    def test_test_optiondict_internal_copy_field_p04_dict_to_list(self):
        optiondict = {
            'internal_copy_fields':
                {'src': 'src_fld', 'dst': 'dst_fld', 'is_blank': False}
        }
        resultdict = {
            'internal_copy_fields': [
                {'src': 'src_fld', 'dst': 'dst_fld', 'is_blank': False}
            ]
        }
        copy_comments.test_optiondict_internal_copy_field(optiondict)
        self.assertEqual(optiondict, resultdict)
        
    def test_test_optiondict_internal_copy_field_f01_no_src(self):
        optiondict = {
            'internal_copy_fields': [
                {'dst': 'dst_fld', 'is_blank': False}
            ]
        }
        resulterrors = ["ERROR:  internal_copy_fields [1] missing required key [src]: {'dst': 'dst_fld', 'is_blank': False}"]
        errors = copy_comments.test_optiondict_internal_copy_field(optiondict)
        self.assertEqual(errors, resulterrors)
        
        
    def test_test_optiondict_internal_copy_field_f02_no_dst(self):
        optiondict = {
            'internal_copy_fields': [
                {'dst': 'dst_fld', 'is_blank': False}
            ]
        }
        resulterrors = ["ERROR:  internal_copy_fields [1] missing required key [src]: {'dst': 'dst_fld', 'is_blank': False}"]
        errors = copy_comments.test_optiondict_internal_copy_field(optiondict)
        self.assertEqual(errors, resulterrors)
        
        
    ########################################
    # the function name: def test_optiondict_settings_pre(optiondict):
    def test_test_optiondict_settings_pre_p01_pass(self):
        # nothing to test
        pass
    
    ########################################
    # the function name: def test_optiondict_src_data(optiondict, src_data, dst_data):
    def test_test_optiondict_src_data_p01_pass(self):
        optiondict = {
            'key_fields': ['fld1', 'fld2'],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = []
        errors = copy_comments.test_optiondict_src_data(optiondict, src_data, [])
        self.assertEqual(errors, resulterrors)

    def test_test_optiondict_src_data_f01_no_src_recs(self):
        optiondict = {
            'key_fields': ['fld1', 'fld2'],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
        ]
        resulterrors = ['ERROR:  Found no records in: ./text.txt']
        errors = copy_comments.test_optiondict_src_data(optiondict, src_data, [])
        self.assertEqual(errors, resulterrors)

    def test_test_optiondict_src_data_f02_missing_key_fields(self):
        optiondict = {
            'key_fields': ['fld1', 'fld2'],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld2': 'val2'}
        ]
        resulterrors = ['ERROR:  You are MOST LIKELY reading in the wrong sheet as we can not find column: fld1']
        errors = copy_comments.test_optiondict_src_data(optiondict, src_data, [])
        self.assertEqual(errors, resulterrors)


    def test_test_optiondict_src_data_f03_missing_fields(self):
        optiondict = {
            'key_fields': ['fld1', 'fld2', 'fld3'],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = ['ERROR:  src_data record 1 is missing field: fld3']
        errors = copy_comments.test_optiondict_src_data(optiondict, src_data, [])
        self.assertEqual(errors, resulterrors)


    ########################################
    # the function name: def test_optiondict_src_data_copy_fields(optiondict, src_data, dst_data):
    def test_test_optiondict_src_data_copy_fields_p01_pass(self):
        optiondict = {
            'copy_fields': ['fld1', 'fld2'],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = []
        errors = copy_comments.test_optiondict_src_data_copy_fields(optiondict, src_data, [])
        self.assertEqual(errors, resulterrors)
        
    def test_test_optiondict_src_data_copy_fields_p02_empty_copy_fields(self):
        optiondict = {
            'copy_fields': [],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = []
        errors = copy_comments.test_optiondict_src_data_copy_fields(optiondict, src_data, [])
        self.assertEqual(errors, resulterrors)
        
    def test_test_optiondict_src_data_copy_fields_p03_no_copy_fields(self):
        optiondict = {
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = []
        errors = copy_comments.test_optiondict_src_data_copy_fields(optiondict, src_data, [])
        self.assertEqual(errors, resulterrors)
        
    def test_test_optiondict_src_data_copy_fields_f01_missing_fld(self):
        optiondict = {
            'copy_fields': ['fld1', 'fld2', 'fld3'],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = ['ERRORS:  Source record missing a copy column: fld3']
        errors = copy_comments.test_optiondict_src_data_copy_fields(optiondict, src_data, [])
        self.assertEqual(errors, resulterrors)
        

    
    ########################################
    # the function name: def test_optiondict_src_data_internal_copy_fields(optiondict, src_data, dst_data):
    def test_test_optiondict_src_data_internal_copy_fields_p01_pass(self):
        optiondict = {
            'internal_copy_fields': [
                {'src': 'fld1', 'dst': 'fld2', 'is_blank': False}
            ],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        dst_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = []
        errors = copy_comments.test_optiondict_src_data_internal_copy_fields(optiondict, src_data, dst_data)
        self.assertEqual(errors, resulterrors)
        
    def test_test_optiondict_src_data_internal_copy_fields_p02_empty_copy_fields(self):
        optiondict = {
            'internal_copy_fields': [],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        dst_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = []
        errors = copy_comments.test_optiondict_src_data_internal_copy_fields(optiondict, src_data, dst_data)
        self.assertEqual(errors, resulterrors)
        
    def test_test_optiondict_src_data_internal_copy_fields_p03_no_copy_fields(self):
        optiondict = {
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        dst_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = []
        errors = copy_comments.test_optiondict_src_data_internal_copy_fields(optiondict, src_data, dst_data)
        self.assertEqual(errors, resulterrors)
        
    def test_test_optiondict_src_data_internal_copy_fields_f01_missing_fld(self):
        optiondict = {
            'internal_copy_fields': [
                {'src': 'fld1', 'dst': 'fld3', 'is_blank': False}
            ],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        dst_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = ["ERROR:  internal_copy_fields dst record missing a copy column in record 0: fld3|{'src': 'fld1', 'dst': 'fld3', 'is_blank': False}"]
        errors = copy_comments.test_optiondict_src_data_internal_copy_fields(optiondict, src_data, dst_data)
        self.assertEqual(errors, resulterrors)
        
        
    ########################################
    # the function name: def display_dump_recs(optiondict, src_data, dst_data):
    def test_display_dump_recs_p01_pass(self):
        pass

    ########################################
    # the function name: def test_optiondict_force_copy_flds(optiondict, src_data, dst_data):
    def test_test_optiondict_force_copy_flds_p01_pass(self):
        optiondict = {
            'force_copy_flds': True,
            'copy_fields': ['fld1', 'fld2'],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        dst_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        results_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        resulterrors = []
        errors = copy_comments.test_optiondict_force_copy_flds(optiondict, src_data, dst_data)
        self.assertEqual(dst_data, results_data)

    def test_test_optiondict_force_copy_flds_p02_add_fld(self):
        optiondict = {
            'force_copy_flds': True,
            'copy_fields': ['fld1', 'fld2', 'fld3'],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2', 'fld3': 'val3'}
        ]
        dst_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        results_data = [
            {'fld1': 'val1', 'fld2': 'val2', 'fld3': ''}
        ]
        resulterrors = []
        errors = copy_comments.test_optiondict_force_copy_flds(optiondict, src_data, dst_data)
        self.assertEqual(dst_data, results_data)

        
        
    ########################################
    # the function name: def test_optiondict_src_data_hyperlink(optiondict, src_data, dst_data):
    def test_test_optiondict_src_data_hyperlink_p01_pass(self):
        pass

    
    ########################################
    # the function name: def set_optiondict_src_data_set_blank(optiondict, src_data, dst_data):
    def test_set_optiondict_src_data_set_blank_p01_pass(self):
        pass
    
    ########################################
    # the function name: def test_optiondict_dst_data_internal_copy_fields(optiondict, src_data, dst_data):
    def test_test_optiondict_dst_data_internal_copy_fields_p01_pass(self):
        optiondict = {
            'internal_copy_fields': [
                {'src': 'fld1', 'dst': 'fld3', 'is_blank': False}
            ],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        dst_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        result_data = [
            {'fld1': 'val1', 'fld2': 'val2', 'fld3': 'val1'}
        ]
        errors = copy_comments.test_optiondict_dst_data_internal_copy_fields(optiondict, src_data, dst_data)
        self.assertEqual(dst_data, result_data)
        self.assertEqual(errors, 'Copying data inside the file defined by internal_copy_fields')

    def test_test_optiondict_dst_data_internal_copy_fields_p02_no_internal(self):
        optiondict = {
            'internal_copy_fields': [
            ],
            'src_dir': './',
            'src_fname': 'text.txt'
        }
        src_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        dst_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        result_data = [
            {'fld1': 'val1', 'fld2': 'val2'}
        ]
        errors = copy_comments.test_optiondict_dst_data_internal_copy_fields(optiondict, src_data, dst_data)
        self.assertEqual(dst_data, result_data)
        self.assertEqual(errors, '')
        
    ########################################
    # the function name: def test_optiondict_settings_post(optiondict, src_data, dst_data):
    def test_test_optiondict_settings_post_p01_pass(self):
        pass

    ########################################
    # the function name: def create_rmv_data(optiondict, src_data, dst_data):
    def test_create_rmv_data_p01_pass(self):
        pass


    ########################################
    # the function name: def format_output(optiondict, src_data, dst_data):
    def test_format_output_p01_pass(self):
        pass

    ########################################
    # the function name: def format_output_cell(optiondict, src_data, dst_data):
    def test_format_output_cell_p01_pass(self):
        pass
    
    ########################################
    # the function name: def print_final_results(optiondict, src_data, dst_data):
    def test_print_final_results_p01_pass(self):
        pass

    ########################################
    # the function name: def test_process_errors(errors):
    def test_test_process_errors_p01_pass(self):
        pass


if __name__ == '__main__':
    unittest.main()

#eof
