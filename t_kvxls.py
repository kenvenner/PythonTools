import kvxls
import kvutil
import unittest
import datetime

import os

xlsfloat2datetime = [ 43080.0,  datetime.datetime.strptime('12/11/2017', '%m/%d/%Y') ]

# filename = kvutil.filename_unique( { 'base_filename' : 't_kvcsvtest', 'file_ext' : '.xls', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )

records = [
    {'Company': 'NHLiq', 'Wine': 'Caravan Cabernet Sauvignon', 'Vintage_Wine': 'Caravan Cabernet Sauvignon 2014', 'Vintage': '2014', 'Date': '12/11/2017', 'Type': 'red-cab', 'LastSeen': 'Never'} ,
    {'Company': 'BevMo', 'Wine': 'Caymus Cabernet Sauvignon Napa (750 ML)', 'Vintage_Wine': 'Caymus Cabernet Sauvignon Napa (750 ML) 2014', 'Vintage': '2014', 'Date': '10/31/2015', 'Type': 'red-cab', 'LastSeen': 'Never'} ,
    {'Company': 'BevMo', 'Wine': 'Caymus Cabernet Sauvignon Special Select (750 ML)', 'Vintage_Wine': 'Caymus Cabernet Sauvignon Special Select (750 ML) 2014', 'Vintage': '2014', 'Date': '10/16/2016', 'Type': 'red-cab', 'LastSeen': 'Never'} ,
    {'Company': 'BevMo', 'Wine': 'Caymus Cabernet Special Select (750 ML)', 'Vintage_Wine': 'Caymus Cabernet Special Select (750 ML) 2014', 'Vintage': '2014', 'Date': '7/23/2015', 'Type': 'red-cab', 'LastSeen': 'Never'} ,
    {'Company': 'WineClub', 'Wine': 'CAYMUS VINEYARDS CABERNET SAUVIGNON', 'Vintage_Wine': 'CAYMUS VINEYARDS CABERNET SAUVIGNON 2014', 'Vintage': '2014', 'Date': '7/15/2018', 'Type': 'red-cab', 'LastSeen': 'Never'} ,
    {'Company': 'WineClub', 'Wine': 'CAYMUS VINEYARDS SPECIAL SELECTION CABERNET SAUVIGNON', 'Vintage_Wine': 'CAYMUS VINEYARDS SPECIAL SELECTION CABERNET SAUVIGNON 2014', 'Vintage': '2014', 'Date': '7/15/2018', 'Type': 'red-cab', 'LastSeen': 'Never'} ,
    {'Company': 'BevMo', 'Wine': 'Chappellet Cab Sauv Pritchard (750 ML)', 'Vintage_Wine': 'Chappellet Cab Sauv Pritchard (750 ML) 2014', 'Vintage': '2014', 'Date': '12/31/2015', 'Type': 'red-cab', 'LastSeen': 'Never'} ,
    {'Company': 'TotalCA', 'Wine': 'Chappellet Cabernet Sauvignon Napa Signature', 'Vintage_Wine': 'Chappellet Cabernet Sauvignon Napa Signature 2014', 'Vintage': '2014', 'Date': '7/2/2013', 'Type': 'red-cab', 'LastSeen': '2/27/2016'} ,
    {'Company': 'WineClub', 'Wine': 'CHAPPELLET PRITCHARD HILL CABERNET SAUVIGNON', 'Vintage_Wine': 'CHAPPELLET PRITCHARD HILL CABERNET SAUVIGNON 2014', 'Vintage': '2014', 'Date': '7/15/2018', 'Type': 'red-cab', 'LastSeen': 'Never'} ,
    {'Company': 'WineClub', 'Wine': 'CHAPPELLET SIGNATURE RESERVE CABERNET SAUVIGNON', 'Vintage_Wine': 'CHAPPELLET SIGNATURE RESERVE CABERNET SAUVIGNON 2014', 'Vintage': '2014', 'Date': '7/15/2018', 'Type': 'red-cab', 'LastSeen': 'Never'} ,
    {'Company': 'Vons', 'Wine': 'Charles Krug Cabernet Sauvignon Wine - 750 Ml', 'Vintage_Wine': 'Charles Krug Cabernet Sauvignon Wine 2014 - 750 Ml', 'Vintage': '2014', 'Date': '2/21/2009', 'Type': 'red-cab', 'LastSeen': '2/27/2016'} ,
]

