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


    ### READING IN THE CURRENT SRC FILE FORMAT ###
    # how to cause the format of the file to be read in and generate an output json used to drive formats
    # 1) Create the starting json configuration file to load this data
    #    desc, src_dir, dst_dir, src_fname, dst_fname, copy_fields, key_fields
    # 2) on the command line set the following
    fmt_dir - format output directory
    fmt_fname - format output filename
    src_width - set to true
    no_fmt - set to true to quit after you create the output file
    format_output - set to true

    # Command Line:
    # python copy_comments.py fmt_dir="." fmt_fname=ken.json format_output=1 no_fmt=1 src_width=1 disp_msg=1 conf_json=<json_file>

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
    col_hidden - a  list of column header letters that are defined as hidden columns
    format_auto - boolean when true - we allow automatic column width calcs
    format_output - boolean when true we format the out_fname, with col_width if passed in or calc col_width on our own
    format_cell - boolean when true we copy the formatting of cells based on match key from src to out_fname
    src_width - when true, and format_output is true, we calculate col_width by reading the values from src_fname

    disp_msg_add_rmv - when creating add/remove files output # of records and the filename
    disp_msg - display messages about what is going on
    update_cnt - report on number of records that were updated with data copoied over to them


@author:   Ken Venner
@contact:  ken.venner@sierrspace.com
@version:  1.34

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

AppVersion = '1.34'
__version__ = '1.34'


# ----------------------------------------


# COMMAND LINE PROCESSING

