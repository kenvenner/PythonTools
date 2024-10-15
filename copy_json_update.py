'''
Utility to update the copy_comment configuration file for JIRA ticket processing
'''


import kvutil
import pprint
import os
import sys

# director and file glob for the JIRA ticket xlsx files
excel_dir = '/Users/KenVenner/OneDrive - Hermeus Corp/Documents/2024-10-08-NetSuite-Mgmt/'
excel_filename_glob = 'NS-ERP (Jira) *.xlsx'

# find the filename with the largest/longest filename
excel_full_filename = kvutil.filename_maxmin(excel_dir + excel_filename_glob, reverse=True)
excel_filename = os.path.basename(excel_full_filename)
excel_dir = os.path.dirname(excel_full_filename)

#debugging
print(excel_filename)
print(excel_dir)

# read in the copy_comment configuration file
json_folder = '/Users/KenVenner/OneDrive - Hermeus Corp/Documents/Code/symphony/migration/validation/'
json_full_filename = json_folder + 'copy_jira.json'

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

