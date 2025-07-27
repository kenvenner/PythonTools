'''
@author:   Ken Venner
@contact:  ken.venner@hermeus.com
@version:  1.11

This library provides tools used when interacting with sharepoint sites and local synch links to sharepoint sites

'''

import os
import time

import kvxls
import kvutil
import kvcsv

import copy_comments

# global variables
AppVersion = '1.11'


# LOCAL FUNCTIONS/HELPERS
# ----------------------------------------

def sp_synched_dir_path(sp_path, onedrive_path=None, local_path=None, debug=False):
    '''
    For mac and windows return back the path to the synched folder in sharepoint of interest

    sp_path - the sharepoint name and folder path to the directory of interest
       e.g.:  "/NetSuite Implementation - Documents/Master Mapping Files/output/"
    onedrive_path - the path from HOME/HOMEPATH to the location where sharepoint files are synched
       can be empty - will default if not set
    local_path - the path to return if the sp path does not exist

    requires:  import os
    '''

    # strip the starting dir
    if sp_path[0] in '/\\':
        sp_path = sp_path[1:]
    
    if onedrive_path is None:
        # default locations that sharepoint synchs on onedrive
        if os.name == "posix":
            # mac
            onedrive_path = "Library/CloudStorage/OneDrive-SharedLibraries-HermeusCorp/"
        else:
            # windows
            onedrive_path = "Hermeus Corp/"
    else:
        # not the default path - make sure the path does not start with dir symbol
        if onedrive_path[0] in '/\\':
            onedrive_path = onedrive_path[1:]

    # calculate the homedir for this user
    home_dir = ''
    
    # Define the master directory path using the home directory
    if os.name == "posix":
        home_dir = os.environ.get("HOME")
    else:
        home_dir = os.environ.get("HOMEPATH")

    # debugging outputs
    if debug:
        print('home_dir', home_dir)
        print('onedrive_path', onedrive_path)
        print('sp_path', sp_path)

    # make the path the concatenation of the parts
    sp_full_path = os.path.join(home_dir, onedrive_path, sp_path)


    # debugging outputs
    if debug:
        print('sp_full_path:', sp_full_path)

    # check for existance of this sharepoint path
    if os.path.exists(sp_full_path):
        return sp_full_path
    else:
        return local_path


def save_and_log_dbms_extract(excel_file_path, result, starttime, now, log_file_path, log_filename=None):
    '''
    Create the screen output and log file update for the dbms extract

    excel_file_path - full path and filename to output xlsx
    result - dataframe created from execution of SQL
    start_time - time.time() timer start
    now - datetime.datetime.now() at start of execution
    log_file_path - the path to where the log of run times is stored
    log_filename - name of hte log filename that houses the results
    
    '''

    if not log_file_path:
        print('must provide a file_path to the log file')
        sys.exit(1)
    # make sure we have the end directory string on this input string
    if log_file_path[-1] != '/':
        log_file_path += '/'

    # default the filename
    if not log_filename:
        log_filename = 'dbms_dump_log.csv'

    # create the full filename
    log_full_filename = log_file_path + log_filename

    # check to see if log exists
    log_exists = os.path.exists( log_full_filename )
    
    
    # Write the DataFrame to an Excel file
    result.to_excel(excel_file_path, index=False, header=True)

    print("Record Count:  ", len(result.index))
    print("Data exported to Excel file successfully: " + excel_file_path)

    # capture adn display run time
    endtime = time.time()
    print('PROGRAM EXECUTION TIME: ', (endtime-starttime)/60, 'min')

    # open the log file and output record
    with open(log_file_path+log_filename, 'a') as fp:
        # create header if the file did not exist
        if not log_exists:
            fp.write(','.join(['excel_file_path', 'run_time', 'record_cnt', 'exec_time_min'])+'\n')
        # output results
        fp.write(f'{excel_file_path},{now.isoformat()},{len(result.index)},{(endtime-starttime)/60}\n')


