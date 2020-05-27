import kvutil

import kvcsv
import kvmatch

import unittest

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

req_cols = ['Company', 'Wine']

# overall setup and tear down functions
def file_setup(cls):
    pass

def file_teardown(cls):
    pass


# Testing class
class TestKVCsv(unittest.TestCase):
    # executed on each test
    def setUp(self):
        # remove the file if it exists - calling with the name of the function that called us
        kvutil.remove_filename(filename,kv.functionName(2), debug=False)

    # executed at the end of all tests - cleans up the environment
    @classmethod
    def tearDownClass(cls):
        kvutil.remove_filename(filename,kv.functionName(), debug=False)

        
    def test_writelist2csv_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p02_missing_dict_elements(self):
        templist = records[:]
        del templist[1]['Company']
        del templist[1]['LastSeen']
        del templist[1]['Type']
        kvcsv.writelist2csv( filename, templist )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p03_too_many_dict_elements(self):
        templist = records[:]
        templist[1]['AddFld1'] = 'AddFld1'
        templist[1]['AddFld2'] = 'AddFld2'
        kvcsv.writelist2csv( filename, templist )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p04_dictkeys(self):
        kvcsv.writelist2csv( filename, records, req_cols )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )
    def test_writelist2csv_p05_noheader(self):
        kvcsv.writelist2csv( filename, records, header=False )
        self.assertTrue( os.path.exists(filename), 'Did not create filename:' + filename )

    def test_readcsv2list_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list( filename )
        self.assertEqual( result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_p02_headerlc(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list( filename, headerlc=True )
        self.assertEqual( len(result), len(records) )
        for key in records[0]:
            self.assertEqual( result[0][key.lower()], records[0][key] )

    def test_readcsv2dict_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        mydict = kvcsv.readcsv2dict( filename, ['Company','Wine'] )
        self.assertEqual(mydict[ kvmatch.build_multifield_key( records[0], ['Company','Wine'] )], records[0])
    def test_readcsv2dict_f01_duplicatekey(self):
        templist = records[:]
        templist.append(templist[0])
        templist.append(templist[1])
        kvcsv.writelist2csv( filename, templist )
        with self.assertRaises(Exception) as context:
            kvcsv.readcsv2dict( filename, ['Company','Wine'], True, True )

    def test_readcsv2list_findheader_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p02_col_header(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'col_header' : True }, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p03_save_row(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'save_row' : True }, debug=False )
        self.assertEqual(result[0]['XLSRow'], 2)
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p04_no_header(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'no_header' : True }, debug=False )
        self.assertEqual(result[1], list(records[0].values()))
        self.assertEqual( len(result), len(records)+1 )
    def test_readcsv2list_findheader_p05_no_header_col_aref(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader( filename, req_cols, col_aref=list(records[0].keys()), optiondict={ 'no_header' : True }, debug=False )
        self.assertEqual(result[1], records[0])
        self.assertEqual( len(result), len(records)+1 )
    def test_readcsv2list_findheader_p06_header_deep(self):
        kvcsv.writelist2csv( filename, records )
        # put blank lines at the top of the file
        flds = len( records[0].keys() )
        with open( filename, 'r' ) as f:
            fileslurp = f.read()
        with open( filename, 'w' ) as f:
            # output blank lines
            for i in range(5):
                f.write( ',' * flds + '\n')
            # and then the original content
            f.write( fileslurp )
        # debugging
        if False:
            with open( filename, 'r' ) as f:
                print(f.read())
        
        result = kvcsv.readcsv2list_findheader( filename, req_cols, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p07_header_deep_start_row(self):
        kvcsv.writelist2csv( filename, records )
        # put blank lines at the top of the file
        flds = len( records[0].keys() )
        with open( filename, 'r' ) as f:
            fileslurp = f.read()
        with open( filename, 'w' ) as f:
            # output blank lines
            for i in range(5):
                f.write( ',' * flds + '\n')
            # and then the original content
            f.write( fileslurp )
        # debugging
        if False:
            with open( filename, 'r' ) as f:
                print(f.read())
        
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'start_row' : 2 }, debug=False )
        self.assertEqual(result[0], records[0])
        self.assertEqual( len(result), len(records) )
    def test_readcsv2list_findheader_p08_header_deep_aref_result(self):
        kvcsv.writelist2csv( filename, records )
        # put blank lines at the top of the file
        flds = len( records[0].keys() )
        with open( filename, 'r' ) as f:
            fileslurp = f.read()
        with open( filename, 'w' ) as f:
            # output blank lines
            for i in range(5):
                f.write( ',' * flds + '\n')
            # and then the original content
            f.write( fileslurp )
        # debugging
        if False:
            with open( filename, 'r' ) as f:
                print(f.read())
        
        result = kvcsv.readcsv2list_findheader( filename, req_cols, optiondict={ 'aref_result' : True }, debug=False )
        self.assertEqual(result[0], list(records[0].values()))
        self.assertEqual( len(result), len(records) )

    # ---- ELIMINATE -----------
    def test_readcsv2list_findheader_old_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        result = kvcsv.readcsv2list_findheader_old( filename, req_cols, debug=False )
        self.assertEqual(result[0], records[0])
    def test_readcsv2list_findheader_old_p03_header_deep(self):
        kvcsv.writelist2csv( filename, records )
        # put blank lines at the top of the file
        flds = len( records[0].keys() )
        with open( filename, 'r' ) as f:
            fileslurp = f.read()
        with open( filename, 'w' ) as f:
            # output blank lines
            for i in range(5):
                f.write( ',' * flds + '\n')
            # and then the original content
            f.write( fileslurp )
        # debugging
        if False:
            with open( filename, 'r' ) as f:
                print(f.read())
        
        result = kvcsv.readcsv2list_findheader_old( filename, req_cols, debug=False )
        self.assertEqual(result[0], records[0])


    def test_readcsv2dict_findheader_old_p01_simple(self):
        kvcsv.writelist2csv( filename, records )
        mydict = kvcsv.readcsv2dict_findheader_old( filename, ['Company','Wine'], req_cols, debug=False )
        self.assertEqual(mydict[ kvmatch.build_multifield_key( records[0], ['Company','Wine'] )], records[0])


    def test_readcsv2dict_findheader_old_p02_header_deep(self):
        kvcsv.writelist2csv( filename, records )
        # put blank lines at the top of the file
        flds = len( records[0].keys() )
        with open( filename, 'r' ) as f:
            fileslurp = f.read()
        with open( filename, 'w' ) as f:
            # output blank lines
            for i in range(5):
                f.write( ',' * flds + '\n')
            # and then the original content
            f.write( fileslurp )
        # debugging
        if False:
            with open( filename, 'r' ) as f:
                print(f.read())

        mydict = kvcsv.readcsv2dict_findheader_old( filename, ['Company','Wine'], req_cols, debug=False )
        self.assertEqual(mydict[ kvmatch.build_multifield_key( records[0], ['Company','Wine'] )], records[0])


if __name__ == '__main__':
    unittest.main()
