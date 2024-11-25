"""
    Copy comments from file 1 and move them into file 2
    matching on the keys between two files

    src_dir/src_fname - the file that has the existing data that we need to copy over
    dst_dir/dst_fname - the NEW file that we read in and apply teh src_data to
    out_dir/out_fname - the output file generated after we apply src_data to dst_fname.

    out_fname_append - enables the generation of the out_fname based in teh dst_fname and append a string.

    copy_fields - list of fields from src_data that are copied into fields in dst_data
    key_fields - the list of fields in src_data and dst_data that define a unique record in the file
    set_blank_fields - a dictionary of key/value pairs - the key is the field in src_data that
                       if not populated with data - we assign the field "value" - if this is None we ignore this flow
    internal_copy_fields - list of dictionaries that define dst fields taht copy to other dst fields
                           each records is 
         {
            'src': <src_fieldname>, 
            'dst': <dst_fieldname>, 
            'if_blank': if true - only update dst field when empty - which is default
         }
    col_width - a dictionary that is column letter and column width numberic
    format_output - boolean when true we format the out_fname, with col_width if passed in or calc col_width on our own
    format_cell - boolean when true we copy the formatting of cells based on match key from src to out_fname
    src_width - when true, and format_output is true, we calculate col_width by reading the values from src_fname

@author:   Ken Venner
@contact:  ken.venner@sierrspace.com
@version:  1.10

    Created:   2024-05-20;kv
    Version:   2024-09-19;kv - more checks and additional features (like json_cfg_filename)
               2024-07-24;kv - added hyperlink_fields
               2024-06-03;kv


"""

import kvutil
import kv_excel
import kvxls
import pprint
import sys
import os


# ----------------------------------------

AppVersion = '1.10'
__version__ = '1.10'


# ----------------------------------------


# COMMAND LINE PROCESSING

optiondictconfig = {
    'AppVersion' : {
        'value': '1.10',
    },
    
    'debug' : {
        'value' : False,
        'type' : 'bool',
    },
    'src_dir' : {
        'value' : "C:/Users/116919/Sierra Space Corporation/Sierra Space Information Technology - General/Ken's Material/2024-02-13-PO-Cleanup",
        'type' : 'dir',
        'description': 'path to the file with the data to be copied from',
    },
    'dst_dir' : {
        'value' : None,
        'type' : 'dir',
        'description': 'path to the file with the data to be copied into',
    },
    'out_dir' : {
        'value' : None,
        'type' : 'dir',
        'description': 'path to the location where the output file is placed',
    },
    'src_fname' : {
        'value' : "2024-04-23-PO-IT-Cleanup-v02.xlsx",
        'description':  'filename of the file with the data to copy from',
    },
    'dst_fname' : {
        'value' : "2024-05-04-PO-IT-Cleanup.xlsx",
        'description':  'filename of the file with the data to copy into',
    },
    'out_fname' : {
        'value' : "2024-05-04-PO-IT-Cleanup-v02.xlsx",
        'description':  'filename of the output file',
    },
    'rmv_fname' : {
        'value' : "",
        'description':  'filename of the removed records output file',
    },
    'src_ws' : {
        'value' : None,
        'description':  'worksheet in the file with the data to copy from',
    },
    'dst_ws' : {
        'value' : None,
        'description':  'worksheet in the file with the data to copy into',
    },
    'out_ws' : {
        'value' : None,
        'description':  'worksheet in the output file',
    },
    'out_fname_append' : {
        'value' : "",
        'description':  'string to append to the dst_fname to create teh out_fname - do not set this and out_fname',
    },
    'rmv_fname_append' : {
        'value' : "",
        'description':  'string to append to the dst_fname to create teh rmv_fname',
    },
    'json_cfg_filename' : {
        'value' : False,
        'description': 'when populated with a filename - we create a default cfg json file',
    },
    'copy_fields' : {
        'value' : [
            'Comment',
            'NewPORequestorID',
            'NewPORequestorName',
            'NewPORequestorEmail',
        ],
        'type' : 'liststr',
        'description': 'fields in the source file that are copied over into the destination file',
    },
    'internal_copy_fields' : {
        'value' : [
        ],
        'type' : 'liststr',
        'description': 'list of dictionaries that defines what we copy inside the dst file moving column data to other columns',
    },
    'key_fields' : {
        'value' : [
            'Purchasing Document',
            'Item',
        ],
        'type' : 'liststr',
        'description': 'fields that create the unique business key in the source and destination file',
    },
    'hyperlink_fields' : {
        'value' : [
        ],
        'type' : 'liststr',
        'description': 'fields that are hyperlink fields and must be converted',
    },
    'set_blank_fields' : {
        'value' : None,
        'type' : 'dict',
        'description': 'dictionary of field and value to set if the field is not populated in the src file',
    },
    'col_width' : {
        'value': None,
        'type' : dict,
        'description' : 'dictionary defines the width for each column',
    },
    'format_output' : {
        'value' : True,
        'type' : 'bool',
        'description': 'when true we format the created out_fname',
    },
    'format_cell' : {
        'value' : True,
        'type' : 'bool',
        'description': 'when true we copy over formatting to out_fname',
    },
    'src_width' : {
        'value' : True,
        'type' : 'bool',
        'description': 'when true and format_output is true - get col_width from the src_fname',
    },
    'force_copy_flds' : {
        'value' : False,
        'type' : 'bool',
        'description': 'when enabled this force the copy fields into the dst file',
    },
    'dump_recs' : {
        'value' : False,
        'type' : 'bool',
        'description': 'when enabled this will cause the data read in to be outputted',
    }
}

