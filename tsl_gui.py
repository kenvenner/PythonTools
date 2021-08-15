__version__ = '1.01'

import PySimpleGUI as sg
import tsl_func
import os
import kv_psg
from attrdict import AttrDict
import logging

# may comment out in the future
import pprint

pp = pprint.PrettyPrinter(indent=4)

# logging
logger = logging.getLogger(__name__)

# when set true we are debugging the screen - generate outputs and dont' perform functions
AppDebug = False


# Generic screen used to drive the generatoin of the trusted share listing
# to console and/or to a file


def create_dump_data_window(settings, cfg_folder):
    """
    dump data from CWP to XLS screen
    """

    def TextLabel(text):
        return sg.Text(text + ':', justification='r', size=(15, 1))

    def TextInput(text, key=None):
        if key is None:
            key = f"-{text.upper()}-"
        return [TextLabel(text), sg.Input(key=key)]

    def CheckboxFileSaveAs(text, key, default_text, default_folder):
        keychkbox = f"-{key.upper()}_CHKBOX-"
        key = f"-{key.upper()}-"
        text = text + ':'
        return [sg.Checkbox(text, default=False, key=keychkbox), 
                sg.Input(key=key, default_text=default_text), sg.FileSaveAs(initial_folder=default_folder, target=key)]

    layout = [
        [sg.T('Select checkbox and enter file names of output files to generate', size=(50, 1))],
        [sg.Checkbox('Display listing to screen', default=True, key=tsl_func.DISPLAY_KEY)],
        CheckboxFileSaveAs('TS Dump file', 'ts_dump', 'ts_dump.xlsx', cfg_folder),
        [sg.B('Ok'), sg.B('Exit')]
    ]

    return sg.Window('e-Share Trusted Share Listing', layout)


def display_ts_listing_window(list_lines):
    """
    generate ts listing to a new window

    :param list_lines: (list) - list to be output

    """

    def TextLabel(text):
        return sg.Text(text + ':', justification='r', size=(15, 1))

    def TextInput(text, key=None):
        if key is None:
            key = f"-{text.upper()}-"
        return [TextLabel(text), sg.Input(key=key)]

    layout = [
        [sg.Output(size=(100, 10), key='ts_listing', font=('Courier', 11))],
        [sg.Button('Done', disabled=True)]
    ]

    window = sg.Window('e-Share Trusted Share Listing', layout, finalize=True)

    buffer = '\n'.join(list_lines)

    # fill in the data to the window
    window['ts_listing'].update(value=buffer)

    # enable the done button
    window['Done'].update(disabled=False)

    # close the window when the button is selected
    window.read(close=True)


#
#############################################################

# this is an application specific implementation not a generic tool
# but this is a pattern that is repeated
def tsl_main(settings, cfg_folder, obj_class, token, url):
    """
    Logic driving the TS listing to display and file features

    :param settings:
    :param cfg_folder:
    :param obj_class: 
    :param token:
    :param url:

    may need to pass in a pointer to the object that we call 
    that will get the list of ts and that generates the output
    I assume this routine will carry the save to file function

    """

    # display a new screen to collect new data
    # because read(close=True) the window is closed when they select an option
    event, values = create_dump_data_window(settings, cfg_folder).read(close=True)

    # second level screen event handler
    if event == 'Ok':

        # set the value based on if we are going to display on the screen
        option_enabled = False if not values[tsl_func.DISPLAY_KEY] else True
        
        # update values based on what was entered in the screen
        # for things that generate output files
        for opt in ['TS_DUMP']:
            if not values[f'-{opt}_CHKBOX-']:
                # not set to true - so clear out the value
                values[f'-{opt}-'] = ''
            else:
                # set the option if they selected one of the file outputs
                option_enabled = True
                # set to true - so lets make sure the filename is correct
                if not os.path.dirname(values[f'-{opt}-']):
                    values[f'-{opt}-'] = os.path.join(settings['cfg_folder'], values[f'-{opt}-'])

        # debugging
        if AppDebug:
            print('dump the data out to files')
            print('settings:')
            pp.pprint(settings)
            print('values:')
            pp.pprint(values)
            print('v2s:')
            pp.pprint(v2s)

        # validate an option is selected otherwise return
        if not option_enabled:
            return

        # Execute the actions requested
        try:
            # create the object that will perform the work
            tsl_obj = tsl_func.TSListing(obj_class, token, url)
            
            # now set up for logging to window
            logger_window = kv_psg.setup_logger_console_window()
            # run through steps to get the data and output files if we are outputtting files
            kv_psg.output_logger_console_window(logger_window,
                                                tsl_obj.ts_listing_steps,
                                                values)

            if values[tsl_func.DISPLAY_KEY]:
                display_ts_listing_window(tsl_obj.ts_listing_lines)

            # check to see if any of the files were checked as being extracted
            # values: {'-TS_DUMP_CHKBOX-': True, '-TS_DUMP-': 'ts_dump.xlsx',
            # 'Save As...': '', '-COLLAB_DUMP_CHKBOX-': False, '-COLLAB_DUMP-': 'collab_dump.xlsx',
            # 'Save As...0': ''}
            # values: {'-TS_DUMP_CHKBOX-': True, '-TS_DUMP-':
            # 'C:/Users/ken/AppData/Roaming/e-share/ts-dump.xlsx',
            # 'Save As...': 'C:/Users/ken/AppData/Roaming/e-share/ts-dump.xlsx',
            # '-COLLAB_DUMP_CHKBOX-': False, '-COLLAB_DUMP-': 'collab_dump.xlsx',
            # 'Save As...0': ''}
            # we should also check to see if we got back just a filename or a full path
            # if just filename - then build the full path as the cfg_folder + filename, if full path - we are done
            # and if so - set the vargs based on what was passed back
            # and call the routine that reads data from CWP and creates the output files
        except Exception as e:
            print(e)
            sg.popup('ERROR - Failed to process trusted share listing', e)

