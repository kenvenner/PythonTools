'''
Utility to update the copy_comment configuration file for JIRA ticket processing
'''


import kvutil
import pprint
import os
import sys

# --------------------------------------------------------------------------------


# COMMAND LINE PROCESSING

optiondictconfig = {
    'AppVersion' : {
        'value' : '1.01',
    },
    'debug' : {
        'value' : False,
        'type' : 'bool',
    },
    'excel_dir': {
        'value': '/Users/KenVenner/OneDrive - Hermeus Corp/Documents/2024-10-08-NetSuite-Mgmt/',
        'type':  'dir',
    },
    'excel_filename_glob': {
        'value': 'NS-ERP (Jira) *0.xlsx',
    },
    'json_folder': {
        'value': '/Users/KenVenner/OneDrive - Hermeus Corp/Documents/Code/symphony/migration/validation/',
        'type':  'dir',
    },
    'json_filename': {
        'value': 'copy_jira.json',
    },
}

optiondict = kvutil.kv_parse_command_line( optiondictconfig ) # , keymapdict=keymapdict )

# update directories
for k, v in optiondictconfig.items():
    # assure directories are set up correctly
    if 'type' in v and v['type'] == 'dir':
        if not optiondict[k]:
            optiondict[k] = ''
        elif optiondict[k][-1] != '/':
            optiondict[k] += '/'
            



# --------------------------------------------------------------------------------



# directory and file glob for the JIRA ticket xlsx files
excel_dir = '/Users/KenVenner/OneDrive - Hermeus Corp/Documents/2024-10-08-NetSuite-Mgmt/'
excel_filename_glob = 'NS-ERP (Jira) *0.xlsx'

excel_dir = optiondict['excel_dir']
excel_filename_glob = optiondict['excel_filename_glob']


# find the filename with the largest/longest filename
excel_full_filename = kvutil.filename_maxmin(excel_dir + excel_filename_glob, reverse=True)
if not excel_full_filename:
    print('No files found: ', excel_dir+excel_filename_glob)
    sys.exit(1)
excel_filename = os.path.basename(excel_full_filename)
excel_dir = os.path.dirname(excel_full_filename)

#debugging
print(excel_filename)
print(excel_dir)

# read in the copy_comment configuration file
json_folder = '/Users/KenVenner/OneDrive - Hermeus Corp/Documents/Code/symphony/migration/validation/'
json_full_filename = json_folder + 'copy_jira.json'

json_folder = optiondict['json_folder']
json_full_filename = json_folder + optiondict['json_filename']


# read in the current configuration
conf_json = kvutil.load_json_file_to_dict(json_full_filename)

# check to see if we have a new file
if excel_filename in [conf_json['dst_fname'], conf_json['out_fname']]:
    # no new file exit with message
    print('No updates')
    sys.exit()
elif(True):
    # we have a new file - message
    print('-'*40)
    print(conf_json['dst_fname'])
    print(conf_json['out_fname'])
    print(excel_filename)


# debugging - show the bvefore conf
print('BEFORE CHANGE:')
pprint.pprint(conf_json)

# update settings in the conf
conf_json['src_fname'] = conf_json['out_fname']
conf_json['dst_fname'] = excel_filename
conf_json['out_fname'] = excel_filename.split('.')[0]+'_map.xlsx'

# debuggin show the after conf
print('AFTER CHANGE:')
pprint.pprint(conf_json)

# save hte conf back
kvutil.dump_dict_to_json_file(json_full_filename, conf_json)

#eof