def save_and_log_exception_rpt(excel_file_path, result, starttime, now, log_file_path, log_filename=None, flds=None, cc_cfg=None, cc_args=None, cc_src_files=None, disp_msg=False):
    '''
    Create the screen output and log file update for the dbms extract

    excel_file_path - full path and filename to output xlsx
    result - dataframe created from execution of SQL
    start_time - time.time() timer start
    now - datetime.datetime.now() at start of execution
    log_file_path - the path to where the log of run times is stored
    log_filename - name of hte log filename that houses the results
    flds - list of fields to output to xlsx (if set)

    cc_cfg = filename of JSON copy_comments optiondict configuration options
    cc_args = dictionary of command line args that override the cc_cfg settings
    
    cc_src_files - list of src files to loop through to pull in data to copy over, if None - use what is defined in cc_cfg

    disp_msg - when true we output messages about what is going on with print statements

    '''

    if not log_file_path:
        print('must provide a file_path to the log file')
        sys.exit(1)
    # make sure we have the end directory string on this input string
    if log_file_path[-1] != '/':
        log_file_path += '/'

    # default the filename
    if not log_filename:
        log_filename = 'exception_rpt_log.csv'

    # create the full filename
    log_full_filename = log_file_path + log_filename

    # check to see if log exists
    log_exists = os.path.exists( log_full_filename )

    # take action if you have to copy_comments
    if cc_cfg:
        # get configuration options
        if not cc_args:
            cc_args = {}
        elif type(cc_args) != dict:
            raise KeyError('cc_args must be a dictionary but is a: '+type(cc_args))
        # set up the pass in values
        cc_args['conf_json'] = cc_cfg
        # now read in the JSON configuration
        cc_optiondict = kvutil.kv_parse_command_line(copy_comments.optiondictconfig, cmdlineargs=cc_args, skipcmdlineargs=True)

	# capture the original src_dir
        orig_src_dir = cc_optiondict['src_dir']
	
	# there are times we need to load update data from more than one source file
        if cc_src_files is None:
            # not specified - so use the single source file that was sent in
            cc_src_files = [cc_optiondict['src_fname']]

        # step through each of the src files
        for src_fullfilename in cc_src_files:
            # split the filename up into parts
            src_dir = os.path.dirname(src_fullfilename)
            src_file = os.path.basename(src_fullfilename)
            # if a directory was in this filename
            if src_dir:
                # use the path passed in with the override file
                cc_optiondict['src_dir'] = src_dir
            else:
                # use the path stored in the config file
                cc_optiondict['src_dir'] = orig_src_dir
            # now pull the filename and replace it in this file
            cc_optiondict['src_fname'] = src_file
            
            # debugging
            if disp_msg:
                print('src_file: ', cc_optiondict['src_fname'])
            
            # validate these configuration options
            copy_comments.validate_inputs(cc_optiondict)
        
            # read in the previous data for this file - copy over any data that was in that file
            src_data = copy_comments.load_records(cc_optiondict, 'src')

            # read in the columns widths if this is defined to be done
            copy_comments.read_src_file_format(cc_optiondict)

            # update the destination arrray based on source data
            matched_recs, updated_recs, src_lookup = copy_comments.src_to_dst_actions(src_data, result, cc_optiondict)
        
            # get the removed records
            rmv_data, dst_lookup = copy_comments.removed_records(src_data, result, cc_optiondict)

            # debugging
            if disp_msg:
                print('src_data: ', len(src_data))
                print('matched.: ', matched_recs)
                print('updated.: ', updated_recs)
                print('rmv_recs: ', len(rmv_data))
            
                  
            # and if we have removed records generate them
            copy_comments.generate_rmv_output_file_not_formatted(rmv_data, cc_optiondict)
    
    # Write the DataFrame to an Excel file
    if result:
        # print(flds)
        kvxls.writelist2xls(excel_file_path, result, flds)
        # now apply formatting to this newly create file
        if cc_cfg:
            copy_comments.format_output(cc_optiondict)
        print('Record count: ', len(result))
        print("Created file:  ", excel_file_path)
    else:
        kvutil.remove_filename(excel_file_path)
        print('No exceptions found')
        
    # capture adn display run time
    endtime = time.time()

    # open the log file and output record
    with open(log_file_path+log_filename, 'a') as fp:
        # create header if the file did not exist
        if not log_exists:
            fp.write(','.join(['excel_file_path', 'run_time', 'record_cnt', 'exec_time_min'])+'\n')
        # output results
        fp.write(f'{excel_file_path},{now.isoformat()},{len(result)},{(endtime-starttime)/60}\n')

        
def save_lot_serial_csv_exception_rpt(excel_file_path, result, lotfield='islotitem'):
    '''
    Create the CSV output files for lot and serial to simplify the load into netsuite

    excel_file_path - full path and filename to output xlsx
    result - dataframe created from execution of SQL
    '''

    # remove the .xlsx and then put on the _Lot.csv
    lot_fname = excel_file_path[:-5]+"_Lot.csv"
    serial_fname = excel_file_path[:-5]+"_Serial.csv"

    # now build the two arrays
    lot_recs = [x for x in result if x[lotfield] == 'T']
    serial_recs = [x for x in result if x[lotfield] == 'F']

    # now output the two results
    if lot_recs:
        kvcsv.writelist2csv(lot_fname, lot_recs)
        print('Record count: ', len(lot_recs))
        print("Created file:  ", lot_fname)
    else:
        kvutil.remove_filename(lot_fname)
    if serial_recs:
        kvcsv.writelist2csv(serial_fname, serial_recs)
        print('Record count: ', len(serial_recs))
        print("Created file:  ", serial_fname)
    else:
        kvutil.remove_filename(serial_fname)
        

def set_master_dir_strings():
    
    master_download_dir = '/Users/KenVenner/Downloads/'
    master_dir = sp_synched_dir_path("/NetSuite Implementation - Documents/Master Mapping Files/")
    master_output_dir = sp_synched_dir_path("/NetSuite Implementation - Documents/Master Mapping Files/output/static/")
    master_static_dir = sp_synched_dir_path("/NetSuite Implementation - Documents/Master Mapping Files/output/static/")
    master_mnfro_dir = sp_synched_dir_path("/NetSuite Implementation - Documents/Master Mapping Files/Manufacturo DataSets/")
    master_ns_dir = sp_synched_dir_path("/NetSuite Implementation - Documents/Master Mapping Files/NetSuite DataSets/")
    master_error_dir = sp_synched_dir_path("/NetSuite Implementation - Documents/Master Mapping Files/error/")

    return master_download_dir, master_dir, master_output_dir, master_static_dir, master_mnfro_dir, master_ns_dir, master_error_dir

#eof
