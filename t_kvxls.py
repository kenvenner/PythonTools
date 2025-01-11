import kvxls
import kvutil
import unittest
import datetime
import pprint

import os

# logging
import kvlogger
config=kvlogger.get_config('t_kvxls.log', loggerlevel='DEBUG')
kvlogger.dictConfig(config)
logger=kvlogger.getLogger(__name__)

# set up filenames
filenamexls = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest', 'file_ext' : '.xls', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )
filenamexlsx = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest', 'file_ext' : '.xlsx', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )

filenamexls2 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest2', 'file_ext' : '.xls', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )
filenamexlsx2 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest2', 'file_ext' : '.xlsx', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )

filenamexls3 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest3', 'file_ext' : '.xls', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )
filenamexlsx3 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest3', 'file_ext' : '.xlsx', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )

filenamexls4 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest4', 'file_ext' : '.xls', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )
filenamexlsx4 = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest4', 'file_ext' : '.xlsx', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )




xlsfloat2datetime = [ 43080.0,  datetime.datetime.strptime('12/11/2017', '%m/%d/%Y'), '12/11/2017' ]

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

xlatdict = {'Company': 'NewCompany', 'Wine': 'Winery'}
req_cols_xlat = ['NewCompany', 'Winery']

# multi sheet xlsx credated for testing chgsheet
optiondict4 = {'sheet_name': 'set_sheet_name2', 'replace_sheet': True}
req_cols4_1 = req_cols
req_cols4_2 = req_cols2
# create xlsx to be tested with
kvxls.writelist2xls( filenamexlsx4, records)
kvxls.writelist2xls( filenamexlsx4, records2, optiondict=optiondict4, debug=False )


