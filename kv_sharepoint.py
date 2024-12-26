'''
@author:   Ken Venner
@contact:  ken.venner@hermeus.com
@version:  1.06

This library provides tools used when interacting with sharepoint sites and local synch links to sharepoint sites

'''

import os
import time

import kvxls
import kvutil
import kvcsv


# global variables
AppVersion = '1.06'


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


def save_and_log_exception_rpt(excel_file_path, result, starttime, now, log_file_path, log_filename=None):
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
        log_filename = 'exception_rpt_log.csv'

    # create the full filename
    log_full_filename = log_file_path + log_filename

    # check to see if log exists
    log_exists = os.path.exists( log_full_filename )
    
    
    # Write the DataFrame to an Excel file
    if result:
        kvxls.writelist2xls(excel_file_path, result)
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
        


#eof
