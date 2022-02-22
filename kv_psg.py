__version__ = '1.20'

import PySimpleGUI as sg
import os
import json
import copy
from pathlib import Path, PurePath
import sys
import traceback
import logging

logger = logging.getLogger(__name__)

# this is the reusable code to create a window to capture the logger output in GUI

# Global variable used to capture log entries
buffer = ''
parent_get_log_filename = None

class Handler(logging.StreamHandler):
    """
    Logging handler that puts outputs into a GUI window

    called by:  setup_logger_console_window() in this file

    then called by:  output_logger_console_window() to have logger.info output to a GUI window

    """

    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.window = None
        self.key = None

    def set_window(self, window, key):
        """
        Set the window variable - what we output into
        Set the key variable - the variable we output into

        :params window: (PySimpleGui.window)
        :params key: (key) - of the field the output is put into
        """
        self.window = window
        self.key = key

    def emit(self, record):
        global buffer
        record = f'{record.name}, [{record.levelname}], {record.message}'
        buffer = f'{str(record)}\n{buffer}'.strip()
        self.window[self.key].update(value=buffer)
        self.window.Refresh()


class MsgPopup(object):
    """
    Helper function that allows you to set up for a function a setting that controls
    if message popups display or not.
    When the object is created you set the flag and this controls if we display a popup or not
    
    msg = kv_psg.MsgPopup(False)
    if <issue>:
        msg.popup('text','text')

    """

    def __init__(self, disp_popup=True):
        """
        Create the popup object - and set the flag if it is to display or not when called

        :params disp_popup: (bool) - defines if we display a popup or not when called
        """

        self.disp_popup = disp_popup

    def popup(self, *args):
        """
        if disp_popup is true - then display the PySimpleGui popup with parameters passed in"

        :params *args: args passed into sg.popup()
        """
        if self.disp_popup:
            sg.popup(*args)


def set_get_log_filename(func_name):
    """
    Set the function name the determines the log file name

    :param func_name: (func) that calculates the log filename
    """
    global parent_get_log_filename

    parent_get_log_filename = func_name


def setup_logger_console_window(key='log'):
    """
    The function you call to setup an application to log into a GUI windows

    this function is called AFTER you call:  
        initialize_logging(vargs.log_path, not vargs.no_console, not vargs.no_logfile)

    called as:  vargs['window'] = kv_psg.setup_logger_console_window()

    :params key: (string) - the key to the element you will update with logger data

    :returns PySimpleGui.window: the window created for update/outputs

    """
    global buffer
    buffer = ''
    ch = Handler()
    ch.setLevel(logging.INFO)
    logging.getLogger('').addHandler(ch)

    # Very basic window.
    layout = [
        [sg.Output(size=(100, 10), key=key)],
        [sg.Button('Done', disabled=True)]
    ]

    # needed to add 'finalize=True' so we don't need the read we can
    # just put outputs into this window
    window = sg.Window('Logger Output', layout, finalize=True)

    # pass the window value in for logging purposes
    ch.set_window(window, key)

    # put a message into the window
    logging.info('Running...')

    return window


# right in and start execution and then only need the Done button
def output_logger_console_window(window, called_function, *args):
    """
    function to cause logger output from "called_function" to be output to GUI window

    this function is called instead of calling the console based function
    and you pass in function name and argument list of hte function you would have called as 
    the console function

    when done - we clean up and close out the console GUI window

    example:
    if vargs.gui:
         logger_window = kv_psg.setup_logger_console_window()
         call_some_intermediate_function()
         kv_psg.output_logger_console_window(logger_window, validate_input_and_exit_early, req_flds, vargs)
    else:
         validate_input_and_exit_early(req_flds, vargs)


    called as:  kv_psg.output_logger_console_window(vargs['window'], function, function_args)

    :params window: (PySimpleGui.Window)
    :params called_function:  (function ref)
    :params *args: (arguments list) to called_function

    """
    # call the function and allow its logging data to be output to the GUI window
    error = None
    result = None
    try:
        result = called_function(*args)
    except Exception as e:
        error = e
        logger.error('%s', traceback.format_exc())

    # when done - enable the done button so we can now click it
    window.find_element('Done').Update(disabled=False)
    # put out the final logging message
    logging.info('Finished...press the Done Button...')

    # then drop into the event loop to capture the Done button
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Done':
            break

    # close the window that displayed this work
    window.close()

    # now remove the last added handler
    logging.getLogger().handlers.pop()

    # return back what came back from the function call
    return result


