"""
    Copy comments from file 1 and move them into file 2
    matching on the keys between two files

    src_dir/src_fname - the file that has the existing data that we need to copy over
    dst_dir/dst_fname - the NEW file that we read in and apply the src_data to
    out_dir/out_fname - the output file generated after we apply src_data to dst_fname.

    src_fname_glob/src_fname_glob_rev - allow the system to do a glob search for max/min filenames to be used
    dst_fname_glob/dst_fname_glob_rev - allow the system to do a glob search for max/min filenames to be used

    src_ws - worksheet to read in
    dst_ws - worksheet to read in and create if generating dst_fname
    out_ws - worksheet to create 

    out_fname_append - enables the generation of the out_fname based in the dst_fname and append a string.

    rmv_fname - show the records that used to be there but no longer are

    rmv_fname_append
    rmv_fname_uniqtype - causes unique filename 

    add_fname - show the records that were added in the new file that were not in the old file

    add_fname_append
    add_fname_uniqtype - causes unique filename

    default_fname - default 'dst_fname', valid values 'src_fname', 'dst_fname', 'out_fname'

    ignore_missing_src/ignore_missing_dst - ignore (don't error out) if there are missing files


    # how to cause the format of the file to be read in and generate an output json used to drive formats
    fmt_dir - format output directory
    fmt_fname - format output filename
    src_width - set to true
    no_fmt - set to true to quit after you create the output file
    format_output - set to true

    # flags to set if you want to capture and output the src_width format data
    src_width = True
    src_width = True
    no_fmt = True


    src_reqcols - the list of column headers that we must find in order to find the header row - when not populated the first row is header
    dst_reqcols - the list of column headers that we must find in order to find the header row - when not populated the first row is header

    copy_fields - list of fields from src_data that are copied into fields in dst_data
    key_fields - the list of fields in src_data and dst_data that define a unique record in the file
    set_blank_fields - a dictionary of key/value pairs - the key is the field in src_data that
                       if not populated with data - we assign the field "value" - if this is None we ignore this flow
    internal_copy_fields - list of dictionaries that define dst fields taht copy to other dst fields
                           each records is 
         {
            'src': <src_fieldname>, 
            'dst': <dst_fieldname>, 
            'src_not_blank': if true - update dst when src is not empty - overrules 'if_blank' when set do nothing on false
            'if_blank': if true - only update dst field when empty - which is default, when else - just always update
         }
    internal_compare_fields - list of dictionaries that define dst fields taht compare fields and communicate diffferences
         {
            'src': <src_fieldname>, 
            'dst': <dst_fieldname>, 
         }
    col_width - a dictionary that is column letter and column width numberic
    format_output - boolean when true we format the out_fname, with col_width if passed in or calc col_width on our own
    format_cell - boolean when true we copy the formatting of cells based on match key from src to out_fname
    src_width - when true, and format_output is true, we calculate col_width by reading the values from src_fname

    disp_msg_add_rmv - when creating add/remove files output # of records and the filename
    disp_msg
    update_cnt - report on number of records that were updated with data copoied over to them


@author:   Ken Venner
@contact:  ken.venner@sierrspace.com
@version:  1.29

    Created:   2024-05-20;kv
    Version:   2025-07-12;kv - lots of changes and now callable as a librarry
               2024-09-19;kv - more checks and additional features (like json_cfg_filename)
               2024-07-24;kv - added hyperlink_fields
               2024-06-03;kv


"""

import kvutil
# import kvdate
import kv_excel
import kvxls
# import kvdate
# import kvmatch
import pprint
import sys
import os


# ----------------------------------------

AppVersion = '1.29'
__version__ = '1.29'


# ----------------------------------------


# COMMAND LINE PROCESSING