'''
Documentation about the structure of col_width dictionary
Example col_width:
{
    'A': 25.0,
    'AA': 17.453125,
    'AB': 20.54296875,
    'AC': 20.1796875,
    'AD': 14.0,
    'AE': 11.7265625,
    'AF': 19.26953125,
    'AG': 23.90625,
    'AH': 11.1796875,
    'AI': 39.26953125,
    'AJ': 8.81640625,
    'AK': 6.7265625,
    'AL': 9.453125,
    'AM': 12.54296875,
    'AN': 12.453125,
    'AO': 12.1796875,
    'AP': 13.81640625,
    'AQ': 9.453125,
    'AR': 19.26953125,
    'AS': 9.0,
    'B': 40.0,
    'C': 19.08984375,
    'D': 4.81640625,
    'E': 11.81640625,
    'G': 11.453125,
    'H': 19.7265625,
    'I': 44.7265625,
    'J': 18.08984375,
    'K': 13.6328125,
    'L': 5.0,
    'M': 17.26953125,
    'N': 13.453125,
    'O': 9.6328125,
    'P': 13.6328125,
    'Q': 8.54296875,
    'R': 14.26953125,
    'S': 12.7265625,
    'T': 13.36328125,
    'U': 10.7265625,
    'V': 30.26953125,
    'W': 12.36328125,
    'X': 17.54296875,
    'Y': 23.453125,
    'Z': 39.26953125
}
'''

def test_process_errors(errors):
    '''
    pass in an array of error messages
    display them and exit the program
    '''
    if not errors:
        return
    print('\n'.errors)
    print('Program Terminated!')
    sys.exit(1)

def test_optiondict_must_set(optiondict):
    '''
    set of variables that must be set
    '''
    errors = []
    for fld in ['src_dir', 'dst_dir', 'src_fname', 'dst_fname']:
        if fld not in optiondict:
            errors.append(f"ERROR: [{fld}] not defined in optiondict")
        elif not optiondict[fld]:
            errors.append(f"ERROR: [{fld}] no value defined in optiondict")

    return errors

def set_optiondict_directories(optiondict):
    '''
    if directories are not set - set them
    '''
    
    # default fields that were not set
    # set directories to match teh src_dir if not set
    for fld in ('dst_dir', 'out_dir'):
        if not optiondict[fld]:
            optiondict[fld] = optiondict['src_dir']

def set_optiondict_dir_char(optiondict):
    ''' 
    validate the directories end with the / 
    '''
    # make sure each directory ends with '/'
    for fld in ['src_dir', 'dst_dir', 'out_dir']:
        if optiondict[fld] and optiondict[fld][-1] != '/':
            optiondict[fld] += '/'

def test_optiondict_out_fname(optiondict):
    '''
    validate the out_fname make sense
    '''
    errors = []
    # determine if we need to generate the output fname
    if optiondict['out_fname'] and optiondict['out_fname_append']:
        errors.append('ERROR:  you can not populate both attributes [out_fname] and [out_fname_append]')
    elif optiondict['out_fname_append']:
        # calculate the out_fname
        fname, fext = os.path.splitext(optiondict['dst_fname'])
        # build the new filename
        optiondict['out_fname'] = fname + optiondict['out_fname_append'] + fext
    return errors

