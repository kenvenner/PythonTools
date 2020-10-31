import kvxls
import kvutil
import unittest
import datetime

import os

# test for creation of xls and xlsx files

xlsfloat2datetime = [ 43080.0,  datetime.datetime.strptime('12/11/2017', '%m/%d/%Y') ]

filenamexlsx = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest', 'file_ext' : '.xlsx', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )
filenamexls  = kvutil.filename_unique( { 'base_filename' : 't_kvxlstest', 'file_ext' : '.xls', 'uniqtype' : 'datecnt', 'overwrite' : True, 'forceuniq' : True } )

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

class TestKVxlsWrite(unittest.TestCase):
    def test_writelist2xls_p01_xlsx_simple(self):
        self.assertFalse( kvxls.writelist2xls( filenamexlsx, records, list(records[0].keys()) ) )
    def test_writelist2xls_p02_xlsx_no_col_aref(self):
        self.assertFalse( kvxls.writelist2xls( filenamexlsx, records) )
    def test_writelist2xls_p03_xlsx_list_no_col_aref(self):
        templist = [list(record.values()) for record in records]
        self.assertFalse( kvxls.writelist2xls( filenamexlsx, records) )

    def test_writelist2xls_p01_xls_simple(self):
        self.assertFalse( kvxls.writelist2xls( filenamexls, records, list(records[0].keys()) ) )



if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        pass
        #        if os.path.exists(filename): os. remove(filename)
        print('filenamexls:', filenamexls)
        print('filenamexlsx:', filenamexlsx)