optiondictconfig = {
    'AppVersion' : {
        'value': '1.29',
    },
    'debug' : {
        'value' : False,
        'type' : 'bool',
        'description': 'causes debugging print statements to execute',
    },
    'disp_msg' : {
        'value' : True,
        'type' : 'bool',
        'description': 'cause processing print statement to execute',
    },
    'disp_msg_add_rmv' : {
        'value' : False,
        'type' : 'bool',
        'description': 'cause processing print statement when creating add or rmv file',
    },
    'default_fname' : {
        'value' : 'dst_fname',
        'description': 'filename to use when filenames are not provided - default is dst_fname',
    },
    'src_dir' : {
        'value' : "",
        'type' : 'dir',
        'description': 'path to the file with the data to be copied from/existing data',
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
    'rmv_dir' : {
        'value' : None,
        'type' : 'dir',
        'description': 'path to the location where the removed records output file is placed',
    },
    'add_dir' : {
        'value' : None,
        'type' : 'dir',
        'description': 'path to the location where the added records output file is placed',
    },
    'fmt_dir' : {
        'value' : None,
        'type' : 'dir',
        'description': 'path to the location where the format col_width dictionary output file is placed',
    },
    'src_fname' : {
        'value' : "",
        'description':  'filename of the file with the data to copy from/existing',
    },
    'src_fname_glob' : {
        'value' : "",
        'description':  'filename glob of the file with the data to copy from/existing',
    },
    'src_fname_glob_rev' : {
        'value' : True,
        'type'  : 'bool',
        'description':  'glob max or min flag - True gets largest, False gets smallest',
    },
    'dst_fname' : {
        'value' : "",
        'description':  'filename of the file with the data to copy into/new version of data',
    },
    'dst_fname_glob' : {
        'value' : "",
        'description':  'filename glob of the file with the data to copy into/new version of data',
    },
    'dst_fname_glob_rev' : {
        'value' : True,
        'type'  : 'bool',
        'description':  'glob max or min flag - True gets largest, False gets smallest',
    },
    'out_fname' : {
        'value' : "",
        'description':  'filename of the output file-populated if different than dst_fname',
    },
    'rmv_fname' : {
        'value' : "",
        'description':  'filename of the removed records output file',
    },
    'add_fname' : {
        'value' : "",
        'description':  'filename of the added records output file',
    },
    'fmt_fname' : {
        'value' : "",
        'description':  'filename of the col_width dictionary output file',
    },
    'out_fname_append' : {
        'value' : "",
        'description':  'string to append to the dst_fname to create the out_fname - do not set this and out_fname',
    },
    'out_fname_uniqtype' : {
        'value' : "",
        'description':  'unique filename code if you want a unique fname generated',
    },
    'rmv_fname_append' : {
        'value' : "",
        'description':  'string to append to the dst_fname to create the rmv_fname',
    },
    'rmv_fname_uniqtype' : {
        'value' : "",
        'description':  'unique filename code if you want a unique fname generated',
    },
    'add_fname_append' : {
        'value' : "",
        'description':  'string to append to the dst_fname to create the add_fname',
    },
    'add_fname_uniqtype' : {
        'value' : "",
        'description':  'unique filename code if you want a unique fname generated',
    },
    'src_ws' : {
        'value' : None,
        'description':  'worksheet in the file with the data to copy from/existing',
    },
    'dst_ws' : {
        'value' : None,
        'description':  'worksheet in the file with the data to copy into',
    },
    'out_ws' : {
        'value' : None,
        'description':  'worksheet in the output file',
    },
    'src_reqcols' : {
        'value' : None,
        'description':  'list of columns used to find the header - when none - first row is the header',
    },
    'dst_reqcols' : {
        'value' : None,
        'description':  'list of columns used to find the header - when none - first row is the header',
    },
    'ignore_missing_src' : {
        'value' : False,
        'type': 'bool',
        'description':  'when true if src file does not exist - exit quietly do not error out',
    },
    'ignore_missing_dst' : {
        'value' : False,
        'type': 'bool',
        'description':  'when true if dst file does not exist - exit quietly do not error out',
    },
    'update_cnt' : {
        'value' : False,
        'type': 'bool',
        'description':  'when true report on the number of records where an update took place',
    },
    'json_cfg_filename' : {
        'value' : False,
        'description': 'when populated with a filename - we create a default cfg json file',
    },
    'copy_fields' : {
        'value' : [
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
    'internal_compare_fields' : {
        'value' : [
        ],
        'type' : 'liststr',
        'description': 'list of dictionaries that defines what we compare inside the dst file and show differences',
    },
    'key_fields' : {
        'value' : [
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
        'description': 'when true we format the created out_fname or dst_fname',
    },
    'format_cell' : {
        'value' : True,
        'type' : 'bool',
        'description': 'when true we copy over formatting to out_fname or dst_fname',
    },
    'src_width' : {
        'value' : True,
        'type' : 'bool',
        'description': 'when true and format_output is true - get col_width from the src_fname',
    },
    'src_width_disp' : {
        'value' : False,
        'type' : 'bool',
        'description': 'when true, and src_width true display the source file column widths',
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
    },
    'no_fmt' : {
        'value' : False,
        'type' : 'bool',
        'description': "when enabled we read in the format but we don't create the output - we exit",
    },
    'desc' : {
        'value' : '',
        'description': "holder for conf description",
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


def validate_inputs(optiondict):
    '''
    test inputs and set defaults
    '''

    debug = False
    debug2 = False
    if debug:
        print('optiondict - validate_inputs')
        pprint.pprint(optiondict)
    
    # expected values - set display message if not set
    if 'disp_msg' not in optiondict:
        optiondict['disp_msg'] = False
        
    # default fields that were not set - set add/rmv to outdir if outdir set and they are not
    for fld in ['rmv_dir', 'add_dir']:
        if not optiondict[fld]:
            if optiondict['out_dir']:
                optiondict[fld] = optiondict['out_dir']
            elif optiondict['dst_dir']:
                optiondict[fld] = optiondict['dst_dir']
        
    # set directories to match the src_dir if not set
    for fld in ('dst_dir', 'out_dir', 'rmv_dir', 'add_dir', 'fmt_dir'):
        if not optiondict[fld]:
            optiondict[fld] = optiondict['src_dir']

    # make sure each directory ends with '/'
    for fld in ('src_dir', 'dst_dir', 'out_dir', 'rmv_dir', 'add_dir', 'fmt_dir'):
        if optiondict[fld][-1] == '\\':
            optiondict[fld] = optiondict[fld][-1] + '/'
        if optiondict[fld][-1] != '/':
            optiondict[fld] += '/'

    # generate the remove and/or add filename
    for fld in ['rmv', 'add', 'out']:
        # determine if we need to create a staring value - if they want to add on - we must create
        if optiondict[fld+'_fname_append'] or optiondict[fld+'_fname_uniqtype']:
            # if fname not populated - take it from dst_fname
            if not optiondict[fld+'_fname']:
                optiondict[fld+'_fname'] = optiondict[optiondict['default_fname']]
                
        # we assume fname is set - that is done in validate_inputs()
        if optiondict[fld+'_fname_append']:
            # calculate the new filename
            fname, fext = os.path.splitext(optiondict[fld+'_fname'])
            # build the new filename
            optiondict[fld+'_fname'] = fname + optiondict[fld+'_fname_append'] + fext

        # generate a unique remove/add filename
        if optiondict[fld+'_fname_uniqtype']:
            # now build the dict that causes the generation of a unique filename
            file_href = {
                'file_path': optiondict[fld+'_dir'],
                'filename': os.path.join(optiondict[fld+'_dir'], optiondict[fld+'_fname']),
                'uniqtype': optiondict[fld+'_fname_uniqtype'],
                'forceuniq': True,
            }
            optiondict[fld+'_fname'] = os.path.basename(kvutil.filename_unique(filename_href=file_href, debug=False))

    # debugging
    if debug:
        print('optiondict - validate_inputs:mid')
        pprint.pprint(optiondict)
    
    # deal with src_fname_glob
    if optiondict['src_fname_glob']:
        optiondict['src_fname'] = os.path.basename(kvutil.filename_maxmin(optiondict['src_dir']+optiondict['src_fname_glob'], optiondict['src_fname_glob_rev']))
    # deal with dst_fname_glob
    if optiondict['dst_fname_glob']:
        optiondict['dst_fname'] = os.path.basename(kvutil.filename_maxmin(optiondict['dst_dir']+optiondict['dst_fname_glob'], optiondict['dst_fname_glob_rev']))


    # key fields comparison - if no key return False - maybe change to raise Exception()
    if not 'key_fields' in optiondict:
        # output messages
        if optiondict['disp_msg']:
            print('Must define the fields that make the business keys in:  key_fields')
        return False

    # if this fields is not the right type - return False - maybe change to raise Exception()
    if type(optiondict['key_fields']) != list:
        # output messages
        if optiondict['disp_msg']:
            print('Attribute key_fields must be a list but is a: ', type(optiondict['key_fields']))
        return False
    
    # validate the structure is correct if we are copying internally
    if optiondict['internal_copy_fields']:
        # if we have a dict - it shoudl have been a list - convert to a list with one dict entry
        if type(optiondict['internal_copy_fields']) == dict:
            optiondict['internal_copy_fields'] = [optiondict['internal_copy_fields']]

        # this shoudl have a list of dicts
        has_issues = False
        for idx, copydict in enumerate(optiondict['internal_copy_fields']):
            for fld in ['src', 'dst']:
                if fld not in copydict:
                    print(f"internal_copy_fields [{idx+1}] missing required key [{fld}]: " + str(copydict))
                    has_issues = True
                # set the default if not set
                if 'is_blank' not in copydict:
                    copydict['is_blank'] = True
        # finally if we have issue then terminate
        if has_issues:
            return False

    # validate the structure is correct if we are copying internally
    if optiondict['internal_compare_fields']:
        # if we have a dict - it shoudl have been a list - convert to a list with one dict entry
        if type(optiondict['internal_compare_fields']) == dict:
            optiondict['internal_compare_fields'] = [optiondict['internal_compare_fields']]

        # this shoudl have a list of dicts
        has_issues = False
        for idx, copydict in enumerate(optiondict['internal_compare_fields']):
            for fld in ['src', 'dst']:
                if fld not in copydict:
                    print(f"internal_compare_fields [{idx+1}] missing required key [{fld}]: " + str(copydict))
                    has_issues = True
            # set the default if not set
            if 'is_blank' not in copydict:
                copydict['is_blank'] = True
        # finally if we have issue then terminate
        if has_issues:
            return False
        

    # validate we have copy_fields
    if optiondict['force_copy_flds']:
        if not 'copy_fields' in optiondict:
            # output messages
            if optiondict['disp_msg']:
                print('When [force_copy_flds] is set you must defined [copy_fields] and have not')
            return False
        elif type(optiondict['copy_fields']) != list:
            # output messages
            if optiondict['disp_msg']:
                print('When [copy_fields] is defined it must be list and is:  ', type(optiondict['copy_fields']))
            return False
        elif not optiondict['copy_fields']:
            # output messages
            if optiondict['disp_msg']:
                print('When [copy_fields] exist it must have values and does not')
            return False

    # debugging
    if debug or debug2:
        print('optiondict - validate_inputs:end')
        pprint.pprint(optiondict)
    if debug:
        sys.exit()
        
    # return that all is ok
    return True
    
def load_records(optiondict, srctype='src', disp_msg=False):
    '''
    pass in the type of config variables we want to load from - then load and return that list of records

    we require srctype+'_dir' and srctype+'_fname' to be populated but not the other vars
    
    srctype can be:  src|dst
    '''
    # set the value if not set
    if srctype+'_ws' not in optiondict:
        optiondict[srctype+'_ws'] = None

    # get the full filename of the object we are going after
    full_filename = os.path.join(optiondict[srctype+'_dir'], optiondict[srctype+'_fname'])
    
    # check for file existenace if we are allowed to not require the file
    if optiondict['ignore_missing_'+srctype]:
        # check for existence of the src file
        if not os.path.exists(full_filename):
            if disp_msg:
                print('copy_comments:load_records:file does not exist: '+full_filename)
            return []

    # load the file
    if srctype+'_reqcols' in optiondict and optiondict[srctype+'_reqcols']:
        # look up the header because we defined the requirec columns
        loaded_optiondict = {'sheetname': optiondict[srctype+'_ws'], 'save_row': True}
        loaded_data = kvxls.readxls2list_findheader(full_filename, optiondict[srctype+'_reqcols'], optiondict=loaded_optiondict)
    else:
        # load with the assumption that the first row is the header
        loaded_data = kvxls.readxls2list(full_filename, optiondict[srctype+'_ws'])

    if False:
        print(full_filename)
        print(len(loaded_data))
    
    return loaded_data

def read_src_file_format(optiondict):
    '''
    This reads in the src file and gets the format from it and stores it in optiondict
    '''
    # set the variable
    if 'disp_msg' not in optiondict:
        optiondict['disp_msg'] = True

    # get full filename
    full_filename = os.path.join(optiondict['src_dir'], optiondict['src_fname'])
    
    # check if we should load the col_width from the src_fname
    if 'src_width' in optiondict and optiondict['src_width']:
        # output messages
        if optiondict['disp_msg']:
            print('Getting col_width formatting from src_fname')
        optiondict['col_width'] = kv_excel.get_existing_column_width(full_filename, disp_msg=optiondict['disp_msg'])
        # display this if they are looking for it
        if optiondict['src_width_disp']:
            print('Source file col width:')
            pprint.pprint(optiondict['col_width'])
            if optiondict['no_fmt']:
                print('src_width, src_width_disp and no_fmt set - exitting')
                sys.exit()

                
def validate_missing_columns(loaded_data, optiondict, fld):
    '''
    Validate that the data has the columns required based on the list of columns defined by 'fld'
    '''
    # check to see if key is even there - if not we are not missing anything
    if fld not in optiondict:
        return []
    
    # get the list of key_fields columns that don't have that key in the first record in this list
    return [x for x in optiondict[fld] if x not in loaded_data[0]]

def create_flds_in_records(loaded_data, fields):
    '''
    force the creation of a field if it does not exist in all records
    '''
    for rec in loaded_data:
        for fld in fields:
            if fld not in rec:
                rec[fld] = ''

def convert_hyperlink_values(loaded_data, optiondict, hyperlink_fld='hyperlink_fields'):
    '''
    Take a list of fields and convert them to hyperlink fields
    '''
    kvutil.convert_hyperlink_field_values(loaded_data, optiondict, hyperlink_fld)
    
def src_to_dst_actions(src_data, dst_data, optiondict):
    '''
    take the action defined in option dict
    '''
    # set up keys with None if they don't exist
    for fld in ['copy_fields', 'internal_copy_fields', 'internal_compare_fields']:
        if fld not in optiondict:
            optiondict[fld] = None

    # nothing to do if there is not src_data
    if not src_data:
        return 0, 0, {}
    
    # generate lookup on source
    src_lookup = kvutil.create_multi_key_lookup(src_data, optiondict['key_fields'])
    
    # do nothing if we have nothing to do
    if not optiondict['copy_fields'] and not optiondict['internal_copy_fields'] and not optiondict['internal_compare_fields']:
        return 0, 0, src_lookup
    
    # now step through the dst data and copy over matching data
    if optiondict['copy_fields']:
        if optiondict['update_cnt']:
            matched_recs, updated_recs = kvutil.copy_matched_data_cnt(
                dst_data,
                src_lookup,
                optiondict['key_fields'],
                optiondict['copy_fields'],
                force_copy_flds=optiondict.get('force_copy_flds', False),
                disp_msg=False
            )
        else:    
            matched_recs = kvutil.copy_matched_data(
                dst_data,
                src_lookup,
                optiondict['key_fields'],
                optiondict['copy_fields'],
                force_copy_flds=optiondict.get('force_copy_flds', False),
                disp_msg=False
            )
            updated_recs = matched_recs
    else:
        matched_recs = 0
        updated_recs = 0
    
    # now copy over fields interest witin the output file
    if optiondict['internal_copy_fields']:
        # output messages
        if optiondict['disp_msg']:
            print('Copying data inside the file defined by internal_copy_fields')
        # copy fields in the file we just read in
        for rec in dst_data:
            for copydict in optiondict['internal_copy_fields']:
                if 'src_not_blank' in copydict and copydict['src_not_blank'] and not rec[copydict['src']]:
                    # copy source when not blank
                    rec[copydict['dst']] = rec[copydict['src']]
                elif (copydict['is_blank'] and not rec[copydict['dst']]) or not copydict['is_blank'] :
                    # dst is not populated and flag set,
                    # or is_blank is False (we want to update all recrs,
                    # then update from src
                    rec[copydict['dst']] = rec[copydict['src']]

    # now compare fields interest witin the output file
    if optiondict['internal_compare_fields']:
        # output messages
        if optiondict['disp_msg']:
            print('Comparing data inside the file defined by internal_compare_fields')
        # copy fields in the file we just read in
        for rec in dst_data:
            # set the original value
            rec['internal_compare'] = ''
            for copydict in optiondict['internal_compare_fields']:
                # compare and set field if
                if rec[copydict['dst']] != rec[copydict['src']] and not rec['internal_compare']:
                    rec['internal_compare'] = 'Mismatch'

    return matched_recs, updated_recs, src_lookup


def removed_records(src_data, dst_data, optiondict):
    '''
    find the records in src_data that are not in dst_data
    '''
    if 'key_fields' not in optiondict:
        raise Exception('key_fields not defined in optiondict')
    if not optiondict['key_fields']:
        raise Exception('key_fields defined and empty in optiondict')
    if type(optiondict['key_fields']) != list:
        raise TypeError('key_fields defined and not list but type: ' + str(type(optiondict['key_fields'])))
    
    dst_lookup = kvutil.create_multi_key_lookup(dst_data, optiondict['key_fields'])
    rmv_data = kvutil.extract_unmatched_data(src_data, dst_lookup, optiondict['key_fields'])

    return rmv_data, dst_lookup

def added_records(src_data, dst_data, src_lookup, optiondict):
    '''
    find the records in dst_data that are not in src_data
    but pass in the dictionary for src_lookup
    '''
    if 'key_fields' not in optiondict:
        raise Exception('key_fields not defined in optiondict')
    if not optiondict['key_fields']:
        raise Exception('key_fields defined and empty in optiondict')
    if type(optiondict['key_fields']) != list:
        raise TypeError('key_fields defined and not list but type: ' + str(type(optiondict['key_fields'])))

    add_data = kvutil.extract_unmatched_data(dst_data, src_lookup, optiondict['key_fields'])

    return add_data

def generate_out_output_file_not_formatted(dst_data, optiondict, updated_recs):
    '''
    generate the output file is we create a new file
    or recreate the destination file if records were updated
    '''
    # output what we came up with
    if 'out_fname' in optiondict and optiondict['out_fname']:
        full_filename = os.path.join(optiondict['out_dir'], optiondict['out_fname'])
        kvxls.writelist2xls(full_filename, dst_data)
        if 'debug' in optiondict and optiondict['debug']:
            print('out_write:', full_filename)
    elif 'dst_fname' in optiondict and optiondict['dst_fname'] and updated_recs:
        full_filename = os.path.join(optiondict['dst_dir'], optiondict['dst_fname'])
        kvxls.writelist2xls(full_filename, dst_data)
        if 'debug' in optiondict and optiondict['debug']:
            print('dst_write:', full_filename)

def generate_rmv_output_file_not_formatted(rmv_data, optiondict):
    '''
    generate the remove file if defined and we have remove file records
    '''
    # output what we came up with
    if 'rmv_fname' in optiondict and optiondict['rmv_fname'] and rmv_data:
        full_filename = os.path.join(optiondict['rmv_dir'], optiondict['rmv_fname'])
        kvxls.writelist2xls(full_filename, rmv_data)
        if 'debug' in optiondict and optiondict['debug']:
            print('rmv_write:', full_filename)
        if 'disp_msg_add_rmv' in optiondict and optiondict['disp_msg_add_rmv']:
            print('Record count: ', len(rmv_data))
            print('Created file: ' + full_filename)

def generate_add_output_file_not_formatted(add_data, optiondict):
    '''
    generate the add file if defined and we have remove file records
    '''
    # output what we came up with
    if 'add_fname' in optiondict and optiondict['add_fname'] and add_data:
        full_filename = os.path.join(optiondict['add_dir'], optiondict['add_fname'])
        kvxls.writelist2xls(full_filename, add_data)
        if 'debug' in optiondict and optiondict['debug']:
            print('add_write:', full_filename)
        if 'disp_msg_add_rmv' in optiondict and optiondict['disp_msg_add_rmv']:
            print('Record count: ', len(add_data))
            print('Created file: ' + full_filename)


def format_output(optiondict):
    '''
    Format the output file based on flags passed in
    '''
    
    # if they want it formatted
    if 'format_output' not in optiondict:
        return
    if not optiondict['format_output']:
        return

    disp_msg = True
    # output messages
    if 'disp_msg' in optiondict:
        if optiondict['disp_msg']:
            print('\nFormatting output file')
        else:
            disp_msg = False
            
    # if we set fmt_fname then save this col width data
    if 'fmt_fname' in optiondict and optiondict['fmt_fname']:
        full_filename = os.path.join(optiondict['fmt_dir'], optiondict['fmt_fname'])
        kvutil.dump_dict_to_json_file(full_filename, {"col_width": optiondict['col_width']})
        # output messages
        if 'disp_msg' in optiondict and optiondict['disp_msg']:
            print('Saved col_width to:' + full_filename)
    #
    # output messages
    if 'disp_msg' in optiondict and optiondict['disp_msg']:
        print('Performing output formatting')
    if 'out_fname' in optiondict and optiondict['out_fname']:
        excel_filename = os.path.join(optiondict['out_dir'],optiondict['out_fname'])
    else:
        excel_filename = os.path.join(optiondict['dst_dir'], optiondict['dst_fname'])
    if optiondict['debug'] or optiondict['no_fmt']:
        # output messages
        if optiondict['disp_msg']:
            print('reformat_out:', excel_filename)
            print('col_width we reformat with:')
            pprint.pprint(optiondict['col_width'])
    if optiondict['no_fmt'] or 'col_width' not in optiondict or not optiondict['col_width']:
        return
    # format this file with what is defined in col_width
    kv_excel.format_xlsx_with_filter_and_freeze(excel_filename, col_width=optiondict['col_width'], disp_msg=disp_msg)

def format_cell(optiondict):
    '''
    Copy over cell based formatting
    '''
    
    # if they want to copy over formatting
    if 'format_cell' not in optiondict or not optiondict['format_cell']:
        return

    # display we are cell formatting
    if optiondict['disp_msg']:
        print('\nCopying Cell Formatting')

    # debug
    # print('src file:', optiondict['src_dir'] + optiondict['src_fname'])
    
    # reading in the source
    excel_dict_src = kvxls.readxls_findheader(
        os.path.join(optiondict['src_dir'],  optiondict['src_fname']),
        [],
        optiondict={'col_header': True, 'keep_vba': False, 'sheetname': optiondict['src_ws']},
        data_only=False
    )

    # define which file we are pulling from as the output/destination
    if optiondict['out_fname']:
        excel_filename = os.path.join(optiondict['out_dir'], optiondict['out_fname'])
        sheetname = optiondict['out_ws']
    else:
        excel_filename = os.path.join(optiondict['dst_dir'], optiondict['dst_fname'])
        sheetname = optiondict['dst_ws']

    # debugging
    if optiondict['debug']:
        print('reformat_cell:', excel_filename)

    # reading in the destination
    excel_dict_out = kvxls.readxls_findheader(
        excel_filename,
        [],
        optiondict={'col_header': True, 'keep_vba': False, 'sheetname': sheetname},
        data_only=False
    )
    # build the cross reference table
    src_lookup = kvxls.create_multi_key_lookup_excel(excel_dict_src, optiondict['key_fields'])

    # debug
    # pprint.pprint(src_lookup)

    # step through the output and find the equivalent input and then copy over the formatting
    for row in range(excel_dict_out['row_header']+1, excel_dict_out['sheetmaxrow']):
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
    kvxls.writexls(excel_dict_out, excel_filename)
    
def generate_out_output_file_formatted(dst_data, optiondict, updated_recs):
    '''
    generate the output file is we create a new file
    or recreate the destination file if records were updated
    '''
    generate_out_output_file_not_formatted(dst_data, optiondict, updated_recs)
    format_output(optiondict)
    format_cell(optiondict)


# --------------------------------------------------------------------------------

if __name__ == "__main__":

    # command line processing
    optiondict = kvutil.kv_parse_command_line( optiondictconfig ) # , keymapdict=keymapdict )

    # dump a json file to be used as a configuration file
    if optiondict['json_cfg_filename']:
        pprint.pprint(optiondict)
        print('-'*40)
        kvutil.dump_dict_to_json_file(optiondict['json_cfg_filename'], optiondict)
        print('Created json_cfg file:  ' + optiondict['json_cfg_filename'])
        sys.exit()


    # validate the inputs/settings
    if not validate_inputs(optiondict):
        sys.exit(1)

    # debugging
    #pprint.pprint(optiondict)
    #sys.exit()

    # check for file existenace
    if optiondict['ignore_missing_src']:
        # check for existence of the src file
        full_filename = os.path.join(optiondict['src_dir'], optiondict['src_fname'])
        if not os.path.exists(full_filename):
            # output messages
            if optiondict['disp_msg']:
                print('SRC File does not exist - moving along: '+full_filename)
            sys.exit()
    if optiondict['ignore_missing_dst']:
        # check for existence of the dst file
        full_filename = os.path.join(optiondict['dst_dir'], optiondict['dst_fname'])
        if not os.path.exists(full_filename):
            # output messages
            if optiondict['disp_msg']:
                print('DST File does not exist - moving along: '+full_filename)
            sys.exit()

    # load the sourced and destination data
    src_data = load_records(optiondict, 'src')
    dst_data = load_records(optiondict, 'dst')

    # check that we found records
    if not len(src_data):
        # output messages
        if optiondict['disp_msg']:
            print('Found no records in: ', os.path.join(optiondict['src_dir'], optiondict['src_fname']))
        sys.exit(1)

    # read in format for src file if we want it
    read_src_file_format(optiondict)

    # check that we have the key fields in the src_data
    missing_cols = validate_missing_columns(src_data, optiondict, 'key_fields')
    if missing_cols:
        # output messages
        if optiondict['disp_msg']:
            print('You are MOST LIKELY reading in the wrong src sheet as we can not find column(s): ',
                  '|'.join(missing_cols) )
        sys.exit(1)        

    # check that we have the copy_fields columns
    missing_cols = validate_missing_columns(src_data, optiondict, 'copy_fields')
    if missing_cols:
        # output messages
        if optiondict['disp_msg']:
            print('You are missing in src_data the following copy_fields column(s): ',
                  '|'.join(missing_cols) )
        sys.exit(1)

    # check that we have the internal_compare_fields  columns
    missing_cols = validate_missing_columns(src_data, optiondict, 'internal_compare_fields')
    if missing_cols:
        # output messages
        if optiondict['disp_msg']:
            print('You are missing in src_data the following internal_compare_fields column(s): ',
                  '|'.join(missing_cols) )
        sys.exit(1)

    # check that we have the internal_compare_fields  columns
    missing_cols = validate_missing_columns(dst_data, optiondict, 'internal_compare_fields')
    if missing_cols: 
        # output messages
        if optiondict['disp_msg']:
            print('You are missing in dst_data the following internal_compare_fields column(s): ',
                  '|'.join(missing_cols) )
        sys.exit(1)

    
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

    # if we are forcing fields to be in the records make it happen
    if optiondict['force_copy_flds']:
        create_flds_in_records(dst_data, optiondict['copy_fields'])

    # update the hyperlink fields
    if optiondict['hyperlink_fields']:
        convert_hyperlink_values(src_data, optiondict, 'hyperlink_fields')
        convert_hyperlink_values(dst_data, optiondict, 'hyperlink_fields')

    # output when requested
    if optiondict['dump_recs']:
        print('-'*80)
        print('Hyperlink Original Source:')
        pprint.pprint(src_data)
        print('-'*80)
        print('Hyperlink New Source:')
        pprint.pprint(dst_data)
        print('-'*80)
        print('\n')

    
    # set the values on blank entries in source file if configured
    if optiondict['set_blank_fields']:
        default_recs = kvutil.set_blank_field_values(src_data, optiondict['set_blank_fields'])
    else:
        default_recs = 0

    # now take the action
    matched_recs, updated_recs, src_lookup = src_to_dst_actions(src_data, dst_data, optiondict)
    
    
    # if we want to save out the removed records then do that analysis
    if optiondict['rmv_fname']:
        rmv_data, dst_lookup = removed_records(src_data, dst_data, optiondict)
    else:
        rmv_data = []

    # if we want to save out the removed records then do that analysis
    if optiondict['add_fname']:
        add_data = added_records(src_data, dst_data, src_lookup, optiondict)
    else:
        add_data = []

    # output what is going on
    if optiondict['dump_recs']:
        print('-'*80)
        print('DST Output Records:')
        pprint.pprint(dst_data)
        print('-'*80)

    # display what is going on
    if optiondict['disp_msg']:
        print('source recs.....: ', len(src_data))
        print('src set2default.: ', default_recs)
        print('new recs........: ', len(dst_data))
        print('matched_recs....: ', matched_recs)
        if optiondict['update_cnt']:
            print('updated_recs....: ', updated_recs)
        if optiondict['rmv_fname']:
            print('removed recs....: ', len(rmv_data))
        if optiondict['add_fname']:
            print('added recs......: ', len(add_data))

    # output raw outputs not formatted
    generate_out_output_file_not_formatted(dst_data, optiondict, updated_recs)
    generate_rmv_output_file_not_formatted(rmv_data, optiondict)
    generate_add_output_file_not_formatted(add_data, optiondict)

    # format the output file
    format_output(optiondict)

    # format the output by cell
    format_cell(optiondict)
    
    # display what is going on
    if optiondict['disp_msg']:
        print('')
        print('source file.....: ', optiondict['src_dir'] + optiondict['src_fname'])
        if optiondict['src_ws']:
            print('source ws.......: ', optiondict['src_ws'])
        print('new data file...: ', optiondict['dst_dir'] + optiondict['dst_fname'])
        if optiondict['dst_ws']:
            print('new data ws.....: ', optiondict['dst_ws'])
        if optiondict['out_fname']:
            print('generated file..: ', optiondict['out_dir'] + optiondict['out_fname'])
        if optiondict['rmv_fname'] and rmv_data:
            print('generated file..: ', optiondict['rmv_dir'] + optiondict['rmv_fname'])
        if optiondict['add_fname'] and add_data:
            print('generated file..: ', optiondict['add_dir'] + optiondict['add_fname'])
    
#eof