class TestKVxls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.debug('STARTUP')
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

                        
    # convert excel date fields to python
    def test_xldate_to_datetime_p01_float(self):
        logger.debug('STARTUP')
        self.assertEqual(kvxls.xldate_to_datetime(xlsfloat2datetime[0]), xlsfloat2datetime[1])
    def test_xldate_to_datetime_p02_string(self):
        logger.debug('STARTUP')
        self.assertEqual(kvxls.xldate_to_datetime(xlsfloat2datetime[2]), xlsfloat2datetime[1])
    def test_xldate_to_datetime_p03_blank_skipblank(self):
        logger.debug('STARTUP')
        self.assertEqual(kvxls.xldate_to_datetime('',True), '')

    def test_xldate_to_datetime_f01_blank(self):
        logger.debug('STARTUP')
        with self.assertRaises(Exception) as context:
            kvxls.xldate_to_datetime('')

    # the function name: def _extract_excel_row_into_list(xlsxfiletype, s, row, colstart, colmax, debug=False):
    # def test__extract_excel_row_into_list_p01_pass(self):
    ########################################
    # the function name: def getExcelCellValue(excel_dict, row, col_name, debug=False):
    # def test_getExcelCellValue_p01_pass(self):
    ########################################
    # the function name: def setExcelCellValue(excel_dict, row, col_name, value, debug=False):
    # def test_setExcelCellValue_p01_pass(self):
    ########################################
    # the function name: def getExcelCellPatternFill(excel_dict, row, col_name, debug=False):
    # def test_getExcelCellPatternFill_p01_pass(self):
    ########################################
    # the function name: def setExcelCellPatternFill(excel_dict, row, col_name, fill=None, start_color=None, end_color=None, fg_color=None, fill_type="solid", debug=False):
    # def test_setExcelCellPatternFill_p01_pass(self):
    ########################################
    # the function name: def copyExcelCellFmtOnRow(excel_dict_src, src_row, excel_dict_out, row, debug=False):
    # def test_copyExcelCellFmtOnRow_p01_pass(self):
    ########################################
    # the function name: def setExcelColumnValue(excel_dict, col_name, value='', debug=False):
    # def test_setExcelColumnValue_p01_pass(self):
    ########################################
    # the function name: def create_multi_key_lookup_excel(excel_dict, fldlist, copy_fields=None):
    # def test_create_multi_key_lookup_excel_p01_pass(self):
    ########################################
    # the function name: def readxls2list(xlsfile, sheetname=None, save_row=False, debug=False, optiondict=None):
    # def test_readxls2list_p01_pass(self):
    ########################################
    # the function name: def readxls2dict(xlsfile, dictkeys, sheetname=None, save_row=False, dupkeyfail=False, debug=False, optiondict=None):
    # def test_readxls2dict_p01_pass(self):
    ########################################
    # the function name: def readxls2dump(xlsfile, rows=10, sep=':', no_warnings=False, returnrecs=False, sheet_name_col=None, debug=False):
    # def test_readxls2dump_p01_pass(self):


    ### READXLS_FINDHEADER
    
    ########################################
    # the function name: def readxls_findheader(xlsfile, req_cols, xlatdict=None, optiondict=None, col_aref=None, data_only=True, debug=False):
    # XLS/XLSX - simple open and return excel_dict
    def test_readxls_findheader_p01_xls_pass(self):
        logger.debug('STARTUP')
        excel_dict = kvxls.readxls_findheader( filenamexls, req_cols, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexls)
        self.assertEqual(excel_dict['start_row'], 0)
        self.assertEqual(excel_dict['sheetmaxrow'], 12)
    def test_readxls_findheader_p02_xlsx_pass(self):
        logger.debug('STARTUP')
        excel_dict = kvxls.readxls_findheader( filenamexlsx, req_cols, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexlsx)
        self.assertEqual(excel_dict['start_row'], 0)
        self.assertEqual(excel_dict['sheetmaxrow'], 12)

    # type of field check
    def test_readxls_findheader_f01_fld_type_col_aref(self):
        logger.debug('STARTUP')
        with self.assertRaises(Exception) as context:
            excel_dict = kvxls.readxls_findheader( filenamexls, req_cols, col_aref={},  debug=False )
    def test_readxls_findheader_f02_fld_type_req_cols(self):
        logger.debug('STARTUP')
        with self.assertRaises(Exception) as context:
            excel_dict = kvxls.readxls_findheader( filenamexls, {}, debug=False )
    def test_readxls_findheader_f03_fld_type_optiondict(self):
        logger.debug('STARTUP')
        with self.assertRaises(Exception) as context:
            excel_dict = kvxls.readxls_findheader( filenamexls, req_cols, optiondict='',  debug=False )
    def test_readxls_findheader_f03_fld_type_xlatdict(self):
        logger.debug('STARTUP')
        with self.assertRaises(Exception) as context:
            excel_dict = kvxls.readxls_findheader( filenamexls, req_cols, xlatdict='',  debug=False )
    
    
    
    # xlatdict
    def test_readxls_findheader_p01_xls_xlat_pass(self):
        logger.debug('STARTUP')
        excel_dict = kvxls.readxls_findheader( filenamexls, req_cols_xlat, xlatdict=xlatdict, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexls)
        self.assertEqual(excel_dict['start_row'], 0)
    def test_readxls_findheader_p02_xlsx_xlat_pass(self):
        logger.debug('STARTUP')
        excel_dict = kvxls.readxls_findheader( filenamexlsx, req_cols_xlat, xlatdict=xlatdict, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexlsx)
        self.assertEqual(excel_dict['start_row'], 0)

    def test_readxls_findheader_f01_xls_xlat_pass(self):
        logger.debug('STARTUP')
        with self.assertRaises(Exception) as context:
            excel_dict = kvxls.readxls_findheader( filenamexls, req_cols2, xlatdict=xlatdict, debug=False )
    def test_readxls_findheader_f02_xlsx_xlat_pass(self):
        logger.debug('STARTUP')
        with self.assertRaises(Exception) as context:
            excel_dict = kvxls.readxls_findheader( filenamexlsx, req_cols2, xlatdict=xlatdict, debug=False )

    # col_header
    def test_readxls_findheader_p01_xls_col_header(self):
        logger.debug('STARTUP')
        optiondict={'col_header': True}
        excel_dict = kvxls.readxls_findheader( filenamexls, [], optiondict=optiondict, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexls)
        self.assertEqual(excel_dict['start_row'], 0)
    def test_readxls_findheader_p02_xlsx_col_header(self):
        logger.debug('STARTUP')
        optiondict={'col_header': True}
        excel_dict = kvxls.readxls_findheader( filenamexlsx, [], optiondict=optiondict, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexlsx)
        self.assertEqual(excel_dict['start_row'], 0)
        
    # no_header
    def test_readxls_findheader_p01_xls_no_header(self):
        logger.debug('STARTUP')
        optiondict={'no_header': True}
        col_aref = list(records[0].keys())
        excel_dict = kvxls.readxls_findheader( filenamexls, [], optiondict=optiondict, col_aref=col_aref, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], None)
        self.assertEqual(excel_dict['xlsfile'], filenamexls)
        self.assertEqual(excel_dict['start_row'], 0)
    def test_readxls_findheader_p02_xlsx_no_header(self):
        logger.debug('STARTUP')
        optiondict={'no_header': True}
        col_aref = list(records[0].keys())
        excel_dict = kvxls.readxls_findheader( filenamexlsx, [], optiondict=optiondict, col_aref=col_aref, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], None)
        self.assertEqual(excel_dict['xlsfile'], filenamexlsx)
        self.assertEqual(excel_dict['start_row'], 0)
    
    # col_aref only
    def test_readxls_findheader_p01_xls_col_aref(self):
        logger.debug('STARTUP')
        optiondict={}
        col_aref = ['ken1', 'ken2', 'ken3', 'ken4']
        excel_dict = kvxls.readxls_findheader( filenamexls, [], optiondict=optiondict, col_aref=col_aref, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexls)
        self.assertEqual(excel_dict['start_row'], 0)
        self.assertEqual(excel_dict['header'], ['ken1', 'ken2', 'ken3', 'ken4', 'blank001', 'blank002', 'blank003'])
    def test_readxls_findheader_p01_xlsx_col_aref(self):
        logger.debug('STARTUP')
        optiondict={}
        col_aref = ['ken1', 'ken2', 'ken3', 'ken4']
        excel_dict = kvxls.readxls_findheader( filenamexlsx, [], optiondict=optiondict, col_aref=col_aref, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexlsx)
        self.assertEqual(excel_dict['start_row'], 0)
        self.assertEqual(excel_dict['header'], ['ken1', 'ken2', 'ken3', 'ken4', 'blank001', 'blank002', 'blank003'])

    # save_row
    def test_readxls_findheader_p01_xls_save_row(self):
        logger.debug('STARTUP')
        optiondict={'save_row': True}
        excel_dict = kvxls.readxls_findheader( filenamexls, [], optiondict=optiondict, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexls)
        self.assertEqual(excel_dict['start_row'], 0)
        # need to define what we do with row header on - nothing today
        # self.assertEqual(excel_dict['header'][-1], 'XLSRow')
    def test_readxls_findheader_p01_xlsx_save_row(self):
        logger.debug('STARTUP')
        optiondict={'save_row': True}
        excel_dict = kvxls.readxls_findheader( filenamexlsx, [], optiondict=optiondict, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexlsx)
        self.assertEqual(excel_dict['start_row'], 0)
        # need to define what we do with row header on - nothing today
        # self.assertEqual(excel_dict['header'][-1], 'XLSRow')

    # simple put set the start row
    def test_readxls_findheader_p01_xls_start_row_col_aref_blank_req_cols(self):
        logger.debug('STARTUP')
        optiondict={'start_row': 3}
        col_aref = ['ken1', 'ken2', 'ken3', 'ken4']
        excel_dict = kvxls.readxls_findheader( filenamexls, [], optiondict=optiondict, col_aref=col_aref, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], None)
        self.assertEqual(excel_dict['xlsfile'], filenamexls)
        self.assertEqual(excel_dict['start_row'], 2)
        self.assertEqual(excel_dict['header'], ['ken1', 'ken2', 'ken3', 'ken4', 'blank001', 'blank002', 'blank003'])
    def test_readxls_findheader_p02_xlsx_pass(self):
        logger.debug('STARTUP')
        optiondict={'start_row': 3}
        col_aref = ['ken1', 'ken2', 'ken3', 'ken4']
        excel_dict = kvxls.readxls_findheader( filenamexlsx, [], optiondict=optiondict, col_aref=col_aref, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], None)
        self.assertEqual(excel_dict['xlsfile'], filenamexlsx)
        self.assertEqual(excel_dict['start_row'], 2)
        self.assertEqual(excel_dict['header'], ['ken1', 'ken2', 'ken3', 'ken4', 'blank001', 'blank002', 'blank003'])

    # maxrowls
    def test_readxls_findheader_p01_xls_max_rows(self):
        logger.debug('STARTUP')
        optiondict={'max_rows': 6}
        excel_dict = kvxls.readxls_findheader( filenamexls, req_cols, optiondict=optiondict, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexls)
        self.assertEqual(excel_dict['start_row'], 0)
        self.assertEqual(excel_dict['sheetmaxrow'], 6)
    def test_readxls_findheader_p02_xlsx_max_rows(self):
        logger.debug('STARTUP')
        optiondict={'max_rows': 6}
        excel_dict = kvxls.readxls_findheader( filenamexlsx, req_cols, optiondict=optiondict, debug=False )
        self.assertEqual(type(excel_dict), dict)
        self.assertEqual(excel_dict['keep_vba'], True)
        self.assertEqual(excel_dict['row_header'], 0)
        self.assertEqual(excel_dict['xlsfile'], filenamexlsx)
        self.assertEqual(excel_dict['start_row'], 0)
        self.assertEqual(excel_dict['sheetmaxrow'], 6)



        
    ### CHGSHEET_FINDHEADER

    ########################################
    # the function name: def chgsheet_findheader(excel_dict, req_cols, xlatdict=None, optiondict=None,
    def test_chgsheet_findheader_p01_xls_pass(self):
        logger.debug('STARTUP')
        # read in teh first time
        excel_dict41 = kvxls.readxls_findheader( filenamexlsx4, req_cols4_1, debug=False )
        #pprint.pprint(excel_dict41)
        # change sheet to the sheet of interest
        excel_dict42 = kvxls.chgsheet_findheader(excel_dict41, req_cols4_2, optiondict=optiondict4, debug=True)
        #pprint.pprint(excel_dict42)
        self.assertEqual(type(excel_dict42), dict)
        
        
    ### READXLS2LIST_FINDHEADER

    # XLS file processing - simple req_cols
    def test_readxls2list_findheader_p01_xls_simple_reqcols(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readxls2list_findheader_p02_xls_simple_reqcols_aref_result(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxls2list_findheader_p03_xls_simple_reqcols_col_header(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'col_header' : True}, debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxls2list_findheader_p04_xls_simple_reqcols_no_header_start_row_return_aref(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxlslist_findheader_p05_xls_simple_reqcols_no_header_start_row_col_aref(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxls2list_findheader_p06_xls_simple_reqcols_no_header_start_row_col_aref_missing_cols(self):
        logger.debug('STARTUP')
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxls2list_findheader_p07_xls_simple_reqcols_col_aref_blank_column(self):
        logger.debug('STARTUP')
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={ 'save_row': True }, col_aref=col_aref, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxls2list_findheader_p08_xls_simple_reqcols_col_header_col_aref_missing_cols(self):
        logger.debug('STARTUP')
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxls2list_findheader_p09_xls_simple_reqcols_convert_dateflds(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls2, req_cols2, optiondict={ 'dateflds' : ['DateField']}, debug=False )
        self.assertEqual(result[0], records2[0])
    def test_readxls2list_findheader_p10_xls_simple_reqcols_save_row(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxls2list_findheader_p11_xls_simple_reqcols_aref_result_starting_blank_lines(self):
        logger.debug('STARTUP')
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
    def test_readxls2list_findheader_p12_xls_simple_reqcol_no_header_starting_blank_lines(self):
        logger.debug('STARTUP')
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'no_header' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'no_header' : True}, debug=False )
        self.assertEqual(result[0], ['', '', '', '', '', '', ''])
        self.assertEqual(result[5], list(records[0].keys()))
        self.assertEqual(result[6], list(records[0].values()))
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )
    def test_readxls2list_findheader_p13_xls_simple_reqcols_break_blank_row(self):
        logger.debug('STARTUP')
        # get the first 6 records
        aref = records[:6]
        # create a non record
        rec = {x:None for x in records[0].keys()}
        # make 2 blank records
        aref.append(rec)
        aref.append(rec)
        # add two no blank records
        aref.extend(records[6:8])
        # save this out
        kvxls.writelist2xls( filenamexls3, aref, debug=False )
        # now read in the file with break on blank lines
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'break_blank_row' : True}, debug=False )
        self.assertEqual(len(result), 6)
        # now read in the file with OUT break on blank lines
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols, debug=False )
        self.assertEqual(len(result), 10)
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )

    def test_readxls2list_findheader_p14_xls_simple_reqcols_skip_blank_row(self):
        logger.debug('STARTUP')
        # get the first 6 records
        aref = records[:6]
        # create a non record
        rec = {x:None for x in records[0].keys()}
        # make 2 blank records
        aref.append(rec)
        aref.append(rec)
        # add two no blank records
        aref.extend(records[6:8])
        # save this out
        kvxls.writelist2xls( filenamexls3, aref, debug=False )
        # now read in the file with break on blank lines
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'skip_blank_row' : True}, debug=False )
        self.assertEqual(len(result), 8)
        # now read in the file with OUT break on blank lines
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols, debug=False )
        self.assertEqual(len(result), 10)
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )


        
    # XLS file processing - simple blank req_cols
    def test_readxls2list_findheader_p01_xls_simple_blankReqCols(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, [], debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readxls2list_findheader_p02_xls_simple_blankReqCols_aref_result(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxls2list_findheader_p03_xls_simple_blankReqCols_col_header(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'col_header' : True}, debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxls2list_findheader_p04_xls_simple_blankReqCols_no_header_start_row_return_aref(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxls2list_findheader_p05_xls_simple_blankReqCols_no_header_start_row_col_aref(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxls2list_findheader_p06_xls_simple_blankReqCols_no_header_start_row_col_aref_missing_cols(self):
        logger.debug('STARTUP') 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxls2list_findheader_p07_xls_simple_blankReqCols_col_aref_blank_column(self):
        logger.debug('STARTUP') 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={ 'save_row': True }, col_aref=col_aref, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxls2list_findheader_p08_xls_simple_blankReqCols_col_header_col_aref_missing_cols(self):
        logger.debug('STARTUP') 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxls2list_findheader_p09_xls_simple_blankReqCols_convert_dateflds(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls2, [], optiondict={ 'dateflds' : ['DateField']}, debug=False )
        self.assertEqual(result[0], records2[0])
    def test_readxls2list_findheader_p10_xls_simple_blankReqCols_save_row(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls, [], optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxls2list_findheader_p11_xls_simple_blankReqCols_aref_result_starting_blank_lines(self):
        logger.debug('STARTUP') 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'aref_result' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, [], optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], ['', '', '', '', '', '', ''])
        self.assertEqual(result[5], list(records[0].values()))
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )
    def test_readxls2list_findheader_p12_xls_simple_blankReqCols_no_header_starting_blank_lines(self):
        logger.debug('STARTUP') 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'no_header' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, [], optiondict={'no_header' : True}, debug=False )
        self.assertEqual(result[0], ['', '', '', '', '', '', ''])
        self.assertEqual(result[5], list(records[0].keys()))
        self.assertEqual(result[6], list(records[0].values()))
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )


        
    def test_readxls2list_findheader_f01_xls_simple_maxrows_exceeded_in_header_search(self):
        logger.debug('STARTUP') 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'no_header' : True}, debug=False )
        with self.assertRaises(Exception) as context:
            kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'maxrows' : 2}, debug=False )
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )
    def test_readxls2list_findheader_f02_xls_simple_unique_columns_test(self):
        logger.debug('STARTUP') 
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
    def test_readxls2list_findheader_p01_xlsx_simple_reqcols(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readxls2list_findheader_p02_xlsx_simple_reqcols_aref_result(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxls2list_findheader_p03_xlsx_simple_reqcols_col_header(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'col_header' : True}, debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxls2list_findheader_p04_xlsx_simple_reqcols_no_header_start_row_return_aref(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxls2list_findheader_p05_xlsx_simple_reqcols_no_header_start_row_col_aref(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxls2list_findheader_p06_xlsx_simple_reqcols_no_header_start_row_col_aref_missing_cols(self):
        logger.debug('STARTUP') 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxls2list_findheader_p07_xlsx_simple_reqcols_col_aref_blank_column(self):
        logger.debug('STARTUP') 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={ 'save_row': True }, col_aref=col_aref, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxls2list_findheader_p08_xlsx_simple_reqcols_col_header_col_aref_missing_cols(self):
        logger.debug('STARTUP') 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxls2list_findheader_p09_xlsx_simple_reqcols_convert_dateflds(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexls2, req_cols2, optiondict={ 'dateflds' : ['DateField']}, debug=False )
        self.assertEqual(result[0], records2[0])
    def test_readxls2list_findheader_p10_xlsx_simple_reqcols_save_row(self):
        logger.debug('STARTUP')
        result = kvxls.readxls2list_findheader( filenamexls, req_cols, optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxls2list_findheader_p11_xlsx_simple_reqcols_aref_result_starting_blank_lines(self):
        logger.debug('STARTUP') 
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
    def test_readxls2list_findheader_p12_xlsx_simple_reqcol_no_header_starting_blank_lines(self):
        logger.debug('STARTUP') 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexls3, aref, optiondict={'no_header' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexls3, req_cols, optiondict={'no_header' : True}, debug=False )
        self.assertEqual(result[0], ['', '', '', '', '', '', ''])
        self.assertEqual(result[5], list(records[0].keys()))
        self.assertEqual(result[6], list(records[0].values()))
        # self.assertEqual(result[0], records[0])
        kvutil.remove_filename( filenamexls3, kvutil.functionName() )


        
    # XLS file processing - simple blank req_cols
    def test_readxls2list_findheader_p01_xlsx_simple_blankReqCols(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readxls2list_findheader_p02_xlsx_simple_blankReqCols_aref_result(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxls2list_findheader_p03_xlsx_simple_blankReqCols_col_header(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'col_header' : True}, debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxls2list_findheader_p04_xlsx_simple_blankReqCols_no_header_start_row_return_aref(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'no_header' : True, 'start_row' : 2}, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
    def test_readxls2list_findheader_p05_xlsx_simple_blankReqCols_no_header_start_row_col_aref(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'no_header' : True, 'start_row' : 2}, col_aref=list(records[0].keys()), debug=False )
        self.assertEqual(result[0], records[0])
    def test_readxls2list_findheader_p06_xlsx_simple_blankReqCols_no_header_start_row_col_aref_missing_cols(self):
        logger.debug('STARTUP') 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'no_header' : True, 'start_row' : 2}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxls2list_findheader_p07_xlsx_simple_blankReqCols_col_aref_blank_column(self):
        logger.debug('STARTUP') 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={ 'save_row': True }, col_aref=col_aref, debug=False )
        self.assertTrue('blank001' in result[0].keys())
    def test_readxls2list_findheader_p08_xlsx_simple_blankReqCols_col_header_col_aref_missing_cols(self):
        logger.debug('STARTUP') 
        col_aref = list(records[0].keys())[:-2]
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={'col_header' : True}, col_aref=col_aref, debug=False )
        # manipulate the data to make them match - first copy the data so we don't change the original
        temprec = dict(records[0])
        temprec['blank001'] = temprec['Type']
        del temprec['Type']
        temprec['blank002'] = temprec['LastSeen']
        del temprec['LastSeen']
        self.assertEqual(result[0], temprec)
    def test_readxls2list_findheader_p09_xlsx_simple_blankReqCols_convert_dateflds(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexlsx2, [], optiondict={ 'dateflds' : ['DateField']}, debug=False )
        self.assertEqual(result[0], records2[0])
    def test_readxls2list_findheader_p10_xlsx_simple_blankReqCols_save_row(self):
        logger.debug('STARTUP') 
        result = kvxls.readxls2list_findheader( filenamexlsx, [], optiondict={ 'save_row': True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
    def test_readxls2list_findheader_p11_xlsx_simple_blankReqCols_aref_result_starting_blank_lines(self):
        logger.debug('STARTUP') 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexlsx3, aref, optiondict={'aref_result' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexlsx3, [],  optiondict={'aref_result' : True}, debug=False )
        self.assertEqual(result[0], [None, None, None, None, None, None, None])
        self.assertEqual(result[5], list(records[0].values()))
        kvutil.remove_filename( filenamexlsx3, kvutil.functionName() )
    def test_readxls2list_findheader_p12_xlsx_simple_blankReqCols_no_header_starting_blank_lines(self):
        logger.debug('STARTUP') 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexlsx3, aref, optiondict={'no_header' : True}, debug=False )
        # now read in the file
        result = kvxls.readxls2list_findheader( filenamexlsx3, [], optiondict={'no_header' : True}, debug=False )
        self.assertEqual(result[0], [None, None, None, None, None, None, None])
        self.assertEqual(result[5], list(records[0].keys()))
        self.assertEqual(result[6], list(records[0].values()))
        kvutil.remove_filename( filenamexlsx3, kvutil.functionName() )


        
    def test_readxls2list_findheader_f01_xlsx_maxrows_exceeded_in_header_search(self):
        logger.debug('STARTUP') 
        # create a list of values that are used to create the xls - we have 6 blank lines at the top
        aref = [[''],[''],[''],[''],['']]
        aref.append(list(records[0].keys()))
        for rec in records:
            aref.append(list(rec.values()))
        kvxls.writelist2xls( filenamexlsx3, aref, optiondict={'no_header' : True}, debug=False )
        with self.assertRaises(Exception) as context:
            kvxls.readxls2list_findheader( filenamexlsx3, req_cols, optiondict={'maxrows' : 2}, debug=False )
        kvutil.remove_filename( filenamexlsx3, kvutil.functionName() )
    def test_readxls2list_findheader_f02_xlsx_unique_columns_test(self):
        logger.debug('STARTUP') 
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


    # the function name: def excelDict2list_findheader(excel_dict, req_cols, xlatdict=None, optiondict=None, col_aref=None, debug=False):
    # def test_excelDict2list_findheader_p01_pass(self):
    ########################################
    # the function name: def readxls2dict_findheader(xlsfile, dictkeys, req_cols=None, xlatdict=None, optiondict=None,
    # def test_readxls2dict_findheader_p01_pass(self):
    ########################################
    # the function name: def writedict2xls(xlsfile, data, col_aref=None, optiondict={}, debug=False):
    # def test_writedict2xls_p01_pass(self):
    
    ########################################
    # the function name: def writelist2xls(xlsfile, data, col_aref=None, optiondict=None, debug=False):
    def test_writelist2xls_p01_xlsx_simple_pass(self):
        # list of dicts
        logger.debug('STARTUP')
        filename = kvxls.writelist2xls( filenamexlsx3, records, debug=False )
        # self.assertEqual(filename, filenamexlsx3)
        results = kvxls.readxls2list( filenamexlsx3 )
        self.assertEqual( records, results )
        kvutil.remove_filename( filenamexlsx3 )
    def test_writelist2xls_p02_xlsx_nodata(self):
        # no data
        logger.debug('STARTUP')
        filename = kvxls.writelist2xls( filenamexlsx3, None, debug=False )
        # self.assertEqual(filename, filenamexlsx3)
        results = kvxls.readxls2list( filenamexlsx3 )
        self.assertEqual( results, [] )
        kvutil.remove_filename( filenamexlsx3 )
    def test_writelist2xls_p03_xlsx_set_sheet(self):
        # list of dicts and set the sheet name created
        logger.debug('STARTUP')
        optiondict={'sheet_name': 'set_sheet_name'}
        filename = kvxls.writelist2xls( filenamexlsx3, records, optiondict=optiondict, debug=False )
        # self.assertEqual(filename, filenamexlsx3)
        results = kvxls.readxls2list( filenamexlsx3, optiondict=optiondict )
        self.assertEqual( records, results )
        kvutil.remove_filename( filenamexlsx3 )
    def test_writelist2xls_p04_xlsx_set_and_limit_column_order(self):
        # list of dicts - set column order and limit columns
        logger.debug('STARTUP')
        col_aref=['Wine', 'Company', 'Vintage']
        filename = kvxls.writelist2xls( filenamexlsx3, records, col_aref=col_aref, debug=False )
        # self.assertEqual(filename, filenamexlsx3)
        results = kvxls.readxls2list( filenamexlsx3 )
        match_records = [{x: v[x] for x in col_aref} for v in records]
        self.assertEqual( results, match_records )
        kvutil.remove_filename( filenamexlsx3 )
    def test_writelist2xls_p05_xlsx_list(self):
        # array of data and we pass in the header
        logger.debug('STARTUP')
        rec_array = [[v[k] for k in v.keys()] for v in records]
        filename = kvxls.writelist2xls( filenamexlsx3, rec_array, col_aref=list(records[0].keys()), debug=False )
        # self.assertEqual(filename, filenamexlsx3)
        results = kvxls.readxls2list( filenamexlsx3 )
        self.assertEqual( records, results )
        kvutil.remove_filename( filenamexlsx3 )
    def test_writelist2xls_p06_xlsx_set_sheet_2sheets(self):
        # list of dicts and set the sheet name created
        logger.debug('STARTUP')
        optiondict={'sheet_name': 'set_sheet_name1'}
        filename = kvxls.writelist2xls( filenamexlsx3, records, optiondict=optiondict, debug=False )
        # self.assertEqual(filename, filenamexlsx3)
        results = kvxls.readxls2list( filenamexlsx3, optiondict=optiondict )
        self.assertEqual( records, results )
        # now build 2nd sheet
        optiondict2={'sheet_name': 'set_sheet_name2', 'replace_sheet': True}
        filename = kvxls.writelist2xls( filenamexlsx3, records, optiondict=optiondict2, debug=False )
        results = kvxls.readxls2list( filenamexlsx3, optiondict=optiondict )
        self.assertEqual( records, results )
        results = kvxls.readxls2list( filenamexlsx3, optiondict=optiondict2 )
        self.assertEqual( records, results )
        kvutil.remove_filename( filenamexlsx3 )
    def test_writelist2xls_p07_xlsx_aref_result(self):
        # array of data and we pass in the header
        logger.debug('STARTUP')
        rec_array = [[v[k] for k in v.keys()] for v in records]
        optiondict={'aref_result': True}
        filename = kvxls.writelist2xls( filenamexlsx3, records, optiondict=optiondict, debug=False )
        # self.assertEqual(filename, filenamexlsx3)
        results = kvxls.readxls2list( filenamexlsx3, optiondict=optiondict )
        self.assertEqual( rec_array, results )
        kvutil.remove_filename( filenamexlsx3 )
    def test_writelist2xls_p08_xlsx_no_header(self):
        # array of data and we pass in the header
        logger.debug('STARTUP')
        col_aref = list(records[0].keys())
        optiondict={'no_header': True}
        filename = kvxls.writelist2xls( filenamexlsx3, records, optiondict=optiondict, debug=False )
        # self.assertEqual(filename, filenamexlsx3)
#        results = kvxls.readxls2list( filenamexlsx3, optiondict=optiondict, col_aref=col_aref )
        results = kvxls.readxls2list_findheader( filenamexlsx3, [], optiondict=optiondict, col_aref=col_aref, debug=False )
        self.assertEqual( records, results )
        kvutil.remove_filename( filenamexlsx3 )
    def test_writelist2xls_p09_xlsx_start_row(self):
        # list of dicts
        logger.debug('STARTUP')
        optiondict = {'start_row': 3}
        filename = kvxls.writelist2xls( filenamexlsx3, records, optiondict=optiondict, debug=False )
        # self.assertEqual(filename, filenamexlsx3)
        optiondict={'no_header': True}
        col_aref = None
        results = kvxls.readxls2list_findheader( filenamexlsx3, [], optiondict=optiondict, col_aref=col_aref, debug=False )
        self.assertEqual(results[0], [None, None, None, None, None, None, None])
        self.assertEqual(results[2], list(records[0].keys()))
        self.assertEqual(results[3], list(records[0].values()))
        kvutil.remove_filename( filenamexlsx3 )

    # the function name: def writexls(excel_dict, xlsfile, xlsm=False, debug=False):
    # def test_writexls_p01_pass(self):
        
if __name__ == '__main__':
    unittest.main()
