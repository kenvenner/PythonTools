# import pytest
import kvargs
import json
import os


def test_merge_settings_p01_conf_in_conf():
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

    assert vargs == finalconf

    os.unlink(conf)
    os.unlink(conf1['conf'])


def test_merge_settings_p02_args_dict():
    vargs=kvargs.merge_settings({})
    assert vargs == {}

def test_merge_settings_p03_set_defaults_all():
    default_args = {
        'arg1': 'arg1',
        'arg2': 'arg2',
    }
    vargs=kvargs.merge_settings({}, args_default=default_args)
    assert vargs == default_args

def test_merge_settings_p04_set_defaults_some():
    default_args = {
        'arg1': 'arg1',
        'arg2': 'arg2',
    }
    vargs=kvargs.merge_settings({'arg1': 'not_default'}, args_default=default_args)
    default_args['arg1'] = 'not_default'
    assert vargs == default_args

def test_missing_settings_p01_none_missing():
    args = {
        'arg1': 'arg1',
        'arg2': 'arg2',
    }
    assert kvargs.missing_settings(args, ['arg1']) == []

def test_missing_settings_p02_one_missing():
    args = {
        'arg1': 'arg1',
        'arg2': 'arg2',
    }
    assert kvargs.missing_settings(args, ['arg3']) == ['arg3']

def test_missing_settings_p03_two_missing():
    args = {
        'arg1': 'arg1',
        'arg2': 'arg2',
    }
    assert kvargs.missing_settings(args, ['arg3', 'arg4']) == ['arg3', 'arg4']