def test_optiondict_rmv_fname(optiondict):
    '''
    build the rmv_fname variable if we set the append variable
    '''
    # generate the remove filename
    if optiondict['rmv_fname_append']:
        # calculate the out_fname
        fname, fext = os.path.splitext(optiondict['dst_fname'])
        # build the new filename
        optiondict['rmv_fname'] = fname + optiondict['rmv_fname_append'] + fext


def test_optiondict_internal_copy_field(optiondict):
    # return the errors
    errors = []
    
    # validate the structure is correct if we are copying internally
    if 'internal_copy_fields' not in optiondict:
        optiondict['internal_copy_fields'] = []

    if not optiondict['internal_copy_fields']:
        return errors
    
    # if we have a dict - it shoudl have been a list - convert to a list with one dict entry
    if type(optiondict['internal_copy_fields']) == dict:
        optiondict['internal_copy_fields'] = [optiondict['internal_copy_fields']]
        
    # this should have a list of dicts
    for idx, copydict in enumerate(optiondict['internal_copy_fields']):
        for fld in ['src', 'dst']:
            if fld not in copydict:
                errors.append(f"ERROR:  internal_copy_fields [{idx+1}] missing required key [{fld}]: " + str(copydict))
        # set the default if not set
        if 'is_blank' not in copydict:
            copydict['is_blank'] = True

    # finally if we have issue then terminate
    return errors

def test_optiondict_settings_pre(optiondict):
    '''
    Execute the test and value setting functions 
    '''
    set_optiondict_directories(optiondict)
    set_optiondict_dir_char(optiondict)
    test_process_errors(test_optiondict_out_fname(optiondict))
    test_optiondict_rmv_fname(optiondict)
    test_process_errors(test_optiondict_internal_copy_field(optiondict))


def test_optiondict_src_data(optiondict, src_data, dst_data):
    '''
    Run tests that tie off to the src_data
    '''
    errors = []
    # check that we found records
    if not len(src_data):
        errors.append('ERROR:  Found no records in: ' + optiondict['src_dir'] + optiondict['src_fname'])
        return errors
    
    # check that we got the right sheet - one of the keys is in this record
    if optiondict['key_fields'][0] not in src_data[0]:
        errors.append('ERROR:  You are MOST LIKELY reading in the wrong sheet as we can not find column: ' + str(optiondict['key_fields'][0]) )
        return errors

    # jump through all fields
    for fld in optiondict['key_fields']:
        if fld not in src_data[0]:
            errors.append('ERROR:  src_data record 1 is missing field: ' + fld )
            
    return errors

def test_optiondict_src_data_copy_fields(optiondict, src_data, dst_data):
    '''
    Run tests that tie off to the src_data copy_fields
    '''

    # check that the source records have the copy fields
    if 'copy_fields' not in optiondict or not optiondict['copy_fields']:
        return []

    # check copy_fields
    errors = []
    for fld in optiondict['copy_fields']:
        if fld not in src_data[0]:
            errors.append('ERRORS:  Source record missing a copy column: ' + fld)
    return errors

def test_optiondict_src_data_internal_copy_fields(optiondict, src_data, dst_data):
    '''
    Run tests that tie off to the src_data copy_fields
    '''

    # check the internal copy fields against dst file
    if 'internal_copy_fields' not in optiondict or not optiondict['internal_copy_fields']:
        return []

    # do the work
    errors = []
    for idx, copydict in enumerate(optiondict['internal_copy_fields']):
        for cfld in ['src', 'dst']:
            fld = copydict[cfld]
            if fld not in dst_data[0]:
                errors.append(f'ERROR:  internal_copy_fields dst record missing a copy column in record {idx}: ' + fld + '|' + str(copydict))

    return errors

def display_dump_recs(optiondict, src_data, dst_data):
    # output when requested
    if optiondict['dump_recs']:
        print('-'*80)
        print('Original Source:')
        pprint.pprint(src_data)
        print('-'*80)
        print('New Source:')
        pprint.pprint(dst_data)
        print('-'*80)
        print('\n')

def test_optiondict_force_copy_flds(optiondict, src_data, dst_data):
    # force copy fields into the dst_data records
    # make sure there is a place in the dictionary of the destination
    # record to accept the copy fields values
    if optiondict['force_copy_flds']:
        for rec in dst_data:
            for fld in optiondict['copy_fields']:
                if fld not in rec:
                    rec[fld] = ''

