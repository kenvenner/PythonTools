__version__ = '1.03'

import pandas
import os
import copy
from attrdict import AttrDict
import logging

# may comment out in the future
import pprint

pp = pprint.PrettyPrinter(indent=4)

# logging
logger = logging.getLogger(__name__)

# Constants

# Columns output in the ts listing
TS_DUMP_RAW_COLS = ['ts_name',
                    'mount_id', 'share_guid', 'is_owner',
                    'created', 'last_modified', 'expires_at',
                    'category', 'type',
                    'is_single_file', 'is_offline',
                    'active']

DISPLAY_KEY = '-TS_DISPLAY_CHKBOX-'
FILE_KEY = '-TS_DUMP-'


# Generic functions used create/manage trusted share listings

class TSListing(object):
    """
    Object used to get trusted share listing data and generate any required outputs
    """

    def __init__(self, obj_class=None, token=None, url=None, owner_only=False):
        """
        Create the object - based on the object class passed in

        :param obj_class: (object_class) - object class that interacts with CWP, that takes in parameters
                                           (mount, token, url, ts_listing=True)
        :param token: (string) - device token
        :param url: (string) - url to the environment you are interacting with
        :param owner_only: (bool) - when true we only get trusted shares this person is the owner of
        """

        # save values passed in
        self.obj_class = obj_class
        self.token = token
        self.url = url
        self.owner_only = owner_only

        # created by making the call to the appropriate function and filling the element
        self.ts_owner_list = []
        self.ts_collab_list = []
        self.ts_listing_lines = []

        # create the object - with ts_listing set to true
        self.eclient = self.obj_class(None, self.token, self.url, ts_listing=True)

    def ts_listing_steps(self, values):
        """
        Using the values in values - perform the required actions to prepare data

        :param values: (dict) - various settings that drive the update
        """

        # 1 - read in the ts listing data
        self.ts_listing_read()

        # 2 - if we have an output file - then generate the output file
        if values[FILE_KEY]:
            self.ts_listing_dump(values[FILE_KEY])

        # 3 - if we have enabled display output - then generate the console listing
        if values[DISPLAY_KEY]:
            self.ts_listing_for_console()
            logger.info('Close this window to get to the Trusted Share listing')

    def ts_listing_for_console(self):
        """
        Create the strings that are used to display the trusted share listings
        
        :uses self.ts_owner_list:
        :uses self.ts_collab_list:

        :updates self.ts_listing_lines:
        """
        self.ts_listing_lines = []

        # owned shares
        self.ts_listing_lines.append('Trusted Shares you own')
        self.ts_listing_lines.append('{:>10s} | {:50s}'.format('Mount', 'TS Description'))
        self.ts_listing_lines.append('{:>10s} | {:50s}'.format('-' * 10, '-' * 50))
        for rec in self.ts_owner_list:
            self.ts_listing_lines.append('{:>10s} | {:50s}'.format(rec['mount_id'], rec['name']))

        # spacer between sections
        self.ts_listing_lines.append('')

        # recipient shares
        self.ts_listing_lines.append('Trusted Shares you are a recipient of')
        self.ts_listing_lines.append('{:>10s} | {:50s}'.format('Mount', 'TS Description'))
        self.ts_listing_lines.append('{:>10s} | {:50s}'.format('-' * 10, '-' * 50))
        for rec in self.ts_collab_list:
            self.ts_listing_lines.append('{:>10s} | {:50s}'.format(rec['mount_id'], rec['name']))

    def ts_listing_read(self, owner_only=None):
        """
        Read in the ts_listing

        :param owner_only: (bool) - if set, defines if we only extract owner_only
        """

        if owner_only is None:
            owner_only = self.owner_only

        self.ts_owner_list, self.ts_collab_list = self.eclient.ts_listing(owner_only=owner_only)

    def ts_listing_dump(self, ts_dump_filename):
        """
        Write the trusted share information to the filename provided
        
        :param ts_dump_filename: (string) - filename or path/filename to output file created
        """

        # owner
        df1 = pandas.DataFrame(self.ts_owner_list)
        df1.rename(columns={'id': 'share_guid', 'name': 'ts_name'}, inplace=True)
        df1['is_owner'] = True
        df1['expires_at'] = ''

        # recipient
        df2 = pandas.DataFrame(self.ts_collab_list)
        df2.rename(columns={'share_id': 'share_guid', 'name': 'ts_name'}, inplace=True)
        df2['is_owner'] = False

        # merge these two lists
        frames = [df1, df2]
        df = pandas.concat(frames, ignore_index=True)

        # define the output columns
        output_cols = copy.deepcopy(TS_DUMP_RAW_COLS)
        df = df[output_cols]

        df.to_excel(ts_dump_filename, index=False)
        logger.info('Created the trusted share secure view listing file:  %s', ts_dump_filename)
