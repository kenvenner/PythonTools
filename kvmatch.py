"""
@author:   Ken Venner
@contact:  ken@venerllc.com
@version:  1.10

Library of tools used in finding matches - used by kvcsv and kvxls
"""

# logging
import logging

logger = logging.getLogger(__name__)

# global variables
AppVersion = '1.10'


# this class is used to take a row and data and determine if it matches a minimal requirement

# utility used to create a new consolidate key that is a multi-field key
def build_multifield_key(rowdict, dictkeys, joinchar='|', debug=False):
    # validate we passed in the required keys
    if not dictkeys:
        logger.debug('missing dictkeys')
        raise Exception('dictkeys not provided')
    if debug:
        print('build_multifield_key:dictkeys:', dictkeys)
        print('build_multifield_key:rowdict:', rowdict)
    logger.debug('dictkeys:%s', dictkeys)
    logger.debug('rowdict:%s', rowdict)
    if isinstance(dictkeys, str):
        dictkeys = [dictkeys]
    return joinchar.join([str(rowdict[key]) for key in dictkeys])


# the warning message string for optiondict concerns
def badoption_msg(func, val, val2, fixed=None):
    if fixed is None:
        return '%s:possible mistyped optiondict key [%s] could be [%s]' % (func, val, val2)
    elif fixed:
        return '%s:possible mistyped optiondict key [%s] could be [%s] - this was fixed' % (func, val, val2)
    else:
        return '%s:possible mistyped optiondict key [%s] could be [%s] - this was NOT fixed' % (func, val, val2)


# the utility used to look at an optiondict and look for possibly bad keys passed in
def badoptiondict_check(func, optiondict, badoptiondict, noshowwarning=False, dieonbadoption=False, fix_missing=False):
    '''
    func - str tells us who called this - usercontrolled
    optiondict - list of options to be inspected, warned, terminated or fixed
    badoptiondict - known list of bad keyss mapped to the proper key
    noshowwarning - when true we do not display print statements about issues 
    dieonbadoption - when true - if we have a badoption key die 
    fix_missing - when true fix this key if the proper key does ot already exist
    '''
    
    # check optiondict for unexpected/mistyped values and provide warnings
    warnings = []
    if False:
        print('optiondict')
        print(optiondict)
        print('badoptiondict')
        print(badoptiondict)
        print(dieonbadoption, noshowwarning, fix_missing)
    for val in badoptiondict:
        # for each bad entry
        if val in optiondict:
            # do we have it - we do
            fixed=None
            if fix_missing:
                # if we fix it check to see if the right value is already set
                fixed=False
                if badoptiondict[val] not in optiondict:
                    optiondict[badoptiondict[val]] = optiondict[val]
                    fixed=True
            # fixed or not create the warning
            warnings.append(badoption_msg(func, val, badoptiondict[val], fixed=fixed))
            # display directly is appropriate
            if not noshowwarning: print(warnings[-1])

    # check to see if we should raise an error if we find problems
    if dieonbadoption and warnings:
        raise Exception('badoption found')

    # now return the warnings
    return warnings


