import pytest
import kvxls
import os

test_file = 't_kvxls_unit.xlsx'

def remove_file():
    if os.path.exists(test_file):
        os.remove(test_file)

# writelist2xls Not Populated
def test_writelist2xls_p01_data_empty_list():
    remove_file()
    res = kvxls.writelist2xls(test_file, [])
    assert os.path.exists(test_file)
    remove_file()

def test_writelist2xls_p02_data_none():
    remove_file()
    res = kvxls.writelist2xls(test_file, None)
    assert os.path.exists(test_file)
    remove_file()

# writedict2xls Not Populated
def test_writelist2dict_p01_data_empty_dict():
    remove_file()
    res = kvxls.writedict2xls(test_file, {})
    assert os.path.exists(test_file)
    remove_file()

def test_writelist2dict_p02_data_none():
    remove_file()
    res = kvxls.writedict2xls(test_file, None)
    assert os.path.exists(test_file)
    remove_file()

def test_writelist2dict_f01_data_list():
    with pytest.raises(Exception):
        remove_file()
        res = kvxls.writedict2xls(test_file, ['list'])
        assert os.path.exists(test_file)
        remove_file()