def test_optiondict_src_data_hyperlink(optiondict, src_data, dst_data):
    # convert hyperlink fields if defined
    if optiondict['hyperlink_fields']:
        kvutil.convert_hyperlink_field_values(src_data, optiondict['hyperlink_fields'])
        kvutil.convert_hyperlink_field_values(dst_data, optiondict['hyperlink_fields'])

def set_optiondict_src_data_set_blank(optiondict, src_data, dst_data):
    # set the values on blank entries in source file if configured
    if optiondict['set_blank_fields']:
        set_blank_rec_cnt = kvutil.set_blank_field_values(src_data, optiondict['set_blank_fields'])
    else:
        set_blank_rec_cnt = 0
    return set_blank_rec_cnt
        
def test_optiondict_dst_data_internal_copy_fields(optiondict, src_data, dst_data):
    msg = ''
    # now copy over fields interest witin the output file
    if optiondict['internal_copy_fields']:
        # message
        msg = 'Copying data inside the file defined by internal_copy_fields'
        # copy fields in the file we just read in
        for rec in dst_data:
            for copydict in optiondict['internal_copy_fields']:
                if not copydict['is_blank'] or not rec[copydict['dst']]:
                    # is_blank is False (we want to update all recrs, or dst is not populated then update from src
                    rec[copydict['dst']] = rec[copydict['src']]

    return msg

def test_optiondict_settings_post(optiondict, src_data, dst_data):
    test_process_errors(test_optiondict_src_data(optiondict, src_data, dst_data))
    test_process_errors(test_optiondict_src_data_copy_fields(optiondict, src_data, dst_data))
    test_process_errors(test_optiondict_src_data_internal_copy_fields(optiondict, src_data, dst_data))
    display_dump_recs(optiondict, src_data, dst_data)
    test_optiondict_force_copy_flds(optiondict, src_data, dst_data)
    test_optiondict_src_data_hyperlink(optiondict, src_data, dst_data)
    set_blank_rec_cnt = set_optiondict_src_data_set_blank(optiondict, src_data, dst_data)
    print(test_optiondict_dst_data_internal_copy_fields(optiondict, src_data, dst_data))
    return set_blank_rec_cnt
    

def create_rmv_data(optiondict, src_data, dst_data):
    rmv_data = []
    # if we want to save out the removed records then do that analysis
    if optiondict['rmv_fname']:
        dst_lookup = kvutil.create_multi_key_lookup(dst_data, optiondict['key_fields'])
        rmv_data = kvutil.extract_unmatched_data(src_data, dst_lookup, optiondict['key_fields'])

        if optiondict['dump_recs']:
            print('-'*80)
            print('DST Output Records:')
            pprint.pprint(dst_data)
            print('-'*80)
            
    return rmv_data


def format_output(optiondict, src_data, dst_data):
    msg = ''
    # if they want it formatted
    if not optiondict['format_output']:
        return msg

    msg += '\nFormatting output file\n'
    
    # check if we should load the col_width from the src_fname
    if optiondict['src_width']:
        msg += 'Getting col_width from src_fname\n'
        optiondict['col_width'] = kv_excel.get_existing_column_width(optiondict['src_dir'] + optiondict['src_fname'])
    #
    msg += 'Performing output formatting'
    kv_excel.format_xlsx_with_filter_and_freeze(optiondict['out_dir'] + optiondict['out_fname'], col_width=optiondict['col_width'])

    return msg