# right in and start execution and then only need the Done button
def output_logger_console_window_with_err_handler(window, called_function, *args):
    """
    function to cause logger output from "called_function" to be output to GUI window

    this function is called instead of calling the console based function
    and you pass in function name and argument list of hte function you would have called as 
    the console function

    when done - we clean up and close out the console GUI window

    example:
    if vargs.gui:
         logger_window = kv_psg.setup_logger_console_window()
         call_some_intermediate_function()
         kv_psg.output_logger_console_window(logger_window, validate_input_and_exit_early, req_flds, vargs)
    else:
         validate_input_and_exit_early(req_flds, vargs)


    called as:  kv_psg.output_logger_console_window(vargs['window'], function, function_args)

    :params window: (PySimpleGui.Window)
    :params called_function:  (function ref)
    :params *args: (arguments list) to called_function

    """
    # call the function and allow its logging data to be output to the GUI window
    error = None
    try:
        _ = called_function(*args)
    except Exception as e:
        error = e
        logger.error('%s', traceback.format_exc())

    # when done - enable the done button so we can now click it
    window.find_element('Done').Update(disabled=False)
    # put out the final logging message
    logging.info('Finished...press the Done Button...')

    # then drop into the event loop to capture the Done button
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Done':
            break

    # close the window that displayed this work
    window.close()

    # now remove the last added handler
    logging.getLogger().handlers.pop()

    # return back what came back from the function call
    return error


# ************  GUI based logger output *******************


# ********** Concepts for putting a GUI start on a screen *****************

def calc_values_key_2_settings_key(vargs, v2s=None):
    """
    For each entry in vargs - create a PySimpleGUI key for that key

    :params vargs: (dict) - program options that are GUI candidates
    :params v2s: (dict) - predefined value to key definitions
    """
    if v2s is None:
        v2s = dict()
    else:
        v2s = copy.deepcopy(v2s)

    # step through the keys in vargs and
    for k in vargs:
        v2s[k] = f"-{k.upper()}-"
    return v2s


def config_folder(sub_folder_list):
    """
    Defines where configuration files for the tool are placed and read from

    Find the starting folder using env vars
    Then create subfolders to provide a location to act as the working folder

    called as:  cfg_folder = config_folder(['e-share','ts_maintain'])

    :params sub_folder_list: (list) - list of subdirectories 

    :returns cfg_folder: (string) - path to the working folder
    """

    # find the folder to work from
    for folder_var in ('APPDATA', 'LOCALAPPDATA', 'TEMP', 'TMP', 'HOMEPATH'):
        app_folder = os.environ.get(folder_var)
        if app_folder and os.path.isdir(app_folder):
            break

    if not app_folder:
        return None

    # check for and build up the path folder(s)
    for sub_folder in sub_folder_list:
        app_folder = os.path.join(app_folder, sub_folder)
        # test to see if our folder exists
        if not os.path.isdir(app_folder):
            os.mkdir(app_folder)

    return app_folder



