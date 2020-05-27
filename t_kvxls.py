import kvxls
import kvutil
import unittest
import datetime

import os

# logging
import kvlogger
config=kvlogger.get_config('t_kvxls.log')
kvlogger.dictConfig(config)
logger=kvlogger.getLogger(__name__)

# set up filenames
filenamexls = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest', 'file_ext' : '.xls', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )
filenamexlsx = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest', 'file_ext' : '.xlsx', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )

filenamexls2 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest2', 'file_ext' : '.xls', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )
filenamexlsx2 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest2', 'file_ext' : '.xlsx', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )

filenamexls3 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest3', 'file_ext' : '.xls', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )
filenamexlsx3 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest3', 'file_ext' : '.xlsx', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )




xlsfloat2datetime = [ 43080.0,  datetime.datetime.strptime('12/11/2017', '%m/%d/%Y') ]

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

records2 = [
    {'StringField': 'this is a string line 1', 'DateField': datetime.datetime(2020, 1, 1, 0, 0), 'IntField': 1, 'NumberField': 12.34},
    {'StringField': 'this is line 2', 'DateField': datetime.datetime(2020, 2, 2, 0, 0), 'IntField': 10, 'NumberField': 1234.56}
]

req_cols = ['Company', 'Wine']
req_cols2 = ['StringField', 'DateField']