def format_output_cell(optiondict, src_data, dst_data):
    msg = ''

    # if they want to copy over formatting
    if not optiondict['format_cell']:
        return msg

    # now format
    msg += '\nCopying Cell Formatting'
    
    # debug
    # print('src file:', optiondict['src_dir'] + optiondict['src_fname'])
    
    # reading in the source
    excel_dict_src = kvxls.readxls_findheader(
        optiondict['src_dir'] + optiondict['src_fname'],
        [],
        optiondict={'col_header': True, 'keep_vba': False, 'sheetname': optiondict['dst_ws']},
        data_only=False
    )
    # reading in the destination
    excel_dict_out = kvxls.readxls_findheader(
        optiondict['out_dir'] + optiondict['out_fname'],
        [],
        optiondict={'col_header': True, 'keep_vba': False, 'sheetname': optiondict['out_ws']},
        data_only=False
    )
    # build the cross reference table
    src_lookup = kvxls.create_multi_key_lookup_excel(excel_dict_src, optiondict['key_fields'])

    # debug
    # pprint.pprint(src_lookup)

    # step through teh output and find the equivalent input and then copy over the formatting
    for row in range(excel_dict_out['row_header']+1, excel_dict_out['sheetmaxrow']):
        # step through the lookup key one level at a time to see if we
        # have a matching record
        matched = True
        ptr = src_lookup
        for fld in optiondict['key_fields']:
            fldvalue = kvxls.getExcelCellValue(excel_dict_out, row, fld)
            # debug
            # print('row', row, 'fldvalue', fldvalue)
            if fldvalue in ptr:
                ptr = ptr[fldvalue]
            else:
                # debug
                # print('did not match')
                
                matched = False
                break
        # if we did not find a match we are done
        if not matched:
            continue
        
        # we now have the src row
        src_row = ptr

        # debug
        # print('outrow: ', row, 'src_row:', src_row)
        
        # now copy formatting
        kvxls.copyExcelCellFmtOnRow(excel_dict_src, src_row, excel_dict_out, row)

    
    # done copying over - save this file
    kvxls.writexls(excel_dict_out, optiondict['out_dir'] + optiondict['out_fname'])
    return msg
    
def print_final_results(optiondict, src_data, dst_data):
    print('')
    print('source file.....: ', optiondict['src_dir'] + optiondict['src_fname'])
    if optiondict['src_ws']:
        print('source ws.......: ', optiondict['src_ws'])
    print('new data file...: ', optiondict['dst_dir'] + optiondict['dst_fname'])
    if optiondict['dst_ws']:
        print('new data ws.....: ', optiondict['dst_ws'])
    print('generated file..: ', optiondict['out_dir'] + optiondict['out_fname'])
    if optiondict['rmv_fname'] and rmv_data:
        print('generated file..: ', optiondict['out_dir'] + optiondict['rmv_fname'])

# --------------------------------------------------------------------------------
# running this program
if __name__ == '__main__':

    
    # command line processing
    optiondict = kvutil.kv_parse_command_line( optiondictconfig ) # , keymapdict=keymapdict )

    # dump a json file to be used as a configuration file
    if optiondict['json_cfg_filename']:
        pprint.pprint(optiondict)
        print('-'*40)
        kvutil.dump_dict_to_json_file(optiondict['json_cfg_filename'], optiondict)
        print('Created json_cfg file:  ' + optiondict['json_cfg_filename'])
        sys.exit()

    # test up front
    test_process_errors(test_optiondict_must_set(optiondict))

    # First round of tests on inputs
    test_process_errors(test_optiondict_settings_pre(optiondict))

    #### Load the files
    src_data = kvxls.readxls2list(optiondict['src_dir'] + optiondict['src_fname'], optiondict['src_ws'])
    dst_data = kvxls.readxls2list(optiondict['dst_dir'] + optiondict['dst_fname'], optiondict['dst_ws'])

    # Second round of tests on inputs using src_data
    set_blank_rec_cnt = test_optiondict_settings_post(optiondict, src_data, dst_data)

    # generate lookup on source
    src_lookup = kvutil.create_multi_key_lookup(src_data, optiondict['key_fields'])
    
    # now step through the dst data and copy over matching data
    matched_recs = kvutil.copy_matched_data(dst_data, src_lookup, optiondict['key_fields'], optiondict['copy_fields'])

    # generatate the rmv_data list
    rmv_data = create_rmv_data(optiondict, src_data, dst_data)

    # display where we are at
    print('source recs.....: ', len(src_data))
    print('src set2default.: ', set_blank_rec_cnt)
    print('new recs........: ', len(dst_data))
    print('matched_recs....: ', matched_recs)
    if rmv_data:
        print('removed recs....: ', len(rmv_data))
        kvxls.writelist2xls(optiondict['out_dir'] + optiondict['rmv_fname'], rmv_data)

    # output what we came up with
    kvxls.writelist2xls(optiondict['out_dir'] + optiondict['out_fname'], dst_data)

    # now format this output we just created
    print(format_output(optiondict, src_data, dst_data))

    # copy over the formatting for cells
    print(format_output_cell(optiondict, src_data, dst_data))
    
    # final output
    print_final_results(optiondict, src_data, dst_data)

#eof