def load_settings(settings_file, default_settings, values_key_2_settings_key):
    """
    Load in the settings from the settings_file

    Add two settings
        cfg_folder - folder we put configuration data into
        settings_file - filename of the settings file

    :params settings_file: (string) - file/path to the settings file
    :params default_settings: (dict) - default settings when we don't read any settings in
    :params values_key_2_settings_key: (dict) - mapping of keys in GUI to keys in settings
    """
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
        settings['cfg_folder'] = os.path.dirname(settings_file)
    except json.decoder.JSONDecodeError as e:
        # report error when we struggle to read the JSON 
        import re
        with open(settings_file, 'r') as json_error:
            json_lines = json_error.readlines()
        err_line = re.search(r'line\s+(\d+)\s+', str(e))
        logger.warning('-' * 40)
        if err_line:
            err_line_int = int(err_line.group(1))
            if err_line_int < len(json_lines):
                logger.warning('Error on line: %s', err_line_int)
                logger.warning(json_lines[err_line_int - 1])
            logger.warning('-' * 40)
        raise
    except FileNotFoundError:
        sg.popup_quick_message('\nNo settings file found... will create one for you\n',
                               keep_on_top=True,
                               background_color='red',
                               text_color='white')
        settings = default_settings
        settings['cfg_folder'] = os.path.dirname(settings_file)
        # make this a str not a WindowsPath in order to make it JSON able
        settings['settings_file'] = str(settings_file)
        save_settings(settings_file, settings, None, values_key_2_settings_key)

    # fill in missing default values
    for k, v in default_settings.items():
        if k not in settings:
            settings[k] = v

    return settings


def update_settings(settings, values, values_key_2_settings_key):
    """
    Update the settings based on the recent values passed back from the window

    Remove the following keys from the settings:
        conf
        conf_files_loaded

    :params settings_file: (string) - file/path to the settings file
    :params settings: (dict) - key/value application settings
    :params values: (dict) - key/value coming from GUI updates - these values are
                             remapped and updates values in settings
    :params values_key_2_settings_key: (dict) - key mapping from GUI values to app settings

    """
    global parent_get_log_filename

    # remove keys that should not remain
    for k in ('conf', 'conf_files_loaded'):
        if k in settings:
            del settings[k]

    # update settings if there are values to update
    not_updated = dict()
    if values:
        if '-LOG_PATH-' in values:
            # TODO - not sure why we are changing this to a file name and not just a path
            if parent_get_log_filename and Path(values['-LOG_PATH-']).is_dir():
                # print('change to get to a file')
                values['-LOG_PATH-'] = parent_get_log_filename(values['-LOG_PATH-'])
            values['-LOG_PATH-'] = str(values['-LOG_PATH-'])

        # update window with the values read from settings file
        for k, v in values_key_2_settings_key.items():
            try:
                if v in values:
                    settings[k] = values[v]
            except Exception as e:
                #
                # pass
                not_updated[k] = {
                    'v': v,
                    'e': e
                }

        # debugging enabled when we want to see failed updates
        if False:
            print(not_updated)


def save_settings(settings_file, settings, values, values_key_2_settings_key):
    """
    Save the app settings defined by settings in file defined by settings_file

    :params settings_file: (string) - file/path to the settings file
    :params settings: (dict) - key/value application settings
    :params values: (dict) - key/value coming from GUI updates - these values are
                             remapped and updates values in settings
    :params values_key_2_settings_key: (dict) - key mapping from GUI values to app settings

    """

    # if there are stuff specified by another window, fill in those values
    try:
        update_settings(settings, values, values_key_2_settings_key)
    except Exception as e:
        print(e)
        raise

    # save the settings values out to the file
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

            sg.popup('Settings saved at:\n' + settings_file)
    except Exception as e:
        sg.popup_quick_message(f'\nFailed to create settings_file:\n{settings_file}\nError:{e}\n', keep_on_top=True,
                               background_color='red', text_color='white')


