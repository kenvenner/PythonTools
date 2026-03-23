import kvutil

import kvcsv
import kvmatch

import unittest

import copy
import os


# logging
import kvlogger

config = kvlogger.get_config("t_kvcsv.log")
kvlogger.dictConfig(config)
logger = kvlogger.getLogger(__name__)

# set up data that is used by these tests
filename = kvutil.filename_unique(
    {
        "base_filename": "t_kvcsvtest",
        "file_ext": ".csv",
        "uniqtype": "datecnt",
        "overwrite": True,
        "forceuniq": True,
    }
)

rowdict = {"Company": "Test", "Wine": "Yummy", "Price": 10.00}

RECORDS = [
    {
        "Company": "NHLiq",
        "Wine": "Caravan Cabernet Sauvignon",
        "Vintage_Wine": "Caravan Cabernet Sauvignon 2014",
        "Vintage": "2014",
        "Date": "12/11/2017",
        "Type": "red-cab",
        "LastSeen": "Never",
    },
    {
        "Company": "BevMo",
        "Wine": "Caymus Cabernet Sauvignon Napa (750 ML)",
        "Vintage_Wine": "Caymus Cabernet Sauvignon Napa (750 ML) 2014",
        "Vintage": "2014",
        "Date": "10/31/2015",
        "Type": "red-cab",
        "LastSeen": "Never",
    },
    {
        "Company": "BevMo",
        "Wine": "Caymus Cabernet Sauvignon Special Select (750 ML)",
        "Vintage_Wine": "Caymus Cabernet Sauvignon Special Select (750 ML) 2014",
        "Vintage": "2014",
        "Date": "10/16/2016",
        "Type": "red-cab",
        "LastSeen": "Never",
    },
    {
        "Company": "BevMo",
        "Wine": "Caymus Cabernet Special Select (750 ML)",
        "Vintage_Wine": "Caymus Cabernet Special Select (750 ML) 2014",
        "Vintage": "2014",
        "Date": "7/23/2015",
        "Type": "red-cab",
        "LastSeen": "Never",
    },
    {
        "Company": "WineClub",
        "Wine": "CAYMUS VINEYARDS CABERNET SAUVIGNON",
        "Vintage_Wine": "CAYMUS VINEYARDS CABERNET SAUVIGNON 2014",
        "Vintage": "2014",
        "Date": "7/15/2018",
        "Type": "red-cab",
        "LastSeen": "Never",
    },
    {
        "Company": "WineClub",
        "Wine": "CAYMUS VINEYARDS SPECIAL SELECTION CABERNET SAUVIGNON",
        "Vintage_Wine": "CAYMUS VINEYARDS SPECIAL SELECTION CABERNET SAUVIGNON 2014",
        "Vintage": "2014",
        "Date": "7/15/2018",
        "Type": "red-cab",
        "LastSeen": "Never",
    },
    {
        "Company": "BevMo",
        "Wine": "Chappellet Cab Sauv Pritchard (750 ML)",
        "Vintage_Wine": "Chappellet Cab Sauv Pritchard (750 ML) 2014",
        "Vintage": "2014",
        "Date": "12/31/2015",
        "Type": "red-cab",
        "LastSeen": "Never",
    },
    {
        "Company": "TotalCA",
        "Wine": "Chappellet Cabernet Sauvignon Napa Signature",
        "Vintage_Wine": "Chappellet Cabernet Sauvignon Napa Signature 2014",
        "Vintage": "2014",
        "Date": "7/2/2013",
        "Type": "red-cab",
        "LastSeen": "2/27/2016",
    },
    {
        "Company": "WineClub",
        "Wine": "CHAPPELLET PRITCHARD HILL CABERNET SAUVIGNON",
        "Vintage_Wine": "CHAPPELLET PRITCHARD HILL CABERNET SAUVIGNON 2014",
        "Vintage": "2014",
        "Date": "7/15/2018",
        "Type": "red-cab",
        "LastSeen": "Never",
    },
    {
        "Company": "WineClub",
        "Wine": "CHAPPELLET SIGNATURE RESERVE CABERNET SAUVIGNON",
        "Vintage_Wine": "CHAPPELLET SIGNATURE RESERVE CABERNET SAUVIGNON 2014",
        "Vintage": "2014",
        "Date": "7/15/2018",
        "Type": "red-cab",
        "LastSeen": "Never",
    },
    {
        "Company": "Vons",
        "Wine": "Charles Krug Cabernet Sauvignon Wine - 750 Ml",
        "Vintage_Wine": "Charles Krug Cabernet Sauvignon Wine 2014 - 750 Ml",
        "Vintage": "2014",
        "Date": "2/21/2009",
        "Type": "red-cab",
        "LastSeen": "2/27/2016",
    },
]