class TestKVxls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.debug('SETUP===============================')
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        # create xls file
        kvxls.writelist2xls( filenamexls, records )
        # create xlsx file
        kvxls.writelist2xls( filenamexlsx, records )
        # create xls file
        kvxls.writelist2xls( filenamexls2, records2 )
        # create xlsx file
        kvxls.writelist2xls( filenamexlsx2, records2 )

    @classmethod
    def tearDownClass(cls):
        if 1:
            kvutil.remove_filename( filenamexls, kvutil.functionName() )
            kvutil.remove_filename( filenamexlsx, kvutil.functionName() )
            kvutil.remove_filename( filenamexls2, kvutil.functionName() )
            kvutil.remove_filename( filenamexlsx2, kvutil.functionName() )

                        
    def test_xldate_to_datetime_p01_simple(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        self.assertEqual(kvxls.xldate_to_datetime(xlsfloat2datetime[0]), xlsfloat2datetime[1])

    # XLS file processing - simple req_cols
    def test_readxlslist_findheader_p01_xls_simple_reqcols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readxlslist_findheader_p02_xls_simple_reqcols_aref_result(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxlslist_findheader_p03_xls_simple_reqcols_col_header(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'col_header' : True}, debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxlslist_findheader_p04_xls_simple_reqcols_no_header_start_row_return_aref(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxlslist_findheader_p05_xls_simple_reqcols_no_header_start_row_col_aref(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxlslist_findheader_p06_xls_simple_reqcols_no_header_start_row_col_aref_missing_cols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p07_xls_simple_reqcols_col_aref_blank_column(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={ 'save_row': True }, col_aref=col_aref, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxlslist_findheader_p08_xls_simple_reqcols_col_header_col_aref_missing_cols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p09_xls_simple_reqcols_convert_dateflds(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        result = kvxls.readxls2list_findheader( filenamexls2, req_cols2, optiondict={ 'dateflds' : ['DateField']}, debug=False )
        self.assertEqual(result[0], records2[0])
    def test_readxlslist_findheader_p10_xls_simple_reqcols_save_row(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxlslist_findheader_p11_xls_simple_reqcols_aref_result_starting_blank_lines(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'aref_result' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )
    def test_readxlslist_findheader_p12_xls_simple_reqcol_no_header_starting_blank_lines(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'no_header' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'no_header' : True}, debug=False )
        self.assertEqual(result[0], ['', '', '', '', '', '', ''])
        self.assertEqual(result[6], list(records[0].keys()))
        self.assertEqual(result[7], list(records[0].values()))
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )


        
    # XLS file processing - simple blank req_cols
    def test_readxlslist_findheader_p01_xls_simple_blankReqCols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        result = kvxls.readxls2list_findheader( filenamexls, [], debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readxlslist_findheader_p02_xls_simple_blankReqCols_aref_result(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName())
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxlslist_findheader_p03_xls_simple_blankReqCols_col_header(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'col_header' : True}, debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxlslist_findheader_p04_xls_simple_blankReqCols_no_header_start_row_return_aref(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxlslist_findheader_p05_xls_simple_blankReqCols_no_header_start_row_col_aref(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxlslist_findheader_p06_xls_simple_blankReqCols_no_header_start_row_col_aref_missing_cols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p07_xls_simple_blankReqCols_col_aref_blank_column(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={ 'save_row': True }, col_aref=col_aref, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxlslist_findheader_p08_xls_simple_blankReqCols_col_header_col_aref_missing_cols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p09_xls_simple_blankReqCols_convert_dateflds(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls2, [], optiondict={ 'dateflds' : ['DateField']}, debug=False )
        self.assertEqual(result[0], records2[0])
    def test_readxlslist_findheader_p10_xls_simple_blankReqCols_save_row(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxlslist_findheader_p11_xls_simple_blankReqCols_aref_result_starting_blank_lines(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'aref_result' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, [], optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], ['', '', '', '', '', '', ''])
        self.assertEqual(result[6], list(records[0].values()))
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )
    def test_readxlslist_findheader_p12_xls_simple_blankReqCols_no_header_starting_blank_lines(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'no_header' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, [], optiondict={'no_header' : True}, debug=False )
        self.assertEqual(result[0], ['', '', '', '', '', '', ''])
        self.assertEqual(result[6], list(records[0].keys()))
        self.assertEqual(result[7], list(records[0].values()))
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )


        
    def test_readxlslist_findheader_f01_xls_simple_maxrows_exceeded_in_header_search(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'no_header' : True}, debug=False )
        with self.assertRaises(Exception) as context:
            kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'maxrows' : 2}, debug=False )
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )
    def test_readxlslist_findheader_f02_xls_simple_unique_columns_test(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        header = list(records[0].keys())
        dupkey = header[0]
        header.append(dupkey)
        aref = []
        for rec in records:
            aref.append(list(rec.values())+[rec[dupkey]])
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'aref_result' : True}, debug=False )
        with self.assertRaises(Exception) as context:
            kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'unique_column' : True}, debug=False )
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )

        
    # XLSX file processing
    def test_readxlslist_findheader_p01_xlsx_simple_reqcols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readxlslist_findheader_p02_xlsx_simple_reqcols_aref_result(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxlslist_findheader_p03_xlsx_simple_reqcols_col_header(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'col_header' : True}, debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxlslist_findheader_p04_xlsx_simple_reqcols_no_header_start_row_return_aref(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxlslist_findheader_p05_xlsx_simple_reqcols_no_header_start_row_col_aref(self):
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxlslist_findheader_p06_xlsx_simple_reqcols_no_header_start_row_col_aref_missing_cols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p07_xlsx_simple_reqcols_col_aref_blank_column(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={ 'save_row': True }, col_aref=col_aref, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxlslist_findheader_p08_xlsx_simple_reqcols_col_header_col_aref_missing_cols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p09_xlsx_simple_reqcols_convert_dateflds(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexls2, req_cols2, optiondict={ 'dateflds' : ['DateField']}, debug=False )
        self.assertEqual(result[0], records2[0])
    def test_readxlslist_findheader_p10_xlsx_simple_reqcols_save_row(self):
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxlslist_findheader_p11_xlsx_simple_reqcols_aref_result_starting_blank_lines(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'aref_result' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols,  optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )
    def test_readxlslist_findheader_p12_xlsx_simple_reqcol_no_header_starting_blank_lines(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'no_header' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'no_header' : True}, debug=False )
        self.assertEqual(result[0], ['', '', '', '', '', '', ''])
        self.assertEqual(result[6], list(records[0].keys()))
        self.assertEqual(result[7], list(records[0].values()))
        # self.assertEqual(result[0], records[0])
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )


        
    # XLS file processing - simple blank req_cols
    def test_readxlslist_findheader_p01_xlsx_simple_blankReqCols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readxlslist_findheader_p02_xlsx_simple_blankReqCols_aref_result(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxlslist_findheader_p03_xlsx_simple_blankReqCols_col_header(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'col_header' : True}, debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxlslist_findheader_p04_xlsx_simple_blankReqCols_no_header_start_row_return_aref(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxlslist_findheader_p05_xlsx_simple_blankReqCols_no_header_start_row_col_aref(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxlslist_findheader_p06_xlsx_simple_blankReqCols_no_header_start_row_col_aref_missing_cols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p07_xlsx_simple_blankReqCols_col_aref_blank_column(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={ 'save_row': True }, col_aref=col_aref, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxlslist_findheader_p08_xlsx_simple_blankReqCols_col_header_col_aref_missing_cols(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxlslist_findheader_p09_xlsx_simple_blankReqCols_convert_dateflds(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexlsx2, [], optiondict={ 'dateflds' : ['DateField']}, debug=False )
        self.assertEqual(result[0], records2[0])
    def test_readxlslist_findheader_p10_xlsx_simple_blankReqCols_save_row(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxlslist_findheader_p11_xlsx_simple_blankReqCols_aref_result_starting_blank_lines(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexlsx3, aref, optiondict={'aref_result' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexlsx3, [],  optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], [None, None, None, None, None, None, None])
        self.assertEqual(result[6], list(records[0].values()))
        kvutil.remove_filename( filenamexlsx3, kvutil.functionName() )
    def test_readxlslist_findheader_p12_xlsx_simple_blankReqCols_no_header_starting_blank_lines(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexlsx3, aref, optiondict={'no_header' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexlsx3, [], optiondict={'no_header' : True}, debug=False )
        self.assertEqual(result[0], [None, None, None, None, None, None, None])
        self.assertEqual(result[6], list(records[0].keys()))
        self.assertEqual(result[7], list(records[0].values()))
        kvutil.remove_filename( filenamexlsx3, kvutil.functionName() )


        
    def test_readxlslist_findheader_f01_xlsx_maxrows_exceeded_in_header_search(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexlsx3, aref, optiondict={'no_header' : True}, debug=False )
        with self.assertRaises(Exception) as context:
            kvxls.readxls2list_findheader( filenamexlsx3, req_cols, optiondict={'maxrows' : 2}, debug=False )
        kvutil.remove_filename( filenamexlsx3, kvutil.functionName() )
    def test_readxlslist_findheader_f02_xlsx_unique_columns_test(self):
        logger.debug('--------------- [%s] ---------------', kvutil.functionName()) 
        header = list(records[0].keys())
        dupkey = header[0]
        header.append(dupkey)
        aref = []
        for rec in records:
            aref.append(list(rec.values())+[rec[dupkey]])
        kvxls.writelist2xls( filenamexlsx3, aref, optiondict={'aref_result' : True}, debug=False )
        with self.assertRaises(Exception) as context:
            kvxls.readxls2list_findheader( filenamexlsx3, req_cols, optiondict={'unique_column' : True}, debug=False )
        kvutil.remove_filename( filenamexlsx3, kvutil.functionName() )


if __name__ == '__main__':
    unittest.main()