optiondictconfig = {
    'AppVersion' : {
        'value': '1.34',
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
    'create_json' : {
        'value' : '',
        'description': 'pass in the filename of XLSX you want to create a json for and this will set flags and output the json',
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
    'col_hidden' : {
        'value': None,
        'type' : list,
        'description' : 'list defines the column headers that are hidden',
    },
    'format_auto' : {
        'value' : False,
        'type' : 'bool',
        'description': 'when true we allow for automatic calculation of column widths',
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

Example of col_hidden:
['P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']

'''

def update_optiondict4json_create(optiondict: dict) -> None:
    """
    when this is set - and has a XLSX filename in it - then set all the proper flags to generate the output json
    """

    # test that the input we got is an xlsx and exists
    if not os.path.exists(optiondict['create_json']):
        raise FileNotFoundError

    # split up the filename
    fdir, fname = os.path.split(optiondict['create_json'])
    fname_only, fext = os.path.splitext(fname)
    # fdir += '\\'
    
    # check the extension
    if fext.upper() != '.XLSX':
        raise ValueError(f'Not XLSX file extension - provided extension was [{fext}]')
    
    # default directory for the output file
    if not optiondict.get('fmt_dir'):
        optiondict['fmt_dir'] = "./"

    # if we did not proivde the filename for the output file - it is the input file with .JSON on it
    if not optiondict.get('fmt_fname'):
        optiondict['fmt_fname']=fname_only + '.json'

    # set the source and dst dir/fname
    for fld in ['src', 'dst']:
        if not optiondict.get(fld+'_dir'):
            optiondict[fld+'_dir'] = fdir
        if not optiondict.get(fld+'_fname'):
            optiondict[fld+'_fname'] = fname

    # copy over src_ws to dst_ws
    if optiondict.get('src_ws') and not optiondict.get('dst_ws'):
        optiondict['dst_ws'] = optiondict['src_ws']
        
    # set default_fname
    if not optiondict.get('default_fname'):
        optiondict['default_fname'] = 'dst_fname'

    # Now set the flags
    for fld in ['src_width', 'no_fmt', 'format_output']:
        optiondict[fld] = True

    # debugging
    if False:
        print('Optiondict generated for create_json:')
        pprint.pprint(optiondict)
    

def validate_inputs(optiondict: dict) -> bool | None:
    """
    test inputs and set defaults
    """

    debug = False
    debug2 = False
    if debug:
        print('optiondict - validate_inputs')
        pprint.pprint(optiondict)
    
    # expected values - set display message if not set
    if 'disp_msg' not in optiondict:
        optiondict['disp_msg'] = False

    # if we set create_json - update the optiondict config to make all the required settings to generate an output configuratoin json
    if optiondict.get('create_json'):
        update_optiondict4json_create(optiondict)
        
    # if src_dir not set - set it to the currnet working directory
    if not optiondict.get('src_dir'):
        optiondict['src_dir'] = './'

    # default fields that were not set - set add/rmv to outdir if outdir set and they are not dst_dir
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
        if optiondict[fld] and optiondict[fld][-1] == '\\':
            optiondict[fld] = optiondict[fld][-1] + '/'
        if optiondict[fld][-1] != '/':
            optiondict[fld] += '/'

    # validate the default filename is set correctly
    if optiondict['default_fname'] not in ('dst_fname', 'src_fname', 'out_fname'):
        if optiondict['disp_msg']:
            print('default_fname must be one of the following: ' + ','.join(['dst_fname', 'src_fname', 'out_fname']) + ' but is: ' + optiondict['default_fname'])
        optiondict['error_msg'] = 'default_fname must be one of the following: ' + ','.join(['dst_fname', 'src_fname', 'out_fname']) + ' but is: ' + optiondict['default_fname']
        return False

    # test that the default filename is actually set
    if not optiondict.get(optiondict['default_fname']):
        if optiondict['disp_msg']:
            print(f'default_fname [{optiondict['default_fname']}] is not set')
        optiondict['error_msg'] = f'default_fname [{optiondict['default_fname']}] is not set'
        return False
    
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


    # format/output options
    if 'src_width' in optiondict and optiondict['src_width'] and (optiondict.get('col_width') or optiondict.get('col_hidden')):
        # output messages
        if optiondict['disp_msg']:
            print('You should not have src_width true and values in col_width or col_hidden')
        optiondict['error_msg'] = 'Must define the fields that make the business keys in:  key_fields''You should not have src_width true and values in col_width or col_hidden'
        return False

    # key fields comparison - if no key return False - maybe change to raise Exception()
    if 'key_fields' not in optiondict:
        # output messages
        if optiondict['disp_msg']:
            print('Must define the fields that make the business keys in:  key_fields')
        optiondict['error_msg'] = 'Must define the fields that make the business keys in:  key_fields'
        return False

    # if this fields is not the right type - return False - maybe change to raise Exception()
    if type(optiondict['key_fields']) is not list:
        # output messages
        if optiondict['disp_msg']:
            print('Attribute key_fields must be a list but is a: ', type(optiondict['key_fields']))
        optiondict['error_msg'] = 'Attribute key_fields must be a list but is a: ', type(optiondict['key_fields'])
        return False
    
    # validate the structure is correct if we are copying internally
    if optiondict['internal_copy_fields']:
        # if we have a dict - it shoudl have been a list - convert to a list with one dict entry
        if type(optiondict['internal_copy_fields']) is dict:
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
            optiondict['error_msg'] = 'Issues with internal_copy_fields'
            return False

    # validate the structure is correct if we are copying internally
    if optiondict['internal_compare_fields']:
        # if we have a dict - it shoudl have been a list - convert to a list with one dict entry
        if type(optiondict['internal_compare_fields']) is dict:
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
            optiondict['error_msg'] = 'Issues with internal_compare_fields'
            return False
        

    # validate we have copy_fields
    if optiondict['force_copy_flds']:
        if 'copy_fields' not in optiondict:
            # output messages
            if optiondict['disp_msg']:
                print('When [force_copy_flds] is set you must defined [copy_fields] and have not')
            optiondict['error_msg'] = 'When [force_copy_flds] is set you must defined [copy_fields] and have not'
            return False
        elif type(optiondict['copy_fields']) is not list:
            # output messages
            if optiondict['disp_msg']:
                print('When [copy_fields] is defined it must be a list and is:  ', type(optiondict['copy_fields']))
            optiondict['error_msg'] = 'When [copy_fields] is defined it must be a list and is:  ', type(optiondict['copy_fields'])
            return False
        elif not optiondict['copy_fields']:
            # output messages
            if optiondict['disp_msg']:
                print('When [copy_fields] exists and it must have values and does not')
            optiondict['error_msg'] = 'When [copy_fields] exists and it must have values and does not'
            return False

    # testing the internal comparison settings
    if optiondict.get('internal_copy_fields'):
        # right type
        if type(optiondict['internal_copy_fields']) != list:
            # output messages
            if optiondict['disp_msg']:
                print('internal_copy_fields must be of type list of dicts and is of type: ' + str(type(optiondict['internal_copy_fields'])))
            optiondict['error_msg'] = 'internal_copy_fields must be of type list of dicts and is of type: ' + str(type(optiondict['internal_copy_fields']))
            return False

        # check the list entries for this
        ruleissues = ''
        for rulenum, copydict in enumerate(optiondict['internal_copy_fields']):
            if not 'dst' in copydict:
                msg = f"{rulenum} missing dst key\n"
                ruleissues += msg
            if not 'src' in copydict:
                msg = f"{rulenum} missing src key\n"
                ruleissues += msg

        # if we have issue report
        if ruleissues:
            if optiondict['disp_msg']:
                print(ruleissues)
            optiondict['error_msg'] = ruleissues
            return False
        
    # testing the internal comparison settings
    if optiondict.get('internal_compare_fields'):
        # right type
        if type(optiondict['internal_compare_fields']) != list:
            # output messages
            if optiondict['disp_msg']:
                print('internal_compare_fields must be of type list of dicts and is of type: ' + str(type(optiondict['internal_compare_fields'])))
            optiondict['error_msg'] = 'internal_compare_fields must be of type list of dicts and is of type: ' + str(type(optiondict['internal_compare_fields']))
            return False

        # check the list entries for this
        ruleissues = ''
        for rulenum, copydict in enumerate(optiondict['internal_compare_fields']):
            if not 'dst' in copydict:
                msg = f"{rulenum} missing dst key\n"
                ruleissues += msg
            if not 'src' in copydict:
                msg = f"{rulenum} missing src key\n"
                ruleissues += msg

        # if we have issue report
        if ruleissues:
            if optiondict['disp_msg']:
                print(ruleissues)
            optiondict['error_msg'] = ruleissues
            return False
        
    # debugging
    if debug or debug2:
        print('optiondict - validate_inputs:end')
        pprint.pprint(optiondict)
    if debug:
        sys.exit()
        
    # return that all is ok
    return True
    
def load_records(optiondict: dict, srctype: str='src', disp_msg: bool=False) -> list[dict]:
    """
    pass in the type of config variables we want to load from - then load and return that list of records

    we require srctype+'_dir' and srctype+'_fname' to be populated but not the other vars

    srctype can be:  src|dst
    """
    # validate srctype is set correctly
    if srctype not in ['src', 'dst']:
        raise TypeError('srctype must be src or dst')

    # validate values are set
    for fld in ['_dir', '_fname']:
        if srctype+fld not in optiondict:
            raise ValueError(srctype+fld+' must be populated')

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
                print('copy_comments:load_records:file does not exist: '+str(full_filename))
            return []

    # look up the header because we defined the required columns
    loaded_optiondict = {'sheetname': optiondict[srctype+'_ws'], 'save_row': True}

    # debuggging
    if False:
        print('loaded_optiondict:srctype:', srctype)
        pprint.pprint(loaded_optiondict)
        
    # load the file
    if srctype+'_reqcols' in optiondict and optiondict[srctype+'_reqcols']:
        loaded_data = kvxls.readxls2list_findheader(full_filename, optiondict[srctype+'_reqcols'], optiondict=loaded_optiondict)
    else:
        # load with the assumption that the first row is the header
        loaded_data = kvxls.readxls2list(full_filename, optiondict[srctype+'_ws'], optiondict=loaded_optiondict)

    # debugging
    if False:
        print(full_filename)
        print(len(loaded_data))
    
    return loaded_data

def read_src_file_format(optiondict: dict) -> None:
    """
    This reads in the src file and gets the format from it and stores it in optiondict
    """
    # set the variable - not sure why we have this here - may need to remove
    if 'disp_msg' not in optiondict:
        optiondict['disp_msg'] = True

    # get full filename
    full_filename = os.path.join(optiondict['src_dir'], optiondict['src_fname'])
    
    # check if we should load the col_width from the src_fname
    if 'src_width' in optiondict and optiondict['src_width']:
        # output messages
        if optiondict['disp_msg']:
            print('full_filename:', full_filename)
            print('Getting col_width formatting from src_fname')
        optiondict['col_width'] = kv_excel.get_existing_column_width(full_filename, ws_sheetname=optiondict.get('src_ws', None), disp_msg=optiondict['disp_msg'])
        # get hidden
        # output messages
        if optiondict['disp_msg']:
            print('Getting col_hidden formatting from src_fname')
        optiondict['col_hidden'] = kv_excel.get_existing_column_hidden(full_filename, ws_sheetname=optiondict.get('src_ws', None), disp_msg=optiondict['disp_msg'])
        # display this if they are looking for it
        if optiondict.get('src_width_disp', False):
            print('Source file col width:')
            pprint.pprint(optiondict['col_width'])
            print('Source file col hidden:')
            pprint.pprint(optiondict['col_hidden'])
            # if src_width, and src_width_disp and no_fmt - we are done processing here.
            if optiondict.get('no_fmt', False):
                print('src_width, src_width_disp and no_fmt set - exitting')
                sys.exit()

                
def validate_missing_columns(loaded_data: list[dict], optiondict: dict, fld: str) -> list:
    """
    Validate that the data has the columns required based on the list of columns defined by 'fld'
    """
    # check to see if key is even there - if not we are not missing anything
    if fld not in optiondict:
        return []
    
    # get the list of key_fields columns that don't have that key in the first record in this list
    return [x for x in optiondict[fld] if x not in loaded_data[0]]

def create_flds_in_records(loaded_data: list[dict], fields: list) -> None:
    """
    force the creation of a field if it does not exist in all records
    """
    for rec in loaded_data:
        for fld in fields:
            if fld not in rec:
                rec[fld] = ''

def convert_hyperlink_values(loaded_data: list, hyperlink_flds: list | None = None, optiondict: dict = None):
    """
    Take a list of fields and convert them to hyperlink fields
    """
    kvutil.convert_hyperlink_field_values(loaded_data, hyperlink_flds)
    
def src_to_dst_actions(src_data: list, dst_data: list , optiondict: dict) -> tuple[int, int, dict]:
    """
    take the action defined in optiondict: 
        copy_fields - None or list of column names
        internal_copy_fields - None or list of dict
                    {'src': column_name, 'dst': column_name, 'src_not_blank': bool, 'is_blank': bool }
        internal_compare_fields - None or list of dict
                    {'src': column_name, 'dst': column_name}

    optiondict must have 'key_fields' populated and as a list of column names

    internal_copy_fields Rules in rule order:
        is_blank - only update dst when dst is blank
                   when not set - update when other rules follow
        src_not_blank - copy when src_not_blank

    internal_compare_fields - sets the "internal_compare" attribute if the src/dst are not the same
        but does not tell you which fields are not matches

    returns
    matched_recs: int - number of matched records
    updated_recs: int - number of updated records
    src_lookup: dict - src_data converted to src_lookup
    """
    # test for key_fields exist, and a list
    if not 'key_fields' in optiondict:
        raise ValueError('key_fields not defined in optiondict')
    if type(optiondict['key_fields']) != list:
        raise TypeError('key_fields in optiondict not defined as list but as: ' + str(type(optiondict['key_fields'])))
    
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
        if optiondict.get('update_cnt', False):
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
        if optiondict.get('disp_msg', False):
            print('Copying data inside the file defined by internal_copy_fields')
        # copy fields in the file we just read in
        for rec in dst_data:
            # for each record in destinatoin file - get the rules
            for copydict in optiondict['internal_copy_fields']:
                # first rule - is_blank - only update when dst is blank
                if copydict.get('is_blank', False) and rec[copydict['dst']]:
                    # skip this rule - because we have the rule enabled
                    # and there is a value already in the dst column so no need
                    # to copy over
                    continue
                # second rule to fire - src_not_blank - copy over when not blank
                if copydict.get('src_not_blank', False) and not rec[copydict['src']]:
                    # skip this rule - we only copy over when the source is not blank
                    # but the source is blank - so no action here
                    continue

                # copy source when not blank
                rec[copydict['dst']] = rec[copydict['src']]

    # now compare fields interest witin the output file
    if optiondict['internal_compare_fields']:
        # output messages
        if optiondict.get('disp_msg', False):
            print('Comparing data inside the file defined by internal_compare_fields')
        # copy fields in the file we just read in
        for rec in dst_data:
            # set the original value
            rec['internal_compare'] = ''
            for copydict in optiondict['internal_compare_fields']:
                # compare and set field if
                if rec[copydict['dst']] != rec[copydict['src']]:
                    rec['internal_compare'] = 'Mismatch'
                    # we found a mismatch - we only need to find one
                    break

    return matched_recs, updated_recs, src_lookup


def removed_records(src_data: list[dict], dst_data: list[dict], optiondict: dict) -> tuple[int, dict]:
    """
    find the records in src_data that are not in dst_data

    returns
    rmv_data: int - number of removed recordss
    dst_lookup: dict - dst_data convrted to dickt

    """
    if 'key_fields' not in optiondict:
        raise Exception('key_fields not defined in optiondict')
    if not optiondict['key_fields']:
        raise Exception('key_fields defined and empty in optiondict')
    if type(optiondict['key_fields']) is not list:
        raise TypeError('key_fields defined and not list but type: ' + str(type(optiondict['key_fields'])))
    
    dst_lookup = kvutil.create_multi_key_lookup(dst_data, optiondict['key_fields'])
    rmv_data = kvutil.extract_unmatched_data(src_data, dst_lookup, optiondict['key_fields'])

    return rmv_data, dst_lookup

def added_records(src_data: list[dict], dst_data: list[dict], src_lookup: dict, optiondict: dict) -> list[dict]:
    """
    find the records in dst_data that are not in src_data
    but pass in the dictionary for src_lookup
    """
    if 'key_fields' not in optiondict:
        raise Exception('key_fields not defined in optiondict')
    if not optiondict['key_fields']:
        raise Exception('key_fields defined and empty in optiondict')
    if type(optiondict['key_fields']) is not list:
        raise TypeError('key_fields defined and not list but type: ' + str(type(optiondict['key_fields'])))

    add_data = kvutil.extract_unmatched_data(dst_data, src_lookup, optiondict['key_fields'])

    return add_data

def generate_out_output_file_not_formatted(dst_data: list[dict], optiondict: dict, updated_recs) -> None:
    """
    generate the output file is we create a new file
    or recreate the destination file if records were updated
    """
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

def generate_rmv_output_file_not_formatted(rmv_data: list[dict], optiondict: dict) -> None:
    """
    generate the remove file if defined and we have remove file records
    """
    # output what we came up with
    if 'rmv_fname' in optiondict and optiondict['rmv_fname'] and rmv_data:
        full_filename = os.path.join(optiondict['rmv_dir'], optiondict['rmv_fname'])
        kvxls.writelist2xls(full_filename, rmv_data)
        if 'debug' in optiondict and optiondict['debug']:
            print('rmv_write:', str(full_filename))
        if 'disp_msg_add_rmv' in optiondict and optiondict['disp_msg_add_rmv']:
            print('Record count: ', len(rmv_data))
            print('Created file: ' + str(full_filename))

def generate_add_output_file_not_formatted(add_data: list[dict], optiondict: dict) -> None:
    """
    generate the add file if defined and we have remove file records
    """
    # output what we came up with
    if 'add_fname' in optiondict and optiondict['add_fname'] and add_data:
        full_filename = os.path.join(optiondict['add_dir'], optiondict['add_fname'])
        kvxls.writelist2xls(full_filename, add_data)
        if 'debug' in optiondict and optiondict['debug']:
            print('add_write:', str(full_filename))
        if 'disp_msg_add_rmv' in optiondict and optiondict['disp_msg_add_rmv']:
            print('Record count: ', len(add_data))
            print('Created file: ' + str(full_filename))


def format_output(optiondict):
    """
    Format the output file based on flags passed in
    or when the 'fmt_fname' is set - then save the configuratoin out to a json file
    """
    
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

    # debugging
    if False:
        print('format_output: optiondict')
        pprint.pprint(optiondict)
    
    # special output json - if exists and populated
    if optiondict.get('create_json'):
        # split up the input filename
        fdir, fname = os.path.split(optiondict['create_json'])

        # create the output json standard configuration
        output = {
            'descr': 'put a description here',
            'src_dir': fdir,
            'src_fname': fname,
            'dst_dir': fdir,
            'dst_fname': fname,
            'copy_fields': [],
            'key_fields': [] if not optiondict.get('key_fields') else optiondict['key_fields'],
            'hyperlink_fields': [],
            'format_output': True,
            'format_cell': False,
            'src_width': False,
            'col_width': optiondict['col_width'],
            'col_hidden': optiondict['col_hidden'],
        }
        # add in sheets if they are set
        if optiondict.get('src_ws'):
            output['src_ws'] = optiondict['src_ws']
            output['dst_ws'] = optiondict['src_ws']

        # output this 
        full_filename = os.path.join(optiondict['fmt_dir'], optiondict['fmt_fname'])
        kvutil.dump_dict_to_json_file(full_filename,output)
        # output messages
        if 'disp_msg' in optiondict and optiondict['disp_msg']:
            print('Saved format json to:' + str(full_filename))
        # if no_fmt is enabled we are done - and we are generating the output format file
        if optiondict.get('no_fmt', False):
            print('no_fmt set - generated output format - ending program')
            sys.exit()
        
    # if we set fmt_fname then save this col width data
    if 'fmt_fname' in optiondict and optiondict['fmt_fname']:
        full_filename = os.path.join(optiondict['fmt_dir'], optiondict['fmt_fname'])
        kvutil.dump_dict_to_json_file(full_filename,
                                      {
                                          "col_width": optiondict['col_width'],
                                          "col_hidden": optiondict['col_hidden'],
                                      })
        # output messages
        if 'disp_msg' in optiondict and optiondict['disp_msg']:
            print('Saved col_width + col_hidden to:' + str(full_filename))
        # if no_fmt is enabled we are done - and we are generating the output format file
        if optiondict.get('no_fmt', False):
            print('no_fmt set - generated output format - ending program')
            sys.exit()
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
            print('col_hidden we reformat with:')
            pprint.pprint(optiondict['col_hidden'])
    # if there is no work to do  - then do not format the output file
    if optiondict['no_fmt']:
        if disp_msg:
            print('no formatting applied - no_fmt enabled')
        return
    # if there is no work to do  - then do not format the output file
    if not (optiondict.get('col_width') or optiondict.get('col_hidden') or optiondict.get('format_auto')):
        if disp_msg:
            print('no formatting applied - no formatting specified in col_width, col_hidden, format_auto')
        return
    # messaging
    if optiondict.get('format_auto') and disp_msg and not optiondict.get('col_width'):
        print('format_auto enabled and no col_width defined')
    # format this file with what is defined in col_width
    kv_excel.format_xlsx_with_filter_and_freeze(excel_filename, col_width=optiondict['col_width'], col_hidden=optiondict['col_hidden'], disp_msg=disp_msg)

def format_cell(optiondict):
    """
    Copy over cell based formatting
    """
    
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
    """
    generate the output file is we create a new file
    or recreate the destination file if records were updated
    """
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
    #print('read in')
    #pprint.pprint(optiondict)
    # sys.exit()

    # check for file existenace
    if optiondict['ignore_missing_src']:
        # check for existence of the src file
        full_filename = os.path.join(optiondict['src_dir'], optiondict['src_fname'])
        if not os.path.exists(full_filename):
            # output messages
            if optiondict['disp_msg']:
                print('SRC File does not exist - moving along: '+str(full_filename))
            sys.exit()
    if optiondict['ignore_missing_dst']:
        # check for existence of the dst file
        full_filename = os.path.join(optiondict['dst_dir'], optiondict['dst_fname'])
        if not os.path.exists(full_filename):
            # output messages
            if optiondict['disp_msg']:
                print('DST File does not exist - moving along: '+str(full_filename))
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

    # set the key fields if not set
    if optiondict.get('create_json') and not optiondict.get('key_fields'):
        if 'XLSRow' in src_data[0].keys():
            optiondict['key_fields'] = ['XLSRow']
        elif 'XLSRowAbs' in src_data[0].keys():
            optiondict['key_fields'] = ['XLSRowAbs']
        else:
            optiondict['key_fields'] = [list(src_data[0].keys())[0]]

    # debugging
    if False and optiondict.get('create_json'):
        print('Option Dict with the Key Fields set')
        pprint.pprint(optiondict)

        
    # read in format for src file if we want it
    read_src_file_format(optiondict)

    # Debugging
    if False:
        print('heading out of read_src_file_format')
        pprint.pprint(optiondict)
    
    # check that we have the key fields in the src_data
    missing_cols = validate_missing_columns(src_data, optiondict, 'key_fields')
    if missing_cols:
        # output messages
        if optiondict['disp_msg']:
            print('You are MOST LIKELY reading in the wrong src sheet as we can not find column(s): ',
                  '|'.join(missing_cols) )
            print('Columns we have found are: ',
                  '|'.join(src_data[0].keys()) )
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
        convert_hyperlink_values(src_data, optiondict['hyperlink_fields'], optiondict)
        convert_hyperlink_values(dst_data, optiondict['hyperlink_fields'], optiondict)

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

    if False:
        print('heading into format_output')
        pprint.pprint(optiondict)
    
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