# ***************** Make a settings window ***********************
def update_windows_values(window, settings, values_key_2_settings_key):
    """
    Update displayed window with values read in from settings file

    :param window:
    :param settings:
    :param values_key_2_settings_key:
    """

    for k, v in values_key_2_settings_key.items():
        if v in window.AllKeysDict:
            try:
                if k in ('settings_file', 'log_path', 'cfg_folder',):
                    window[v].update(value=str(Path(settings[k])))
                else:
                    window[v].update(value=settings[k])
            except Exception:
                # print(f'Problem updating PySimpleGUI window from settings. Key = {k}')
                pass

    # special processing - capturing the settings_file
    # may be able to remove this section
    for k in ('settings_file', 'log_path'):
        # k = 'settings_file'
        v = f"-{k.upper()}-"
        if v in window.AllKeysDict:
            try:
                window[v].update(value=str(Path(settings[k])))
            except Exception:
                # print(f'Problem updating PySimpleGUI window from settings. Key = {k}')
                pass

    window.Refresh()


def create_settings_window(settings, values_key_2_settings_key, app_version):
    """
    Generic application settings windows for editting app setting values
    and display the current application version number

    Values set:
        token
        URL
        log_path
        log_console
        log_file
        clear_logs

    :params settings: (dict) - key/value application settings
    :params values_key_2_settings_key: (dict) - mapping from settings to GUI keys

    """

    def TextLabel(text):
        return sg.Text(text + ':', justification='r', size=(15, 1))

    def TextInput(text, key=None):
        if key is None:
            key = f"-{text.upper()}-"
        return [TextLabel(text), sg.Input(key=key, size=(70, 1))]

    layout = [[sg.Text('Settings', font='Any 15')],
              TextInput('Token'),
              TextInput('URL'),
              [TextLabel('Log Folder'), sg.Input(key='-LOG_PATH-', size=(62, 1)), sg.FolderBrowse(target='-LOG_PATH-')],
              [TextLabel('Log to console:'), sg.Checkbox('', default=False, key='-LOG_CONSOLE-')],
              [TextLabel('Log to file:'), sg.Checkbox('', default=True, key='-LOG_FILE-')],
              [TextLabel('Clear log on startup:'), sg.Checkbox('', default=False, key='-CLEAR_LOGS-')],
              [TextLabel('Application version'), sg.Text(app_version)],
              [TextLabel('Settings file'), sg.Input(key='-SETTINGS_FILE-', size=(70, 1))],
              [sg.Button('Save'),
               sg.Button('Exit'),
               sg.Input(key='-SAVE_AS-', visible=False, enable_events=True),
               sg.FileSaveAs('SaveAs', key='-SAVE_AS-', file_types=(('Cfg', '*.json'),),
                             initial_folder=settings.get('cfg_folder', '')),
               sg.Input(key='-LOAD-', visible=False, enable_events=True),
               sg.FileBrowse('Load', key='-LOAD-', file_types=(('Cfg', '*.json'),),
                             initial_folder=settings.get('cfg_folder', '')),
               sg.Button('Edit'),
               sg.Button('ViewLog')]]

    window = sg.Window('Settings', layout, finalize=True)

    # cause values in this screen to update
    update_windows_values(window, settings, values_key_2_settings_key)

    return window


def open_in_notepad(input):
    """
    Cause the settings file JSON to be opened in notepad

    :param input: (str) filename of the file to be opened
    """
    logger.info('Editted file in notepad: %s', input)
    editted_file = os.system(f'notepad "{input}"')


def reinitialize_logging(vargs, settings, parent):
    logger.info('Check for change in logging settings')
    value_diff = False
    # force the value to be a directory not a full filename
    if not os.path.isdir(vargs['log_path']):
        vargs['log_path'] = os.path.dirname(vargs['log_path'])
    if not os.path.isdir(settings['log_path']):
        settings['log_path'] = os.path.dirname(settings['log_path'])
    # now check for differences
    for k in ('log_path', 'log_console', 'log_file'):
        if vargs.get(k) != settings.get(k):
            logger.info('Setting changed: %s',
                        {'key': k,
                         'vargs[key]': vargs.get(k),
                         'settings[key]': settings.get(k)})
            value_diff = True
            break
    if value_diff:
        logger.info('Calling to change logging settings: %s',
                    {'log_path': settings['log_path'],
                     'log_console': settings['log_console'],
                     'log_file': settings['log_file']})
        parent.initialize_logging(settings['log_path'], settings['log_console'], settings['log_file'])
        logger.info('Logging settings changed: %s',
                    {'old_log_path': vargs['log_path'],
                     'new_log_path': settings['log_path']})