req_cols = ['Company', 'Wine']

class TestKVxls(unittest.TestCase):
    def test_xldate_to_datetime_p01_simple(self):
        self.assertEqual(kvxls.xldate_to_datetime(xlsfloat2datetime[0]), xlsfloat2datetime[1])

    # XLS file processing
    def test_readxlslist_findheader_p01_xls_simple(self):
        filename = 't_kvxlstest01.xls'
        result = kvxls.readxls2list_findheader( filename, req_cols, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # convert to date.time if XLS - already set if XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
        self.assertEqual( len(result), len(records) )
    def test_readxlslist_findheader_p02_xls_simple_aref(self):
        filename = 't_kvxlstest01.xls'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'aref_result' : True}, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = list(records[0].values())
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec[3] = float(temprec[3])
        temprec[4] =  datetime.datetime.strptime(temprec[4], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # convert to date.time if XLS - already set if XLSX
            result[0][4] = kvxls.xldate_to_datetime(result[0][4])
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p03_xls_simple_col_header(self):
        filename = 't_kvxlstest01.xls'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'col_header' : True}, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # update the xl date field to be datetime - if xls - already done if xlsx
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p04_xls_simple_no_header_start_row_return_aref(self):
        filename = 't_kvxlstest01.xls'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = list(records[0].values())
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec[3] = float(temprec[3])
        temprec[4] =  datetime.datetime.strptime(temprec[4], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # update to date.time if XLS not XLSX
            result[0][4] = kvxls.xldate_to_datetime(result[0][4])
        #print('temprec2:', temprec)
        #print('result[0]:', result[0])
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p05_xls_simple_no_header_start_row_col_aref(self):
        filename = 't_kvxlstest01.xls'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # update to date.time if XLS not XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p06_xls_simple_no_header_start_row_col_aref_missing_cols(self):
        filename = 't_kvxlstest01.xls'
        col_aref = list(records[0].keys())
        col_aref = col_aref[:-2]
        #print('col_aref:', col_aref)
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # update to date.time if XLS not XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        #print('temprec2:', temprec)
        #print('result[0]:', result[0])
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p07_xls_simple_col_header_col_aref_missing_cols(self):
        filename = 't_kvxlstest01.xls'
        col_aref = list(records[0].keys())
        col_aref = col_aref[:-2]
        #print('col_aref:', col_aref)
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # update to date.time if XLS not XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        #print('temprec2:', temprec)
        #print('result[0]:', result[0])
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p08_xls_convert_dateflds(self):
        filename = 't_kvxlstest01.xls'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={ 'dateflds' : ['Date']}, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p09_xls_save_row(self):
        filename = 't_kvxlstest01.xls'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxlslist_findheader_p10_xls_blank_column(self):
        filename = 't_kvxlstest02.xls'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={ 'save_row': True }, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxlslist_findheader_p11_xls_starting_blank_lines(self):
        filename = 't_kvxlstest02.xls'
        result = kvxls.readxls2list_findheader( filename, req_cols, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        temprec['blank001'] = ''
        if filename.endswith('.xls'):
            # we compare to blank string in XLS vs None in XLSX
            temprec['blank001'] = ''
            # update to date.time if XLS not XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        else:
            # we compare to blank string in XLS vs None in XLSX
            temprec['blank001'] = None
        #print('temprec2:', temprec)
        #print('result[0]:', result[0])
        self.assertEqual(result[0], temprec)

    def test_readxlslist_findheader_f01_exceed_rows(self):
        with self.assertRaises(Exception) as context:
            filename = 't_kvxlstest02.xls'
            kvxls.readxls2list_findheader( filename, req_cols, optiondict={'maxrows' : 2}, debug=False )
    def test_readxlslist_findheader_f02_unique_columns_test(self):
        with self.assertRaises(Exception) as context:
            filename = 't_kvxlstest03.xls'
            kvxls.readxls2list_findheader( filename, req_cols, optiondict={'unique_column' : True}, debug=False )

        
    # XLSX file processing
    #   1) copy the XLS tests
    #   2) change the filename to have a .xlsx ending
    #   3) chnage the _xls_ to be _xlsx_
    def test_readxlslist_findheader_p01_xlsx_simple(self):
        filename = 't_kvxlstest01.xlsx'
        result = kvxls.readxls2list_findheader( filename, req_cols, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # convert to date.time if XLS - already set if XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
        self.assertEqual( len(result), len(records) )
    def test_readxlslist_findheader_p02_xlsx_simple_aref(self):
        filename = 't_kvxlstest01.xlsx'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'aref_result' : True}, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = list(records[0].values())
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec[3] = float(temprec[3])
        temprec[4] =  datetime.datetime.strptime(temprec[4], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # convert to date.time if XLS - already set if XLSX
            result[0][4] = kvxls.xldate_to_datetime(result[0][4]) 
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p03_xlsx_simple_col_header(self):
        filename = 't_kvxlstest01.xlsx'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'col_header' : True}, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        if filename.endswith('.xls'):
            # update the xl date field to be datetime - if xls - already done if xlsx
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p04_xlsx_simple_no_header_start_row_return_aref(self):
        filename = 't_kvxlstest01.xlsx'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = list(records[0].values())
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec[3] = float(temprec[3])
        temprec[4] =  datetime.datetime.strptime(temprec[4], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # update to date.time if XLS not XLSX
            result[0][4] = kvxls.xldate_to_datetime(result[0][4])
        #print('temprec2:', temprec)
        #print('result[0]:', result[0])
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p05_xlsx_simple_no_header_start_row_col_aref(self):
        filename = 't_kvxlstest01.xlsx'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # update to date.time if XLS not XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p06_xlsx_simple_no_header_start_row_col_aref_missing_cols(self):
        filename = 't_kvxlstest01.xlsx'
        col_aref = list(records[0].keys())
        col_aref = col_aref[:-2]
        #print('col_aref:', col_aref)
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # update to date.time if XLS not XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        #print('temprec2:', temprec)
        #print('result[0]:', result[0])
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p07_xlsx_simple_col_header_col_aref_missing_cols(self):
        filename = 't_kvxlstest01.xlsx'
        col_aref = list(records[0].keys())
        col_aref = col_aref[:-2]
        #print('col_aref:', col_aref)
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        # update memory to match field types read from xls
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        # update the xl date field to be datetime
        if filename.endswith('.xls'):
            # update to date.time if XLS not XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        #print('temprec2:', temprec)
        #print('result[0]:', result[0])
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p08_xlsx_convert_dateflds(self):
        filename = 't_kvxlstest01.xlsx'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={ 'dateflds' : ['Date']}, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        #print('temprec2:', temprec)
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p09_xlsx_save_row(self):
        filename = 't_kvxlstest01.xlsx'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxlslist_findheader_p10_xlsx_blank_column(self):
        filename = 't_kvxlstest02.xlsx'
        result = kvxls.readxls2list_findheader( filename, req_cols, optiondict={ 'save_row': True }, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxlslist_findheader_p11_xlsx_starting_blank_lines(self):
        filename = 't_kvxlstest02.xlsx'
        result = kvxls.readxls2list_findheader( filename, req_cols, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        #print('temprec1:', temprec)
        temprec['Vintage'] = float(temprec['Vintage'])
        temprec['Date'] =  datetime.datetime.strptime(temprec['Date'], '%m/%d/%Y')
        if filename.endswith('.xls'):
            # we compare to blank string in XLS vs None in XLSX
            temprec['blank001'] = ''
            # update to date.time if XLS not XLSX
            result[0]['Date'] = kvxls.xldate_to_datetime(result[0]['Date'])
        else:
            # we compare to blank string in XLS vs None in XLSX
            temprec['blank001'] = None
        #print('temprec2:', temprec)
        #print('result[0]:', result[0])
        self.assertEqual(result[0], temprec)

    def test_readxlslist_findheader_f01_xlsx_exceed_rows(self):
        with self.assertRaises(Exception) as context:
            filename = 't_kvxlstest02.xlsx'
            kvxls.readxls2list_findheader( filename, req_cols, optiondict={'maxrows' : 2}, debug=False )
    def test_readxlslist_findheader_f02_xlsx_unique_columns_test(self):
        with self.assertRaises(Exception) as context:
            filename = 't_kvxlstest03.xlsx'
            kvxls.readxls2list_findheader( filename, req_cols, optiondict={'unique_column' : True}, debug=False )


if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        pass
        #        if os.path.exists(filename): os. remove(filename)
        # print(filename)