# build up the dictionary data for testing
FLD_DICTKEY = "RecID"

FMT_DICTKEY = "{:03d}"
VAL_DICTKEY_REC1 = FMT_DICTKEY.format(1)

RECORDS_DICT = {}
for reccnt, rec in enumerate(RECORDS, start=1):
    key = FMT_DICTKEY.format(reccnt)
    rec[FLD_DICTKEY] = key
    RECORDS_DICT[key] = rec

REQ_COLS = ["Company", "Wine"]


# Testing class
class TestKVCsv(unittest.TestCase):
    # executed on each test
    def setUp(self):
        kvutil.remove_filename(filename, kvutil.functionName(2), debug=False)

    def tearDown(self):
        kvutil.remove_filename(filename, kvutil.functionName(2), debug=False)

    # executed at the end of all tests - cleans up the environment
    @classmethod
    def tearDownClass(cls):
        kvutil.remove_filename(filename, kvutil.functionName(), debug=False)

    @classmethod
    def setUpClass(cls):
        kvutil.remove_filename(filename, kvutil.functionName(), debug=False)

    # max_column_list
    def test_max_column_list_p01_simple_1_1(self):
        self.assertEqual(
            kvcsv.max_column_list([{"Field1": "value1"}]), ["Field1"]
        )

    def test_max_column_list_p02_simple_1_2(self):
        self.assertEqual(
            kvcsv.max_column_list([{"Field1": "value1", "Field2": "value2"}]),
            ["Field1", "Field2"],
        )

    def test_max_column_list_p03_simple_2_1(self):
        self.assertEqual(
            kvcsv.max_column_list([{"Field1": "value1"}, {"Field2": "value2"}]),
            ["Field1", "Field2"],
        )

    def test_max_column_list_p04_simple_2_mix(self):
        self.assertEqual(
            kvcsv.max_column_list(
                [
                    {"Field1": "value1", "Field2": "value2"},
                    {"Field2": "value2", "Field3": "value3"},
                ]
            ),
            ["Field1", "Field2", "Field3"],
        )

    def test_max_column_list_f01_csvlist_dict(self):
        with self.assertRaises(Exception) as context:
            kvcsv.max_column_list({"a": 1})

    def test_max_column_list_f02_csvlist_list_list(self):
        with self.assertRaises(Exception) as context:
            kvcsv.max_column_list(
                [
                    {"Field1", "value1", "Field2", "value2"},
                    {"Field2", "value2", "Field3", "value3"},
                ]
            )

    # writelist2csv
    def test_writelist2csv_p01_simple(self):
        kvcsv.writelist2csv(filename, RECORDS)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header = kvcsv.readcsv2list_with_header(filename)
        self.assertEqual(RECORDS, results)

    def test_writelist2csv_p02_missing_dict_elements(self):
        templist = copy.deepcopy(RECORDS)
        del templist[0]["Company"]
        del templist[0]["LastSeen"]
        del templist[0]["Type"]
        kvcsv.writelist2csv(filename, templist)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header = kvcsv.readcsv2list_with_header(filename)
        self.assertEqual(list(templist[0].keys()), header)

    def test_writelist2csv_p03_missing_dict_elements_csvfields(self):
        templist = copy.deepcopy(RECORDS)
        csvfields = list(templist[0].keys())
        del templist[0]["Company"]
        del templist[0]["LastSeen"]
        del templist[0]["Type"]
        kvcsv.writelist2csv(filename, templist, csvfields)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header = kvcsv.readcsv2list_with_header(filename)
        self.assertEqual(header, list(RECORDS[0].keys()))

    def test_writelist2csv_p04_missing_dict_elements_maxcolumns(self):
        templist = copy.deepcopy(RECORDS)
        del templist[0]["Company"]
        del templist[0]["LastSeen"]
        del templist[0]["Type"]
        kvcsv.writelist2csv(filename, templist, maxcolumns=True)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header = kvcsv.readcsv2list_with_header(filename)
        # this was manually created and will be adjusted as we change logic
        maxcol_header = [
            "Wine",
            "Vintage_Wine",
            "Vintage",
            "Date",
            "RecID",
            "Company",
            "Type",
            "LastSeen",
        ]
        self.assertEqual(maxcol_header, header)

    def test_writelist2csv_p05_too_many_dict_elements(self):
        templist = copy.deepcopy(RECORDS)
        templist[0]["AddFld1"] = "AddFld1"
        templist[0]["AddFld2"] = "AddFld2"
        kvcsv.writelist2csv(filename, templist)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header = kvcsv.readcsv2list_with_header(filename)
        # this was manually created and will be adjusted as we change logic
        maxcol_header = [
            "Company",
            "Wine",
            "Vintage_Wine",
            "Vintage",
            "Date",
            "Type",
            "LastSeen",
            "RecID",
            "AddFld1",
            "AddFld2",
        ]
        self.assertEqual(maxcol_header, header)

    def test_writelist2csv_p06_more_dict_elements_than_csvfields(self):
        templist = copy.deepcopy(RECORDS)
        csvfields = list(templist[0].keys())
        templist[0]["AddFld1"] = "AddFld1"
        templist[0]["AddFld2"] = "AddFld2"
        kvcsv.writelist2csv(filename, templist, csvfields)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header = kvcsv.readcsv2list_with_header(filename)
        self.assertEqual(csvfields, header)

    def test_writelist2csv_p06_fewer_dict_elements_than_csvfields(self):
        templist = copy.deepcopy(RECORDS)
        csvfields = list(templist[0].keys())
        csvfields.append("AddFld1")
        csvfields.append("AddFld2")
        kvcsv.writelist2csv(filename, templist, csvfields)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header = kvcsv.readcsv2list_with_header(filename)
        self.assertEqual(csvfields, header)

    def test_writelist2csv_p07_dictkeys(self):
        kvcsv.writelist2csv(filename, RECORDS, REQ_COLS)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header = kvcsv.readcsv2list_with_header(filename)
        self.assertEqual(REQ_COLS, header)

    def test_writelist2csv_p08_noheader(self):
        kvcsv.writelist2csv(filename, RECORDS, header=False)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        csvfields = list(RECORDS[0].keys()) + ["RecID"]
        results, header = kvcsv.readcsv2list_with_noheader(
            filename, header=csvfields
        )
        self.assertEqual(csvfields, header)

    def test_writelist2csv_p09_noheader_append(self):
        kvcsv.writelist2csv(filename, RECORDS, header=False)
        kvcsv.writelist2csv(filename, RECORDS, header=False, mode="a")
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        csvfields = list(RECORDS[0].keys()) + ["RecID"]
        results, header = kvcsv.readcsv2list_with_noheader(
            filename, header=csvfields
        )
        self.assertEqual(csvfields, header)
        self.assertEqual(len(results), 2 * len(RECORDS))

    def test_writelist2csv_p10_set_output_cols(self):
        col_aref = ["Wine", "Company", "Vintage"]
        kvcsv.writelist2csv(filename, RECORDS, col_aref=col_aref, debug=False)
        results = kvcsv.readcsv2list(filename)
        match_records = [{x: v[x] for x in col_aref} for v in RECORDS]
        self.assertEqual(results, match_records)

    def test_writelist2csv_f01_empty_csvfile(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writelist2csv("", RECORDS, debug=False)

    def test_writelist2csv_f02_not_list_csvlist(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writelist2csv(filename, RECORDS_DICT, debug=False)

    def test_writelist2csv_f03_not_list_csvlist(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writelist2csv(filename, RECORDS_DICT, debug=False)

    def test_writelist2csv_f04_list_csvlist_rec0_list(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writelist2csv(
                filename, [[1, 2, 3], {"a": 1, "b": 2}], debug=False
            )

    def test_writelist2csv_f05_not_list_csvfields(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writelist2csv(filename, RECORDS, csvfields="ken", debug=False)

    def test_writelist2csv_f06_col_aref_not_list(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writelist2csv(filename, RECORDS, col_aref="ken", debug=False)

    def test_writelist2csv_f07_bad_mode(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writelist2csv(filename, RECORDS, mode=1, debug=False)

    # writedict2csv
    def test_writedict2csv_p01_simple(self):
        kvcsv.writedict2csv(filename, RECORDS_DICT)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, [FLD_DICTKEY]
        )
        self.assertEqual(results, RECORDS_DICT)
        self.assertFalse(dupcount)

    def test_writedict2csv_p02_less_keys_in_key1(self):
        templist = copy.deepcopy(RECORDS_DICT)
        key1 = list(templist.keys())[0]
        del templist[key1]["Company"]
        del templist[key1]["LastSeen"]
        del templist[key1]["Type"]
        csvfields = list(templist[key1].keys())
        kvcsv.writedict2csv(filename, templist)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, [FLD_DICTKEY]
        )
        self.assertEqual(header, csvfields)
        self.assertEqual(len(results), len(RECORDS_DICT))
        self.assertFalse(dupcount)

    def test_writedict2csv_p03_missing_dict_elements_csvfields(self):
        templist = copy.deepcopy(RECORDS_DICT)
        key1 = list(templist.keys())[0]
        csvfields = list(templist[key1].keys())
        del templist[key1]["Company"]
        del templist[key1]["LastSeen"]
        del templist[key1]["Type"]
        kvcsv.writedict2csv(filename, templist, csvfields)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, [FLD_DICTKEY]
        )
        self.assertEqual(header, csvfields)
        self.assertEqual(len(results), len(RECORDS_DICT))
        self.assertFalse(dupcount)

    def test_writedict2csv_p04_missing_dict_elements_maxcolumns(self):
        templist = copy.deepcopy(RECORDS_DICT)
        key1 = list(templist.keys())[0]
        csvfields = list(templist[key1].keys())
        del templist[key1]["Company"]
        del templist[key1]["LastSeen"]
        del templist[key1]["Type"]
        kvcsv.writedict2csv(filename, templist, maxcolumns=True)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        # needed to set this manually due to order difference
        expected_header = [
            "Wine",
            "Vintage_Wine",
            "Vintage",
            "Date",
            "RecID",
            "Company",
            "Type",
            "LastSeen",
        ]
        results, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, [FLD_DICTKEY]
        )
        self.assertEqual(header, expected_header)
        self.assertEqual(len(results), len(RECORDS_DICT))
        self.assertFalse(dupcount)

    def test_writedict2csv_p05_too_many_dict_elements(self):
        templist = copy.deepcopy(RECORDS_DICT)
        key1 = list(templist.keys())[0]
        templist[key1]["AddFld1"] = "AddFld1"
        templist[key1]["AddFld2"] = "AddFld2"
        kvcsv.writedict2csv(filename, templist)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, [FLD_DICTKEY]
        )
        self.assertEqual(header, list(templist[key1].keys()))
        self.assertEqual(len(results), len(RECORDS_DICT))
        self.assertFalse(dupcount)

    def test_writedict2csv_p06_too_many_dict_elements_csvfields(self):
        templist = copy.deepcopy(RECORDS_DICT)
        key1 = list(templist.keys())[0]
        csvfields = list(templist[key1].keys())
        templist[key1]["AddFld1"] = "AddFld1"
        templist[key1]["AddFld2"] = "AddFld2"
        kvcsv.writedict2csv(filename, templist, csvfields)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        results, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, [FLD_DICTKEY]
        )
        self.assertEqual(header, csvfields)
        self.assertEqual(len(results), len(RECORDS_DICT))
        self.assertFalse(dupcount)

    def test_writedict2csv_p07_dictkeys(self):
        kvcsv.writedict2csv(filename, RECORDS_DICT, REQ_COLS)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )

    def test_writedict2csv_p08_noheader(self):
        kvcsv.writedict2csv(filename, RECORDS_DICT, header=False)
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        csvfields = list(RECORDS[0].keys()) + ["RecID"]
        results, header, dupcount = kvcsv.readcsv2dict_with_noheader(
            filename, [FLD_DICTKEY], header=csvfields
        )
        self.assertEqual(csvfields, header)
        self.assertFalse(dupcount)

    def test_writedict2csv_p08_noheader_append(self):
        kvcsv.writedict2csv(filename, RECORDS_DICT, header=False)
        kvcsv.writedict2csv(filename, RECORDS_DICT, header=False, mode="a")
        self.assertTrue(
            os.path.exists(filename), "Did not create filename:" + filename
        )
        csvfields = list(RECORDS[0].keys()) + ["RecID"]
        results, header, dupcount = kvcsv.readcsv2dict_with_noheader(
            filename, [FLD_DICTKEY], header=csvfields
        )
        self.assertEqual(csvfields, header)
        # we will get duplicates because we wrote out the same keys twice
        self.assertTrue(dupcount)
        self.assertEqual(len(results), len(RECORDS_DICT))

    def test_writedict2csv_p10_set_output_cols(self):
        col_aref = ["Wine", "Company", "Vintage"]
        col_aref.append(FLD_DICTKEY)
        kvcsv.writedict2csv(
            filename, RECORDS_DICT, col_aref=col_aref, debug=False
        )
        results, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, [FLD_DICTKEY]
        )
        self.assertEqual(col_aref, header)
        self.assertFalse(dupcount)

    def test_writedict2csv_f01_empty_csvfile(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writedict2csv("", RECORDS, debug=False)

    def test_writedict2csv_f02_not_dict_csvdict(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writedict2csv(filename, RECORDS, debug=False)

    def test_writedict2csv_f04_dict_csvdict_key1_list(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writedict2csv(filename, {"a": [1, 2, 3]}, debug=False)

    def test_writedict2csv_f05_not_list_csvfields(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writedict2csv(
                filename, RECORDS_DICT, csvfields="ken", debug=False
            )

    def test_writedict2csv_f06_col_aref_not_list(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writedict2csv(
                filename, RECORDS_DICT, col_aref="ken", debug=False
            )

    def test_writedict2csv_f07_bad_mode(self):
        with self.assertRaises(Exception) as context:
            kvcsv.writedict2csv(filename, RECORDS_DICT, mode=1, debug=False)

    # readcsv2list_with_header
    def test_readcsv2list_with_header_p01_simple(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result, header = kvcsv.readcsv2list_with_header(filename)
        self.assertEqual(result[0], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))
        self.assertEqual(header, list(RECORDS[0].keys()))

    def test_readcsv2list_with_header_p02_headerlc(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result, header = kvcsv.readcsv2list_with_header(filename, headerlc=True)
        record1lc = {x.lower(): y for x, y in RECORDS[0].items()}
        self.assertEqual(result[0], record1lc)
        self.assertEqual(len(result), len(RECORDS))
        self.assertEqual(header, list(record1lc.keys()))

    def test_readcsv2list_with_header_f01_empty_csvfile(self):
        with self.assertRaises(Exception) as context:
            kvcsv.readcsv2list_with_header("", debug=False)

    # readcsv2list
    def test_readcsv2list_p01_simple(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result = kvcsv.readcsv2list(filename)
        self.assertEqual(result[0], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2list_p02_headerlc(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result = kvcsv.readcsv2list(filename, headerlc=True)
        record1lc = {x.lower(): y for x, y in RECORDS[0].items()}
        self.assertEqual(result[0], record1lc)
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2list_f01_empty_csvfile(self):
        with self.assertRaises(Exception) as context:
            kvcsv.readcsv2list("", debug=False)

    # readcsv2dict_with_header
    def test_readcsv2dict_with_header_p01_simple(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, REQ_COLS
        )
        self.assertEqual(
            result[kvmatch.build_multifield_key(RECORDS[0], REQ_COLS)],
            RECORDS[0],
        )
        self.assertEqual(header, list(RECORDS[0].keys()))
        self.assertEqual(dupcount, 0)

    def test_readcsv2dict_with_header_p02_headerlc(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, REQ_COLS, headerlc=True
        )
        record1lc = {x.lower(): y for x, y in RECORDS[0].items()}
        self.assertEqual(
            result[kvmatch.build_multifield_key(RECORDS[0], REQ_COLS)],
            record1lc,
        )
        self.assertEqual(header, list(record1lc.keys()))
        self.assertEqual(dupcount, 0)

    def test_readcsv2dict_with_header_p03_dup_warning(self):
        duprecords = copy.deepcopy(RECORDS)
        duprecords.append(RECORDS[0])
        kvcsv.writelist2csv(filename, duprecords)
        result, header, dupcount = kvcsv.readcsv2dict_with_header(
            filename, REQ_COLS
        )
        self.assertEqual(
            result[kvmatch.build_multifield_key(RECORDS[0], REQ_COLS)],
            RECORDS[0],
        )
        self.assertEqual(header, list(RECORDS[0].keys()))
        self.assertEqual(dupcount, 1)

    def test_readcsv2dict_with_header_f01_empty_csvfile(self):
        with self.assertRaises(Exception) as context:
            kvcsv.readcsv2dict_with_header("", [FLD_DICTKEY], debug=False)

    def test_readcsv2dict_with_header_f02_empty_dictkeys(self):
        with self.assertRaises(Exception) as context:
            kvcsv.readcsv2dict_with_header(filename, [], debug=False)

    def test_readcsv2dict_with_header_f03_dictkeys_not_list(self):
        with self.assertRaises(Exception) as context:
            kvcsv.readcsv2dict_with_header(filename, {"a": 1}, debug=False)

    def test_readcsv2dict_with_header_f04_dupkeyfail_nowarning(self):
        duprecords = copy.deepcopy(RECORDS)
        duprecords.append(RECORDS[0])
        kvcsv.writelist2csv(filename, duprecords)
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_header(
                filename, REQ_COLS, dupkeyfail=True
            )

    def test_readcsv2dict_with_header_f05_dupkeyfail_warning(self):
        duprecords = copy.deepcopy(RECORDS)
        duprecords.append(RECORDS[0])
        kvcsv.writelist2csv(filename, duprecords)
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_header(
                filename, REQ_COLS, dupkeyfail=True, noshowwarning=True
            )

    # readcsv2dict
    def test_readcsv2dict_p01_simple(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result = kvcsv.readcsv2dict(filename, REQ_COLS)
        self.assertEqual(
            result[kvmatch.build_multifield_key(RECORDS[0], REQ_COLS)],
            RECORDS[0],
        )

    def test_readcsv2dict_p02_headerlc(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result = kvcsv.readcsv2dict(filename, REQ_COLS, headerlc=True)
        record1lc = {x.lower(): y for x, y in RECORDS[0].items()}
        self.assertEqual(
            result[kvmatch.build_multifield_key(RECORDS[0], REQ_COLS)],
            record1lc,
        )

    def test_readcsv2dict_p03_dup_warning(self):
        duprecords = copy.deepcopy(RECORDS)
        duprecords.append(RECORDS[0])
        kvcsv.writelist2csv(filename, duprecords)
        result = kvcsv.readcsv2dict(filename, REQ_COLS)
        self.assertEqual(
            result[kvmatch.build_multifield_key(RECORDS[0], REQ_COLS)],
            RECORDS[0],
        )

    def test_readcsv2dict_f01_dupkeyfail_nowarning(self):
        duprecords = copy.deepcopy(RECORDS)
        duprecords.append(RECORDS[0])
        kvcsv.writelist2csv(filename, duprecords)
        with self.assertRaises(Exception) as context:
            result = kvcsv.readcsv2dict(filename, REQ_COLS, dupkeyfail=True)

    def test_readcsv2dict_f02_dupkeyfail_warning(self):
        duprecords = copy.deepcopy(RECORDS)
        duprecords.append(RECORDS[0])
        kvcsv.writelist2csv(filename, duprecords)
        with self.assertRaises(Exception) as context:
            result = kvcsv.readcsv2dict(
                filename, REQ_COLS, dupkeyfail=True, noshowwarning=True
            )

    # readcsv2dict_with_noheader
    def test_readcsv2dict_with_noheader_p01_simple(self):
        kvcsv.writelist2csv(filename, RECORDS, header=False)
        header = list(RECORDS[0].keys())
        result, header, dupcount = kvcsv.readcsv2dict_with_noheader(
            filename, REQ_COLS, header
        )
        self.assertEqual(
            result[kvmatch.build_multifield_key(RECORDS[0], REQ_COLS)],
            RECORDS[0],
        )
        self.assertEqual(header, list(RECORDS[0].keys()))
        self.assertEqual(dupcount, 0)

    def test_readcsv2dict_with_noheader_p02_dup_warning(self):
        duprecords = copy.deepcopy(RECORDS)
        duprecords.append(RECORDS[0])
        kvcsv.writelist2csv(filename, duprecords, header=False)
        header = list(RECORDS[0].keys())
        result, header, dupcount = kvcsv.readcsv2dict_with_noheader(
            filename, REQ_COLS, header
        )
        self.assertEqual(
            result[kvmatch.build_multifield_key(RECORDS[0], REQ_COLS)],
            RECORDS[0],
        )
        self.assertEqual(header, list(RECORDS[0].keys()))
        self.assertEqual(dupcount, 1)

    def test_readcsv2dict_with_noheader_f01_no_csvfile(self):
        header = list(RECORDS[0].keys())
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_noheader(
                "", REQ_COLS, header
            )

    def test_readcsv2dict_with_noheader_f02_empty_header(self):
        header = list()
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_noheader(
                filename, REQ_COLS, header
            )

    def test_readcsv2dict_with_noheader_f03_header_dict(self):
        header = {"a": 1}
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_noheader(
                fileanem, REQ_COLS, header
            )

    def test_readcsv2dict_with_noheader_f04_dictkeys_empty(self):
        header = list(RECORDS[0].keys())
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_noheader(
                fileanem, [], header
            )

    def test_readcsv2dict_with_noheader_f05_dictkeys_not_list(self):
        header = list(RECORDS[0].keys())
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_noheader(
                fileanem, header, header
            )

    def test_readcsv2dict_with_noheader_f06_dupkeyfail_nowarning(self):
        duprecords = copy.deepcopy(RECORDS)
        duprecords.append(RECORDS[0])
        kvcsv.writelist2csv(filename, duprecords)
        header = list(RECORDS[0].keys())
        with self.assertRaises(Exception) as context:
            result, header, dupcount = kvcsv.readcsv2dict_with_noheader(
                filename, REQ_COLS, header, dupkeyfail=True
            )

    # readcsv2list_findheader
    def test_readcsv2list_findheader_p01_reqcols_simple(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result, header_rtn = kvcsv.readcsv2list_findheader(
            filename, REQ_COLS, debug=False
        )
        self.assertEqual(result[0], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2list_findheader_p02_reqcols_col_header(self):
        # first row is header
        kvcsv.writelist2csv(filename, RECORDS)
        result, header_rtn = kvcsv.readcsv2list_findheader(
            filename, REQ_COLS, optiondict={"col_header": True}, debug=False
        )
        self.assertEqual(result[0], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2list_findheader_p03_reqcols_col_header_col_aref(self):
        # first row is the header, but change the keys of the file to col_aref (which is all upper)
        kvcsv.writelist2csv(filename, RECORDS)
        col_aref = [x.upper() for x in list(RECORDS[0].keys())]
        result, header_rtn = kvcsv.readcsv2list_findheader(
            filename,
            REQ_COLS,
            optiondict={"col_header": True},
            col_aref=col_aref,
            debug=False,
        )

        self.assertEqual(
            result[0], {x.upper(): y for x, y in RECORDS[0].items()}
        )
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2list_findheader_p04_reqcols_save_row(self):
        # add a new key for save_row that is the record number
        kvcsv.writelist2csv(filename, RECORDS)
        result, header_rtn = kvcsv.readcsv2list_findheader(
            filename, REQ_COLS, optiondict={"save_row": True}, debug=False
        )
        self.assertEqual(result[0]["XLSRow"], 2)
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2list_findheader_p06_reqcols_no_header_col_aref(self):
        # no headers so what is the header in this file is just record #1
        # we then do the compares on record 2
        kvcsv.writelist2csv(filename, RECORDS)
        result, header_rtn = kvcsv.readcsv2list_findheader(
            filename,
            REQ_COLS,
            col_aref=list(RECORDS[0].keys()),
            optiondict={"no_header": True},
            debug=False,
        )
        self.assertEqual(result[1], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS) + 1)

    def test_readcsv2list_findheader_p07_reqcols_header_deep_not_1stline(self):
        blankrec = {x: "" for x in RECORDS[0].keys()}
        headerrec = {x: x for x in RECORDS[0].keys()}
        # put out a bunch of blank lines in the file so we are not starting at the top of the file
        aref = []
        for i in range(5):
            aref.append(blankrec)
        # add the header row
        aref.append(headerrec)
        # add all the other data records
        aref.extend(RECORDS)
        # write this out with header as false
        kvcsv.writelist2csv(
            filename, aref, list(RECORDS[0].keys()), header=False
        )
        # now load this finding the header line that is not at the top
        result, header_rtn = kvcsv.readcsv2list_findheader(
            filename, REQ_COLS, debug=False
        )
        self.assertEqual(result[0], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2list_findheader_p08_reqcols_header_deep_start_row(self):
        blankrec = {x: "" for x in RECORDS[0].keys()}
        headerrec = {x: x for x in RECORDS[0].keys()}
        aref = []
        for i in range(5):
            aref.append(blankrec)
        aref.append(headerrec)
        aref.extend(RECORDS)
        kvcsv.writelist2csv(
            filename, aref, list(RECORDS[0].keys()), header=False
        )

        result, header_rtn = kvcsv.readcsv2list_findheader(
            filename, REQ_COLS, optiondict={"start_row": 2}, debug=False
        )
        self.assertEqual(result[0], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2list_findheader_p09_reqcols_header_deep_aref_result(self):
        blankrec = {x: "" for x in RECORDS[0].keys()}
        headerrec = {x: x for x in RECORDS[0].keys()}
        aref = []
        for i in range(5):
            aref.append(blankrec)
        aref.append(headerrec)
        aref.extend(RECORDS)
        kvcsv.writelist2csv(
            filename, aref, list(RECORDS[0].keys()), header=False
        )

        result, header_rtn = kvcsv.readcsv2list_findheader(
            filename, REQ_COLS, optiondict={"aref_result": True}, debug=False
        )
        self.assertEqual(result[0], list(RECORDS[0].values()))
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2list_findheader_p10_reqcols_xlat(self):
        kvcsv.writelist2csv(filename, RECORDS)
        # we want out putput results to have WineVendor (not company) and WineLabel (not Wine)
        xlatdict = {
            "Company": "WineVendor",
            "Wine": "WineLabel",
        }
        # define the new requjired columns based on the output we want not the input we process
        req_cols_local = [xlatdict.get(x, x) for x in REQ_COLS]
        # and this shiould be the resulting header we get back
        header_chg = [xlatdict.get(x, x) for x in RECORDS[0].keys()]
        result, header_rtn = kvcsv.readcsv2list_findheader(
            filename, req_cols_local, xlatdict=xlatdict, debug=False
        )
        self.assertEqual(header_chg, header_rtn)

    # readcsv2dict_findheader
    def test_readcsv2dict_findheader_p01_reqcols_simple(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result, header_rtn, dupcount = kvcsv.readcsv2dict_findheader(
            filename, REQ_COLS, [FLD_DICTKEY], debug=False
        )
        self.assertEqual(result[VAL_DICTKEY_REC1], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2dict_findheader_p02_reqcols_col_header(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result, header_rtn, dupcount = kvcsv.readcsv2dict_findheader(
            filename,
            REQ_COLS,
            [FLD_DICTKEY],
            optiondict={"col_header": True},
            debug=False,
        )
        self.assertEqual(result[VAL_DICTKEY_REC1], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2dict_findheader_p03_reqcols_col_header_col_aref(self):
        kvcsv.writelist2csv(filename, RECORDS)
        col_aref = [x.upper() for x in list(RECORDS[0].keys())]
        upper_fld_dictkey = FLD_DICTKEY.upper()
        result, header_rtn, dupcount = kvcsv.readcsv2dict_findheader(
            filename,
            REQ_COLS,
            [upper_fld_dictkey],
            optiondict={"col_header": True},
            col_aref=col_aref,
            debug=False,
        )

        self.assertEqual(
            result[VAL_DICTKEY_REC1],
            {x.upper(): y for x, y in RECORDS[0].items()},
        )
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2dict_findheader_p04_reqcols_save_row(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result, header_rtn, dupcount = kvcsv.readcsv2dict_findheader(
            filename,
            REQ_COLS,
            [FLD_DICTKEY],
            optiondict={"save_row": True},
            debug=False,
        )
        self.assertEqual(result[VAL_DICTKEY_REC1]["XLSRow"], 2)
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2dict_findheader_f05_reqcols_no_header(self):
        kvcsv.writelist2csv(filename, RECORDS)
        with self.assertRaises(Exception) as context:
            result, header_rtn, dupcount = kvcsv.readcsv2dict_findheader(
                filename,
                REQ_COLS,
                [FLD_DICTKEY],
                optiondict={"no_header": True},
                debug=False,
            )

    def test_readcsv2dict_findheader_p06_reqcols_no_header_col_aref(self):
        kvcsv.writelist2csv(filename, RECORDS)
        result, header_rtn, dupcount = kvcsv.readcsv2dict_findheader(
            filename,
            REQ_COLS,
            [FLD_DICTKEY],
            col_aref=list(RECORDS[0].keys()),
            optiondict={"no_header": True},
            debug=False,
        )
        self.assertEqual(result[VAL_DICTKEY_REC1], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS) + 1)

    def test_readcsv2dict_findheader_p07_reqcols_header_deep(self):
        blankrec = {x: "" for x in RECORDS[0].keys()}
        headerrec = {x: x for x in RECORDS[0].keys()}
        aref = []
        for i in range(5):
            aref.append(blankrec)
        aref.append(headerrec)
        aref.extend(RECORDS)
        kvcsv.writelist2csv(
            filename, aref, list(RECORDS[0].keys()), header=False
        )
        result, header_rtn, dupcount = kvcsv.readcsv2dict_findheader(
            filename, REQ_COLS, [FLD_DICTKEY], debug=False
        )
        self.assertEqual(result[VAL_DICTKEY_REC1], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2dict_findheader_p08_reqcols_header_deep_start_row(self):
        blankrec = {x: "" for x in RECORDS[0].keys()}
        headerrec = {x: x for x in RECORDS[0].keys()}
        aref = []
        for i in range(5):
            aref.append(blankrec)
        aref.append(headerrec)
        aref.extend(RECORDS)
        kvcsv.writelist2csv(
            filename, aref, list(RECORDS[0].keys()), header=False
        )

        result, header_rtn, dupcount = kvcsv.readcsv2dict_findheader(
            filename,
            REQ_COLS,
            [FLD_DICTKEY],
            optiondict={"start_row": 2},
            debug=False,
        )
        self.assertEqual(result[VAL_DICTKEY_REC1], RECORDS[0])
        self.assertEqual(len(result), len(RECORDS))

    def test_readcsv2dict_findheader_f09_reqcols_header_deep_aref_result(self):
        blankrec = {x: "" for x in RECORDS[0].keys()}
        headerrec = {x: x for x in RECORDS[0].keys()}
        aref = []
        for i in range(5):
            aref.append(blankrec)
        aref.append(headerrec)
        aref.extend(RECORDS)
        kvcsv.writelist2csv(
            filename, aref, list(RECORDS[0].keys()), header=False
        )
        with self.assertRaises(Exception) as context:
            result, header_rtn, dupcount = kvcsv.readcsv2dict_findheader(
                filename,
                REQ_COLS,
                [FLD_DICTKEY],
                optiondict={"aref_result": True},
                debug=False,
            )


if __name__ == "__main__":
    unittest.main()
# eof