def clear_logs(vargs, settings, p_get_log_filename=None):
    global parent_get_log_filename

    logs_cleared = False
    
    # if we are not clearing logs - no action here
    if not (vargs.get('clear_logs', False) or settings.get('clear_logs', False)):
        if False:
            logger.warning("REMOVE THIS: %s",
                           {'settings': settings,
                            'msg': 'clear logs not set'})
        return logs_cleared

    # set the function
    if p_get_log_filename:
        parent_get_log_filename = p_get_log_filename

    # make sure we set the get_log_filename
    if not parent_get_log_filename:
        logger.error('must set parent_get_log_filename before calling this function')
        raise Exception

    # print - shutting down logging
    logging.shutdown()

    log_path = str(parent_get_log_filename(vargs.get('log_path', '')))
    if os.path.isfile(log_path):
        # logger.info('Removing cfg_folder vargs log file: ', log_path)
        print('kv_psg:clear_logs:Removing cfg_folder vargs log file: ', log_path)
        os.remove(log_path)
        logs_cleared = True
    log_path = str(parent_get_log_filename(settings.get('log_path', '')))
    if os.path.isfile(log_path):
        # logger.info('Removing cfg_folder settings log file: ', log_path)
        print('kv_psg:clear_logs:Removing cfg_folder settings log file: ', log_path)
        os.remove(log_path)
        logs_cleared = True

    return logs_cleared