# this is the object that is persistent and is used to find a matching record to the defined constraints of the __init__
class MatchRow(object):
    '''
    req_cols - list of columns in the dictionary
    xlat_dict - dict when populated, that changes the key of a column to a newkey
    optiondict - setting vaues level 1
    optiondict2 - setting values level 2 takes precidensce over level 1

    option keys:
    dieonbadoption - bool - when true - we will die if we receive invalid options
    nocase - bool - if true - we check for key match case insensitive
    max_rows - integer - max number of rows to check
    unique_column - bool - if true - we must have unqiue columns in the final result
    no_warnings - bool - when true - we do not display warnings but pass them back as an array
    fix_missing - bool - when true - when a bad option is found we will attempt to fix them

    '''

    # set up the parser with input information
    def __init__(self, req_cols, xlatdict={}, optiondict={}, optiondict2={}, debug=False):
        # validate input types
        if req_cols and not isinstance(req_cols, list):
            raise Exception(u'req_cols must be a list: {}'.format(req_cols))
        if xlatdict and not isinstance(xlatdict, dict):
            raise Exception(u'xlatdict must be a dict: {}'.format(req_cols))
        if optiondict and not isinstance(optiondict, dict):
            raise Exception(u'optiondict must be a dict: {}'.format(req_cols))
        if optiondict2 and not isinstance(optiondict2, dict):
            raise Exception(u'optiondict2 must be a dict: {}'.format(req_cols))

        # setup variables
        self._req_cols = req_cols[:]  # make sure we have a copy of this so it does not get changed on us
        self._xlatdict = {}  # xref dictionary with passed and (if nocase - lower case keys)
        self._xlatdict_lower = {}  # xref dictionary for lower case key and lower case value

        self._header_row = []  # NOT USED
        self._near_match_count = {}  # NOT USED

        self._match_count = {}  # dictionary of the column names we are looking for - with a count of matches in data
        self._match_columns = 0  # count of columns we have matched

        self.search_failed = False  # if true - we did not succeed in the search
        self.search_exceeded = False  # if true - we exceeded the number of rows to check
        self.error_msg = ''  # if search_failed - this is populated with a string describing why the search failed
        self.warning_msg = []  # list of warning messages

        self.rowcount = 0  # counts the number of rows processed

        # results from this routine
        # self._data # the array that was found as the matching array (original header)
        # self._data_mapped # the array that was remapped using xlatdict and had blank entries converted (desired header)

        # optiondict values passed in
        self.nocase = False  # if true - we check for key match case insensitive
        self.unique_column = False  # if true - we must have unqiue columns in the final result
        self.max_rows = 10  # max number of rows to check
        self.no_warnings = False  # if true - we supress sending out warning message
        self.dieonbadoption = False  # if true - we raise error on bad options
        self.fix_missing = False # if true - we fix, if None display no msg


        # create the list of misconfigured solutions
        badoptiondict = {
            'diebadoption': 'dieonbadoption',
            'die_badoption': 'dieonbadoption',
            'die_onbadoption': 'dieonbadoption',
            'no_case': 'nocase',
            'maxrow': 'max_rows',
            'maxrows': 'max_rows',
            'max_row': 'max_rows',
            'uniquecolumn': 'unique_column',
            'uniquecolumns': 'unique_column',
            'unique_columns': 'unique_column',
            'nowarning': 'no_warnings',
            'nowarnings': 'no_warnings',
            'no_warning': 'no_warnings',
            'noshowwarning': 'no_warnings',
            'noshowwarnings': 'no_warnings',
            'fixmissing': 'fix_missing',
        }

        optiondict3 = {}
        for fld in ['nocase','unique_column','max_rows','no_warnings','dieonbadoption','fix_missing']:
            if fld in optiondict2:
                optiondict3[fld] = optiondict2[fld]
            elif fld in optiondict:
                optiondict3[fld] = optiondict[fld]
        # values from badoptiondict
        for fld, v in badoptiondict.items():
            if v not in optiondict3 and fld in optiondict2:
                optiondict3[v] = optiondict2[fld]
            elif v not in optiondict3 and fld in optiondict:
                optiondict3[v] = optiondict[fld]


        # debugging
        if debug:
            print('kvmatch.MatchRow:init:optiondict3:')
            for k,v in optiondict3.items():
                print(k,v)


        # update flag/setting if options is set
        if 'nocase' in optiondict3:
            self.nocase = optiondict3['nocase']
        if 'unique_column' in optiondict3:
            self.unique_column = optiondict3['unique_column']
        if 'max_rows' in optiondict3:
            self.max_rows = optiondict3['max_rows']
        if 'no_warnings' in optiondict3:
            self.no_warnings = optiondict3['no_warnings']
        if 'dieonbadoption' in optiondict3:
            self.dieonbadoption = optiondict3['dieonbadoption']
        if 'fix_missing' in optiondict3:
            self.fix_missing = optiondict3['fix_missing']

        # check what got passed in
        self.warning_msg = badoptiondict_check('kvmatch:MatchRow:__init__', optiondict, badoptiondict, self.no_warnings,
                                               self.dieonbadoption, self.fix_missing)

        # copy over the translations dictionary and add values if required
        for key in xlatdict:
            if self.nocase:
                # if the nocase option is enabled - then create lower case key and result for lookup
                self._xlatdict_lower[key.lower()] = xlatdict[key].lower()
                # add the lower case key to the _xlatdict
                self._xlatdict[key.lower()] = xlatdict[key]
            else:
                # copy into local copy the dictionary
                self._xlatdict[key] = xlatdict[key]

    # clear values to prep for a new run through the data
    def reset(self):
        self.setupForMatch()
        self._near_match_count = {}

        self.rowcount = 0
        self._data = []
        self._data_mapped = []
        self.search_failed = False
        self.search_exceed = False
        self.error_msg = ''

    # clear values to support a new run to look for a match
    def setupForMatch(self):
        self._header_row = []
        self._match_columns = 0
        self._match_count = {}
        for col in self._req_cols:
            if self.nocase:
                self._match_count[col.lower()] = 0
            else:
                self._match_count[col] = 0

    # this routine takes data and create the remapped list
    def remappedRow(self, data, debug=False):
        blankfmt = 'blank%03d'
        blankcount = 1

        remapped = []
        # step through and convert it appropriate
        for val in data:
            if not val:
                # no value specified - create the field name using string formatting

                # debugging
                if debug: print('not val:', blankfmt % blankcount)
                logger.debug('not val:%s', blankfmt % blankcount)
                # no value in this field - create a new value and save
                remapped.append(blankfmt % blankcount)
                # increment the counter
                blankcount += 1
            elif val in self._xlatdict:
                # this field converts directly based on information in xlatdict

                # debugging
                if debug: print('xlatdict:val:', val, ':xladict:', self._xlatdict[val])
                logger.debug('xlatdict:val:%s:xladict:%s', val, self._xlatdict[val])
                # coverts directly
                remapped.append(self._xlatdict[val])
            elif self.nocase and val.lower() in self._xlatdict_lower:
                # the lower case version of this field translates to the lowercase version directly

                # debugging
                if debug: print('nocase:xlatdict:val:', val, ':xladict_lower:', self._xlatdict_lower[val.lower()])
                logger.debug('nocase:xlatdict:val:%s:xladict_lower:%s', val, self._xlatdict_lower[val.lower()])
                # lower case value converts - but use the _xlatdict - because that points to the proper result
                # the xlatdict_lower has lower case key and lower case result
                remapped.append(self._xlatdict[val.lower()])
            else:
                # debugging
                if debug: print('val:', val)
                logger.debug('val:%s', val)
                # just take the value we got
                remapped.append(val)

        # return what we found
        return remapped

    # validate the data is unique values - if not pass back the values that are duplicated
    def _unique_values(self, data, debug=False):
        # dictionary to count number of times we have seen a value
        seen_val = {}
        # capture values that have duplicates
        duplicate_val = []

        # debugging
        if debug:
            print('_unique_values:data:', data)
        logger.debug('data:%s', data)

        # step through the list of values provided
        for val in data:
            if val in seen_val:
                # increment the count - we have seen this again
                seen_val[val] += 1
                if seen_val[val] == 2:
                    # we saw this twice - message - if we see it more - we already communicated
                    duplicate_val.append(val)
            else:
                # first time seen
                seen_val[val] = 1

        # return the array of duplidate values
        return duplicate_val

    # pass back True if this row matches the requirements
    def matchRowList(self, data, debug=False):
        # increment the row counter
        self.rowcount += 1

        # debugging
        if debug:
            print('xlatdict:', self._xlatdict)
            print('req_cols:', self._req_cols)
            print('data:', data)
            print('rowcount:', self.rowcount)
            print('max_rows:', self.max_rows)
            print('nocase:', self.nocase)

        logger.debug('xlatdict:%s', self._xlatdict)
        logger.debug('req_cols:%s', self._req_cols)
        logger.debug('data:%s', data)
        logger.debug('rowcount:%s', self.rowcount)
        logger.debug('nocase:%s', self.nocase)

        # some upfront tests
        if self.rowcount > self.max_rows:
            if debug:  print('rowcount > max_rows - set variables and return None')
            logger.debug('rowcount > max_rows - set variables and return None')
            self.search_failed = True
            self.search_exceeded = True
            self.error_msg = 'Max search row count [%s] exceeded at row [%s]' % (self.max_rows, self.rowcount)
            return None

        # initialize what we need to match on
        self.setupForMatch()

        # step through the elements in this list
        for val in data:
            # if this is blank get next value - no work to do here
            if not val:
                if debug: print('skip val as blank')
                logger.debug('skip val as blank')
                continue

            # if we are nocase and this is a string - we want to be lower case
            if self.nocase and isinstance(val, str):
                val = val.lower()
                if debug: print('convert to lower case:', val)
                logger.debug('convert to lower case:%s', val)

            # << might add back in the converstion of \r or \r\n to \n

            # << might add back in the rtrim feature here as a flag

            # check to see if this value matches something we are looking for

            # check to see that this value matches one we are looking for
            if val in self._match_count:
                # this value/column is a match to a required column so capture this fact
                self._match_count[val] += 1
                self._header_row.append(val)
                # debugging
                if debug: print('increment match_count for val:', val)
                logger.debug('increment match_count for val:%s', val)
            elif val in self._xlatdict and self._xlatdict[val] in self._match_count:
                self._match_count[self._xlatdict[val]] += 1
                # debugging
                if debug: print('increment match_count for val:', val, ':xlatdict[val]:', self._xlatdict[val])
            elif val in self._xlatdict_lower and self._xlatdict_lower[val] in self._match_count:
                self._match_count[self._xlatdict_lower[val]] += 1
                # debugging
                if debug: print('increment match_count for val:', val, ':xlatdict_lower[val]:',
                                self._xlatdict_lower[val])
                logger.debug('increment match_count for val:%s:xlatdict_lower[val]:%s', val, self._xlatdict_lower[val])
            else:
                # debugging
                logger.debug('no match val:%s', val)
                if debug:
                    print('no match val:', val)
                    if val in self._xlatdict:
                        print('nomatch:xlatdict[val]:', self._xlatdict[val])
                    elif val in self._xlatdict_lower:
                        print('nomatch:xlatdict_lower[val]:', self._xlatdict_lower[val])

        # debugging
        if debug:  print('_match_count:', self._match_count)
        logger.debug('_match_count:%s', self._match_count)

        # count the number of column matches we got
        for col in self._req_cols:
            if self.nocase and self._match_count[col.lower()]:
                self._match_columns += 1
                if debug:  print('increment on col.lower:', col, ':match_columns:', self._match_columns)
                logger.debug('increment on col.lower:%s:match_columns:%s', col, self._match_columns)
            elif not self.nocase and self._match_count[col]:
                self._match_columns += 1
                if debug:  print('increment on col:', col, ':match_columns:', self._match_columns)
                logger.debug('increment on col:%s:match_columns:%s', col, self._match_columns)

        # debugging
        if debug: print('match_columns:', self._match_columns)
        if debug: print('len(req_cols):', len(self._req_cols))
        logger.debug('match_columns:%s', self._match_columns)
        logger.debug('len(req_cols):%d', len(self._req_cols))

        # now check if the count is the same
        if self._match_columns == len(self._req_cols):
            # save the record that was a match
            self._data = data
            # save the mapped record
            self._data_mapped = self.remappedRow(data)

            # final test - check to see if we required unique columns
            if self.unique_column:
                duplicate_col = self._unique_values(self._data_mapped, debug=debug)

                # now test to see if we have duplicates
                if duplicate_col:
                    self.search_failed = True
                    self.error_msg = 'Row found with duplicate column headers:' + ','.join(duplicate_col)
                    return None

            # return true
            return True
        elif self.rowcount == self.max_rows:
            if debug:  print('rowcount == max_rows - match not found, set variables and return None')
            logger.debug('rowcount == max_rows - match not found, set variables and return None')
            self.search_failed = True
            self.search_exceeded = True
            self.error_msg = 'Max search row count [%s] exceeded at row [%s] - no match found' % (self.max_rows, self.rowcount)
            return False


# eof
