import kvutil

import kvcsv
import kvmatch

import unittest

import time
import copy
import os


# logging
import kvlogger
config=kvlogger.get_config('t_kvcsv.log')
kvlogger.dictConfig(config)
logger=kvlogger.getLogger(__name__)

# set up data that is used by these tests
filename = kvutil.filename_unique( { 'base_filename' : 't_kvcsvtest', 'file_ext' : '.csv', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )

rowdict = { 'Company' : 'Test', 'Wine' : 'Yummy', 'Price' : 10.00 }

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

# build up the dictionary data for testing
dictkeyfld = 'RecID'

dictkeyval = '{:03d}'.format(1)

reccnt=1
dictrecords = {}
for rec in records:
    key='{:03d}'.format(reccnt)
    rec[dictkeyfld] = key
    dictrecords[key]=rec
    reccnt += 1

req_cols = ['Company', 'Wine']


# Testing class
class TestKVCsv(unittest.TestCase):
    # executed on each test
    def setUp(self):
        kvutil.remove_filename(filename,kvutil.functionName(2), debug=False)

    def tearDown(self):
        kvutil.remove_filename(filename,kvutil.functionName(2), debug=False)

        
    # executed at the end of all tests - cleans up the environment
    @classmethod
    def tearDownClass(cls):
        kvutil.remove_filename(filename,kvutil.functionName(), debug=False)

    @classmethod
    def setUpClass(cls):
        kvutil.remove_filename(filename,kvutil.functionName(), debug=False)


    def test_max_column_list_p01_simple_1_1(self):
        self.assertEqual( kvcsv.max_column_list( [{'Field1' : 'value1'}] ), ['Field1'] )
    def test_max_column_list_p01_simple_1_2(self):
        self.assertEqual( kvcsv.max_column_list( [{'Field1' : 'value1', 'Field2' : 'value2'}] ), ['Field1','Field2'] )
    def test_max_column_list_p01_simple_2_1(self):
        self.assertEqual( kvcsv.max_column_list( [{'Field1' : 'value1'}, {'Field2' : 'value2'}] ), ['Field1','Field2'] )
    def test_max_column_list_p01_simple_2_mix(self):
        self.assertEqual( kvcsv.max_column_list( [{'Field1' : 'value1', 'Field2' : 'value2'}, {'Field2' : 'value2', 'Field3' : 'value3'}] ), ['Field1','Field2','Field3'] )
        

        
        
    def test_writelist2csv_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p02_missing_dict_elements(self):
        templist = copy.deepcopy(records)
        del templist[0]['Company']
        del templist[0]['LastSeen']
        del templist[0]['Type']
        kvcsv.writelist2csv( filename, templist )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p03_missing_dict_elements_csvfields(self):
        templist = copy.deepcopy(records)
        csvfields = list(templist[0].keys())
        del templist[0]['Company']
        del templist[0]['LastSeen']
        del templist[0]['Type']
        kvcsv.writelist2csv( filename, templist, csvfields )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p04_missing_dict_elements_maxcolumns(self):
        templist = copy.deepcopy(records)
        del templist[0]['Company']
        del templist[0]['LastSeen']
        del templist[0]['Type']
        kvcsv.writelist2csv( filename, templist, maxcolumns=True )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p05_too_many_dict_elements(self):
        templist = copy.deepcopy(records)
        templist[0]['AddFld1'] = 'AddFld1'
        templist[0]['AddFld2'] = 'AddFld2'
        kvcsv.writelist2csv( filename, templist )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p06_too_many_dict_elements_csvfields(self):
        templist = copy.deepcopy(records)
        csvfields = list(templist[0].keys())
        templist[0]['AddFld1'] = 'AddFld1'
        templist[0]['AddFld2'] = 'AddFld2'
        kvcsv.writelist2csv( filename, templist, csvfields )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p07_dictkeys(self):
        kvcsv.writelist2csv( filename, records, req_cols )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p08_noheader(self):
        kvcsv.writelist2csv( filename, records, header=False )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p09_noheader_append(self):
        kvcsv.writelist2csv( filename, records, header=False )
        kvcsv.writelist2csv( filename, records, header=False, mode='a' )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p10_set_output_cols(self):
        col_aref=['Wine', 'Company', 'Vintage']
        kvcsv.writelist2csv( filename, records, col_aref=col_aref, debug=False )
        results = kvcsv.readcsv2list( filename )
        match_records = [{x: v[x] for x in col_aref} for v in records]
        self.assertEqual( results, match_records )


    def test_writedict2csv_p01_simple(self):
        kvcsv.writedict2csv( filename, dictrecords )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writedict2csv_p02_missing_dict_elements(self):
        templist = copy.deepcopy(dictrecords)
        key1 = list(templist.keys())[0]
        del templist[key1]['Company']
        del templist[key1]['LastSeen']
        del templist[key1]['Type']
        kvcsv.writedict2csv( filename, templist )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writedict2csv_p03_missing_dict_elements_csvfields(self):
        templist = copy.deepcopy(dictrecords)
        key1 = list(templist.keys())[0]
        csvfields = list(templist[key1].keys())
        del templist[key1]['Company']
        del templist[key1]['LastSeen']
        del templist[key1]['Type']
        kvcsv.writedict2csv( filename, templist, csvfields )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writedict2csv_p04_missing_dict_elements_maxcolumns(self):
        templist = copy.deepcopy(dictrecords)
        key1 = list(templist.keys())[0]
        del templist[key1]['Company']
        del templist[key1]['LastSeen']
        del templist[key1]['Type']
        kvcsv.writedict2csv( filename, templist, maxcolumns=True )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writedict2csv_p05_too_many_dict_elements(self):
        templist = copy.deepcopy(dictrecords)
        key1 = list(templist.keys())[0]
        templist[key1]['AddFld1'] = 'AddFld1'
        templist[key1]['AddFld2'] = 'AddFld2'
        kvcsv.writedict2csv( filename, templist )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writedict2csv_p06_too_many_dict_elements_csvfields(self):
        templist = copy.deepcopy(dictrecords)
        key1 = list(templist.keys())[0]
        csvfields = list(templist[key1].keys())
        templist[key1]['AddFld1'] = 'AddFld1'
        templist[key1]['AddFld2'] = 'AddFld2'
        kvcsv.writedict2csv( filename, templist, csvfields )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writedict2csv_p07_dictkeys(self):
        kvcsv.writedict2csv( filename, dictrecords, req_cols )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writedict2csv_p08_noheader(self):
        kvcsv.writedict2csv( filename, dictrecords, header=False )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writedict2csv_p08_noheader_append(self):
        kvcsv.writedict2csv( filename, dictrecords, header=False )
        kvcsv.writedict2csv( filename, dictrecords, header=False, mode='a' )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )


    def test_readcsv2list_with_header_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        result,header = kvcsv.readcsv2list_with_header( filename )
        self.assertEqual( result[0], records[0])
        self.assertEqual( len(result), len(records) )
        self.assertEqual(header, list(records[0].keys()))
    def test_readcsv2list_with_header_p01_headerlc(self):
        kvcsv.writelist2csv( filename, records )
        result,header = kvcsv.readcsv2list_with_header( filename, headerlc=True )
        record1lc = { x.lower():y for x,y in records[0].items() }
        self.assertEqual( result[0], record1lc)
        self.assertEqual( len(result), len(records) )
        self.assertEqual(header, list(record1lc.keys()))


    def test_readcsv2list_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list( filename )
        self.assertEqual( result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_p02_headerlc(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list( filename, headerlc=True )
        record1lc = { x.lower():y for x,y in records[0].items() }
        self.assertEqual( result[0], record1lc)
        self.assertEqual( len(result), len(records) )


    def test_readcsv2dict_with_header_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        result, header, dupcount = kvcsv.readcsv2dict_with_header( filename, req_cols )
        self.assertEqual(result[ kvmatch.build_multifield_key( records[0], req_cols )], records[0])
        self.assertEqual(header, list(records[0].keys()))
        self.assertEqual(dupcount,0)
    def test_readcsv2dict_with_header_p02_headerlc(self):
        kvcsv.writelist2csv( filename, records )
        result, header, dupcount = kvcsv.readcsv2dict_with_header( filename, req_cols, headerlc=True )
        record1lc = { x.lower():y for x,y in records[0].items() }
        self.assertEqual(result[ kvmatch.build_multifield_key( records[0], req_cols )], record1lc)
        self.assertEqual(header, list(record1lc.keys()))
        self.assertEqual(dupcount,0)
    def test_readcsv2dict_with_header_p03_dup_warning(self):
        duprecords = copy.deepcopy(records)
        duprecords.append( records[0] )
        kvcsv.writelist2csv( filename, duprecords )
        result, header, dupcount = kvcsv.readcsv2dict_with_header( filename, req_cols )
        self.assertEqual(result[ kvmatch.build_multifield_key( records[0], req_cols )], records[0])
        self.assertEqual(header, list(records[0].keys()))
        self.assertEqual(dupcount,1)
    def test_readcsv2dict_with_header_f01_dupkeyfail_nowarning(self):
        duprecords = copy.deepcopy(records)
        duprecords.append( records[0] )
        kvcsv.writelist2csv( filename, duprecords )
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_header( filename, req_cols, dupkeyfail=True )
    def test_readcsv2dict_with_header_f02_dupkeyfail_warning(self):
        duprecords = copy.deepcopy(records)
        duprecords.append( records[0] )
        kvcsv.writelist2csv( filename, duprecords )
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_header( filename, req_cols, dupkeyfail=True, noshowwarning=True )

    def test_readcsv2dict_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2dict( filename, req_cols )
        self.assertEqual(result[ kvmatch.build_multifield_key( records[0], req_cols )], records[0])
    def test_readcsv2dict_p02_headerlc(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2dict( filename, req_cols, headerlc=True )
        record1lc = { x.lower():y for x,y in records[0].items() }
        self.assertEqual(result[ kvmatch.build_multifield_key( records[0], req_cols )], record1lc)
    def test_readcsv2dict_p03_dup_warning(self):
        duprecords = copy.deepcopy(records)
        duprecords.append( records[0] )
        kvcsv.writelist2csv( filename, duprecords )
        result = kvcsv.readcsv2dict( filename, req_cols )
        self.assertEqual(result[ kvmatch.build_multifield_key( records[0], req_cols )], records[0])
    def test_readcsv2dict_f01_dupkeyfail_nowarning(self):
        duprecords = copy.deepcopy(records)
        duprecords.append( records[0] )
        kvcsv.writelist2csv( filename, duprecords )
        with self.assertRaises(Exception) as context:
            result = kvcsv.readcsv2dict( filename, req_cols, dupkeyfail=True )
    def test_readcsv2dict_f02_dupkeyfail_warning(self):
        duprecords = copy.deepcopy(records)
        duprecords.append( records[0] )
        kvcsv.writelist2csv( filename, duprecords )
        with self.assertRaises(Exception) as context:
            result = kvcsv.readcsv2dict( filename, req_cols, dupkeyfail=True, noshowwarning=True )


    def test_readcsv2dict_with_noheader_p01_simple(self):
        kvcsv.writelist2csv( filename, records, header=False )
        header = list(records[0].keys())
        result, header, dupcount = kvcsv.readcsv2dict_with_noheader( filename, req_cols, header )
        self.assertEqual(result[ kvmatch.build_multifield_key( records[0], req_cols )], records[0])
        self.assertEqual(header, list(records[0].keys()))
        self.assertEqual(dupcount,0)
    def test_readcsv2dict_with_noheader_p02_dup_warning(self):
        duprecords = copy.deepcopy(records)
        duprecords.append( records[0] )
        kvcsv.writelist2csv( filename, duprecords, header=False )
        header = list(records[0].keys())
        result, header, dupcount = kvcsv.readcsv2dict_with_noheader( filename, req_cols, header )
        self.assertEqual(result[ kvmatch.build_multifield_key( records[0], req_cols )], records[0])
        self.assertEqual(header, list(records[0].keys()))
        self.assertEqual(dupcount,1)
    def test_readcsv2dict_with_noheader_f01_dupkeyfail_nowarning(self):
        duprecords = copy.deepcopy(records)
        duprecords.append( records[0] )
        kvcsv.writelist2csv( filename, duprecords )
        header = list(records[0].keys())
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_noheader( filename, req_cols, header, dupkeyfail=True )
    def test_readcsv2dict_with_noheader_f02_no_reqcols(self):
        kvcsv.writelist2csv( filename, records, header=False )
        header = list(records[0].keys())
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_noheader( filename, [], header )
    def test_readcsv2dict_with_noheader_f03_no_header(self):
        kvcsv.writelist2csv( filename, records, header=False )
        header = list(records[0].keys())
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_noheader( filename, req_cols, [] )


    def test_readcsv2list_findheader_p01_reqcols_simple(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p02_reqcols_col_header(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'col_header' : True }, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p03_reqcols_col_header_col_aref(self):
        kvcsv.writelist2csv( filename, records )
        col_aref = [x.upper() for x in list(records[0].keys())]
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'col_header' : True }, col_aref=col_aref, debug=False )
        
        self.assertEqual(result[0], {x.upper():y for x,y in records[0].items()})
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p04_reqcols_save_row(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'save_row' : True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p05_reqcols_no_header(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'no_header' : True }, debug=False )
        self.assertEqual(result[1], list(records[0].values()))
        self.assertEqual( len(result), len(records)+1 )
    def test_readcsv2list_findheader_p06_reqcols_no_header_col_aref(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, col_aref=list(records[0].keys()), optiondict={ 'no_header' : True }, debug=False )
        self.assertEqual(result[1], records[0])
        self.assertEqual( len(result), len(records)+1 )
    def test_readcsv2list_findheader_p07_reqcols_header_deep(self):
        blankrec = { x : '' for x in records[0].keys() }
        headerrec = { x : x for x in records[0].keys() }
        aref = []
        for i in range(5):
            aref.append( blankrec )
        aref.append(headerrec)
        aref.extend(records)
        kvcsv.writelist2csv( filename, aref, list(records[0].keys()), header=False )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p08_reqcols_header_deep_start_row(self):
        blankrec = { x : '' for x in records[0].keys() }
        headerrec = { x : x for x in records[0].keys() }
        aref = []
        for i in range(5):
            aref.append( blankrec )
        aref.append(headerrec)
        aref.extend(records)
        kvcsv.writelist2csv( filename, aref, list(records[0].keys()), header=False )

        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'start_row' : 2 }, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p09_reqcols_header_deep_aref_result(self):
        blankrec = { x : '' for x in records[0].keys() }
        headerrec = { x : x for x in records[0].keys() }
        aref = []
        for i in range(5):
            aref.append( blankrec )
        aref.append(headerrec)
        aref.extend(records)
        kvcsv.writelist2csv( filename, aref, list(records[0].keys()), header=False )
        
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'aref_result' : True }, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
        self.assertEqual( len(result), len(records) )


    def test_readcsv2dict_findheader_p01_reqcols_simple(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2dict_findheader( filename, req_cols, [dictkeyfld], debug=False )
        self.assertEqual(result[dictkeyval], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2dict_findheader_p02_reqcols_col_header(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2dict_findheader( filename, req_cols, [dictkeyfld], optiondict={ 'col_header' : True }, debug=False )
        self.assertEqual(result[dictkeyval], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2dict_findheader_p03_reqcols_col_header_col_aref(self):
        kvcsv.writelist2csv( filename, records )
        col_aref = [x.upper() for x in list(records[0].keys())]
        upperdictkeyfld = dictkeyfld.upper()
        result = kvcsv.readcsv2dict_findheader( filename, req_cols, [upperdictkeyfld], optiondict={ 'col_header' : True }, col_aref=col_aref, debug=False )
        
        self.assertEqual(result[dictkeyval], {x.upper():y for x,y in records[0].items()})
        self.assertEqual( len(result), len(records) )
    def test_readcsv2dict_findheader_p04_reqcols_save_row(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2dict_findheader( filename, req_cols, [dictkeyfld], optiondict={ 'save_row' : True }, debug=False )
        self.assertEqual(result[dictkeyval]['XLSRow'], 2)
        self.assertEqual( len(result), len(records) )
    def test_readcsv2dict_findheader_f05_reqcols_no_header(self):
        kvcsv.writelist2csv( filename, records )
        with self.assertRaises(Exception) as context:
            result = kvcsv.readcsv2dict_findheader( filename, req_cols, [dictkeyfld], optiondict={ 'no_header' : True }, debug=False )
    def test_readcsv2dict_findheader_p06_reqcols_no_header_col_aref(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2dict_findheader( filename, req_cols, [dictkeyfld], col_aref=list(records[0].keys()), optiondict={ 'no_header' : True }, debug=False )
        self.assertEqual(result[dictkeyval], records[0])
        self.assertEqual( len(result), len(records)+1 )
    def test_readcsv2dict_findheader_p07_reqcols_header_deep(self):
        blankrec = { x : '' for x in records[0].keys() }
        headerrec = { x : x for x in records[0].keys() }
        aref = []
        for i in range(5):
            aref.append( blankrec )
        aref.append(headerrec)
        aref.extend(records)
        kvcsv.writelist2csv( filename, aref, list(records[0].keys()), header=False )
        result = kvcsv.readcsv2dict_findheader( filename, req_cols, [dictkeyfld], debug=False )
        self.assertEqual(result[dictkeyval], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2dict_findheader_p08_reqcols_header_deep_start_row(self):
        blankrec = { x : '' for x in records[0].keys() }
        headerrec = { x : x for x in records[0].keys() }
        aref = []
        for i in range(5):
            aref.append( blankrec )
        aref.append(headerrec)
        aref.extend(records)
        kvcsv.writelist2csv( filename, aref, list(records[0].keys()), header=False )

        result = kvcsv.readcsv2dict_findheader( filename, req_cols, [dictkeyfld], optiondict={ 'start_row' : 2 }, debug=False )
        self.assertEqual(result[dictkeyval], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2dict_findheader_f09_reqcols_header_deep_aref_result(self):
        blankrec = { x : '' for x in records[0].keys() }
        headerrec = { x : x for x in records[0].keys() }
        aref = []
        for i in range(5):
            aref.append( blankrec )
        aref.append(headerrec)
        aref.extend(records)
        kvcsv.writelist2csv( filename, aref, list(records[0].keys()), header=False )
        with self.assertRaises(Exception) as context:      
            result = kvcsv.readcsv2dict_findheader( filename, req_cols, [dictkeyfld], optiondict={ 'aref_result' : True }, debug=False )
        

if __name__ == '__main__':
    unittest.main()
#eof