def process_change_settings(vargs, settings, v2s, parent, debug=False):
    # capture if we changed and saved data
    settings_file = settings['settings_file']

    # generic change settings option selected
    window = create_settings_window(settings, v2s, parent.__version__)

    while True:
        # bring window to the front
        window.BringToFront()

        # create new window for this
        event, values = window.read()

        # debugging
        
        if debug:
            print(f'event: [{event}]\nvalues: {values}')

        # generic event to exit out
        if event in (sg.WIN_CLOSED, 'Exit'):
            # check to see if the log_path was changed in the screen
            if Path(settings['log_path']) != Path(values['-LOG_PATH-']):
                # post into existing log file
                logger.info('Changing log dir to: %s', values['-LOG_PATH-'])
                # update settings
                old_settings = {'log_path': settings['log_path']}
                settings['log_path'] = values['-LOG_PATH-']
                # update the logging if we changed something
                reinitialize_logging(old_settings, settings, parent)
            break

        if event == 'Save':
            # make sure field is set properly
            if values['-SETTINGS_FILE-'] != settings['settings_file']:
                # the field was changed - lets see if what we have is a valid folder and filename
                if not Path(values['-SETTINGS_FILE-']).parent.is_dir():
                    # the entered parent is not a dir - so we need to skip
                    window['-SETTINGS_FILE-'].update(value=settings['settings_file'])
                    window.Refresh()
                    sg.popup('Improper path to file settings', 'Correct or try using the SaveAs button',
                             'Data not saved')
                    continue

                # valid file capture value and continue on
                settings['settings_file'] = values['-SETTINGS_FILE-']
                # capture the filename from the save as
                settings_file = values['-SETTINGS_FILE-']

            # save screen data to file
            save_settings(settings_file, settings, values, v2s)

            # update the screen
            update_windows_values(window, settings, v2s)

            # update the logging if we changed something
            reinitialize_logging(vargs, settings, parent)

        if event == '-SAVE_AS-':
            # capture the filename from the save as
            settings_file = values['-SAVE_AS-']
            # check the input
            if not settings_file:
                # user cancelled - just get out
                continue

            # get it in the right string structure
            settings_file = str(Path(settings_file))

            if not Path(settings_file).parent.is_dir():
                sg.popup('Selected directory does not exist')
                continue

            settings['settings_file'] = settings_file

            # force the value to change - it may not have been updated on the screen
            values['-SETTINGS_FILE-'] = settings_file

            # and now save out to this file
            save_settings(settings_file, settings, values, v2s)

            # update the screen
            update_windows_values(window, settings, v2s)

            # update the logging if we changed something
            reinitialize_logging(vargs, settings, parent)

        if event == '-LOAD-':
            # capture the filename from the save as
            settings_file = values['-LOAD-']
            # check the input
            if not settings_file:
                # user selected cancel
                continue
            if not os.path.exists(settings_file):
                continue
            # and now read in this data 
            settings = load_settings(settings_file, settings, v2s)
            # set the variable
            settings['settings_file'] = settings_file
            # update the screen
            update_windows_values(window, settings, v2s)

            # update the logging if we changed something
            reinitialize_logging(vargs, settings, parent)

        if event == 'Edit':
            # make sure field is set properly
            if values['-SETTINGS_FILE-'] != settings['settings_file']:
                # the field was changed - lets see if what we have is a valid folder and filename
                if not Path(values['-SETTINGS_FILE-']).parent.is_dir():
                    # the entered parent is not a dir - so we need to skip
                    window['-SETTINGS_FILE-'].update(value=settings['settings_file'])
                    window.Refresh()
                    sg.popup('Improper path to file settings', 'Correct or try using the SaveAs button',
                             'Data not saved')
                    continue

                # valid file capture value and continue on
                settings['settings_file'] = values['-SETTINGS_FILE-']
                # capture the filename from the save as
                settings_file = values['-SETTINGS_FILE-']

            # save screen data to file
            # save_settings(settings_file, settings, values, v2s)
            logger.info('Editting settings in notepad: %s', settings_file)

            # copy the current definitoin of settings in case the edit file can not be loaded
            settings_copy = copy.deepcopy(settings)

            # edit the file we just saved
            open_in_notepad(settings_file)

            # reload the editted file
            try:
                settings = load_settings(settings_file, settings, v2s)
                logger.info('Loaded editted settings file')
            except:
                logger.info('Editted settings file could not be loaded - restoring prior version')
                save_settings(settings_file, settings_copy, values, v2s)

            # update the screen
            update_windows_values(window, settings, v2s)

            # update the logging if we changed something
            reinitialize_logging(settings_copy, settings, parent)

        if event == 'ViewLog':
            global parent_get_log_filename

            # we have not set this - set it
            if parent_get_log_filename is None:
                parent_get_log_filename = parent.get_log_filename
            
            # check for the log file
            try:
                log_path = str(parent_get_log_filename(settings.get('log_path', '')))
            except Exception as e:
                logger.exception('Trying to get log path')
                
            if os.path.isfile(log_path):
                logger.info('User viewed this log file in notepad: %s', log_path)

                # open the file in notepad
                open_in_notepad(log_path)

    window.close()
    return settings, settings_file


# testing
if __name__ == "__main__":
    import ts_maintain as parent
    import os

    vargs = {
        'token': 'token',
        'url': 'url',
        'log_path': '',
        'log_console': False,
        'log_file': True,
    }

    app_folder_path = ["e-share", 'kv_psg']

    # modeled from gui_main routine
    v2s = calc_values_key_2_settings_key(vargs)

    cfg_folder = config_folder(app_folder_path)

    settings_file = os.path.join(config_folder(app_folder_path), 'settings.json')

    settings = load_settings(settings_file, vargs, v2s)

    chg_settings = process_change_settings(vargs, settings, v2s, parent, True)

    print(chg_settings)
