# import pytest
import kvargs
import json
import os


def test_merge_settings_conf_in_conf():
    conf='kvargs1.json'
    args_default = {
        'setting1': 'start1',
        'setting2': 'start2',
    }
    args = {
        'setting1': '',
        'setting2': '',
        'setting3': 'start3',
    }
    conf1 = {
        'setting1': 'middle1',
        'conf': 'kvargs2.json',
    }
    conf2 = {
        'setting2': 'middle2',
        'setting3': 'middle3',
    }
    finalconf = {
        'setting3': 'start3',
        'setting1': 'middle1',
        'conf': 'kvargs2.json',
        'setting2': 'middle2',
        'conf_files_loaded': ['kvargs1.json', 'kvargs2.json'],
    }
    with open(conf, 'w') as f:
        json.dump(conf1, f)
    with open(conf1['conf'], 'w') as f:
        json.dump(conf2, f)
    vargs=kvargs.merge_settings(args, conf, args_default)

    os.unlink(conf)
    os.unlink(conf1['conf'])
    assert vargs == finalconf
