import pytest
import kvargs
import json
import os
import argparse
import copy
import sys
from attrdict import AttrDict

conf = 'kvargs1.json'
args_default = {
    'setting1': 'start1',
    'setting2': 'start2',
}
conf1 = {
    'setting1': 'middle1',
    'conf': 'kvargs2.json',
}
conf2 = {
    'setting2': 'middle2',
    'setting3': 'middle3',
}


#
def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    parser.add_argument("--disp_vargs", action="store_true")
    parser.add_argument("--console", action="store_true", dest="display")
    parser.add_argument("--no_console", action="store_false", dest="display")
    parser.add_argument("--url", dest="uri", default="http")
    parser.add_argument("--conf")
    return parser


def write_conf(filename, conf_dict):
    with open(filename, 'w') as f:
        json.dump(conf_dict, f, indent=4)


# ----------------------------------------

def test_load_json_file_to_dict_p01_simple():
    with open(conf, 'w') as f:
        json.dump(conf2, f)

    vargs = kvargs.load_json_file_to_dict(conf)

    assert vargs == conf2

    os.unlink(conf)


# ----------------------------------------

def test_conf_settings_p01_conf_in_conf():
    finalconf = {
        'setting1': 'middle1',
        'setting2': 'middle2',
        'setting3': 'middle3',
        'conf': 'kvargs2.json',
        'conf_files_loaded': ['kvargs1.json', 'kvargs2.json'],
    }

    with open(conf, 'w') as f:
        json.dump(conf1, f)
    with open(conf1['conf'], 'w') as f:
        json.dump(conf2, f)

    vargs, conf_loaded, vargs_updated_by = kvargs.conf_settings(conf)

    assert dict(vargs) == finalconf
    assert conf_loaded == finalconf['conf_files_loaded']
    assert vargs_updated_by == {
        'conf': ['conf:kvargs1.json'],
        'setting1': ['conf:kvargs1.json'],
        'setting2': ['conf:kvargs2.json'],
        'setting3': ['conf:kvargs2.json'],
    }

    os.unlink(conf)
    os.unlink(conf1['conf'])


def test_conf_settings_p02_conf_in_conf_overlap():
    finalconf = {
        'setting1': 'middle1',
        'setting2': 'middle2',
        'setting3': 'middle3',
        'conf': 'kvargs2.json',
        'conf_files_loaded': ['kvargs1.json', 'kvargs2.json'],
    }

    conf1a = copy.deepcopy(conf1)
    conf1a['setting2'] = 'start2'

    with open(conf, 'w') as f:
        json.dump(conf1a, f)
    with open(conf1['conf'], 'w') as f:
        json.dump(conf2, f)

    vargs, conf_loaded, vargs_updated_by = kvargs.conf_settings(conf)

    assert vargs == finalconf
    assert conf_loaded == finalconf['conf_files_loaded']
    assert vargs_updated_by == {
        'conf': ['conf:kvargs1.json'],
        'setting1': ['conf:kvargs1.json'],
        'setting2': ['conf:kvargs1.json', 'conf:kvargs2.json'],
        'setting3': ['conf:kvargs2.json'],
    }

    os.unlink(conf)
    os.unlink(conf1['conf'])


def test_conf_settings_p03_conf_in_conf_overlap_conf():
    finalconf = {
        'setting1': 'middle1',
        'setting2': 'middle2',
        'setting3': 'middle3',
        'conf': 'kvargs2.json',
        'conf_files_loaded': ['kvargs1.json', 'kvargs2.json'],
    }

    conf2a = copy.deepcopy(conf2)
    conf2a['conf'] = conf
    finalconf['conf'] = conf

    with open(conf, 'w') as f:
        json.dump(conf1, f)
    with open(conf1['conf'], 'w') as f:
        json.dump(conf2a, f)

    vargs, conf_loaded, vargs_updated_by = kvargs.conf_settings(conf)

    assert dict(vargs) == finalconf
    assert conf_loaded == finalconf['conf_files_loaded']
    assert vargs_updated_by == {
        'conf': ['conf:kvargs1.json', 'conf:kvargs2.json'],
        'setting1': ['conf:kvargs1.json'],
        'setting2': ['conf:kvargs2.json'],
        'setting3': ['conf:kvargs2.json'],
    }

    os.unlink(conf)
    os.unlink(conf1['conf'])


# ----------------------------------------

def test_merge_settings_p01_conf_in_conf():
    args = {
        'setting1': None,
        'setting2': None,
        'setting3': 'start3',
    }
    finalconf = {
        'setting1': 'middle1',
        'setting2': 'middle2',
        'setting3': 'start3',
        'conf': 'kvargs2.json',
        'conf_files_loaded': ['kvargs1.json', 'kvargs2.json'],
    }

    with open(conf, 'w') as f:
        json.dump(conf1, f)
    with open(conf1['conf'], 'w') as f:
        json.dump(conf2, f)

    vargs = kvargs.merge_settings(args, conf, args_default)

    assert vargs == finalconf

    os.unlink(conf)
    os.unlink(conf1['conf'])


def test_merge_settings_p02_set_by_default_no_conf():
    args = {
        'setting1': None,
        'setting2': None,
        'setting3': 'start3',
    }
    finalconf = {
        'setting1': 'start1',
        'setting2': 'start2',
        'setting3': 'start3',
    }

    vargs = kvargs.merge_settings(args, '', args_default)

    assert dict(vargs) == finalconf


def test_merge_settings_p03_set_by_default_no_conf_no_value():
    args = {
        'setting3': 'start3',
    }
    finalconf = {
        'setting1': 'start1',
        'setting2': 'start2',
        'setting3': 'start3',
    }

    vargs = kvargs.merge_settings(args, '', args_default)

    assert dict(vargs) == finalconf


def test_merge_settings_p04_set_by_default_no_conf_blank_value():
    args = {
        'setting1': '',
        'setting3': 'start3',
    }
    finalconf = {
        'setting1': '',
        'setting2': 'start2',
        'setting3': 'start3',
    }

    vargs = kvargs.merge_settings(args, '', args_default)

    assert vargs == finalconf


def test_merge_settings_p04_all_set_cmd_line():
    args = {
        'setting1': 'cmd1',
        'setting2': 'cmd2',
        'setting3': 'cmd3',
    }
    finalconf = args
    finalconf['conf_files_loaded'] = []

    vargs = kvargs.merge_settings(args, '', args_default)

    assert vargs == finalconf


def test_merge_settings_p02_args_dict():
    vargs = kvargs.merge_settings({})
    assert vargs == {}


def test_merge_settings_p03_set_defaults_all():
    default_args = {
        'arg1': 'arg1',
        'arg2': 'arg2',
    }
    vargs = kvargs.merge_settings({}, args_default=default_args)
    assert vargs == default_args


def test_merge_settings_p04_set_defaults_some():
    default_args = {
        'arg1': 'arg1',
        'arg2': 'arg2',
    }
    vargs = kvargs.merge_settings({'arg1': 'not_default'}, args_default=default_args)
    default_args['arg1'] = 'not_default'
    assert vargs == default_args


# ----------------------------------------

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


# ----------------------------------------

def test_parser_extract_default_and_set_to_none_p01_simple_default():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default="ken")
    assert parser.get_default("token") == "ken"

    ad = kvargs.parser_extract_default_and_set_to_none(parser)
    assert ad == {'token': 'ken'}
    assert parser.get_default("token") is None


def test_parser_extract_default_and_set_to_none_p02_simple_no_default():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    assert parser.get_default("token") is None

    ad = kvargs.parser_extract_default_and_set_to_none(parser)
    assert ad == {}
    assert parser.get_default("token") is None


def test_parser_extract_default_and_set_to_none_p03_true_toggle():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action='store_true')
    assert not parser.get_default("token")

    ad = kvargs.parser_extract_default_and_set_to_none(parser)
    assert ad == {'token': False}
    assert parser.get_default("token") is None


def test_parser_extract_default_and_set_to_none_p04_false_toggle():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action='store_false')
    assert parser.get_default("token")

    ad = kvargs.parser_extract_default_and_set_to_none(parser)
    assert ad == {'token': True}
    assert parser.get_default("token") is None


def test_parser_extract_default_and_set_to_none_p05_true_toggle_set_true():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action='store_true', default=True)
    assert parser.get_default("token") is True

    ad = kvargs.parser_extract_default_and_set_to_none(parser)
    assert ad == {'token': True}
    assert parser.get_default("token") is None


def test_parser_extract_default_and_set_to_none_p06_set_true_two_same_dest():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action='store_true', dest="ken")
    parser.add_argument("--no_token", action='store_false', dest="ken")
    assert parser.get_default("ken") is False

    ad = kvargs.parser_extract_default_and_set_to_none(parser)
    assert ad == {'ken': False}
    assert parser.get_default("ken") is None


def test_parser_extract_default_and_set_to_none_p07_set_true_two_same_dest_with_default():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action='store_true', dest="ken")
    parser.add_argument("--no_token", action='store_false', dest="ken")
    assert parser.get_default("ken") is False

    ad = kvargs.parser_extract_default_and_set_to_none(parser, {'ken': True})
    assert ad == {'ken': True}
    assert parser.get_default("ken") is None


def test_parser_extract_default_and_set_to_none_p08_set_true_two_same_dest_with_default():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action='store_true', dest="ken")
    parser.add_argument("--no_token", action='store_false', dest="ken")
    assert parser.get_default("ken") is False

    ad = kvargs.parser_extract_default_and_set_to_none(parser, {'ken': 'sue'})
    assert ad == {'ken': 'sue'}
    assert parser.get_default("ken") is None


def test_parser_extract_default_and_set_to_none_p09_true_toggle_default_true():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action='store_true')
    assert parser.get_default("token") is False

    ad = kvargs.parser_extract_default_and_set_to_none(parser, {'token': True})
    assert ad == {'token': True}
    assert parser.get_default("token") is None


# ----------------------------------------

def test_parser_defaults_p01_pass():
    parser = setup_parser()

    args_parser_default = kvargs.parser_defaults(parser)
    assert args_parser_default == {
        'console': {
            'cmd': '--console',
            'const': True,
            'dest': 'display',
            'first': True,
            'value': False
        },
        'disp_vargs': {
            'cmd': '--disp_vargs',
            'const': True,
            'dest': 'disp_vargs',
            'first': True,
            'value': False
        },
        'no_console': {
            'cmd': '--no_console',
            'const': True,
            'dest': 'display',
            'first': False,
            'value': False
        },
        'url': {
            'cmd': '--url',
            'const': False,
            'dest': 'uri',
            'first': True,
            'value': 'http'},
    }


def test_parser_defaults_p02_pass():
    parser = setup_parser()

    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    assert args_parser_default == {
        'console': {
            'cmd': '--console',
            'const': True,
            'dest': 'display',
            'first': True,
            'value': False
        },
        'disp_vargs': {
            'cmd': '--disp_vargs',
            'const': True,
            'dest': 'disp_vargs',
            'first': True,
            'value': False
        },
        'no_console': {
            'cmd': '--no_console',
            'const': True,
            'dest': 'display',
            'first': False,
            'value': False
        },
        'url': {
            'cmd': '--url',
            'const': False,
            'dest': 'uri',
            'first': True,
            'value': 'http'},
    }


def test_parser_defaults_p03_pass():
    parser = setup_parser()

    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    assert args_parser_default == {}


# ----------------------------------------

# the function name: def updated_by(updated_dict, key, value):
def test_updated_by_p01_simple_dict_key_exist_value():
    updated_dict = {'key': ['value']}
    kvargs.updated_by(updated_dict, 'key', 'value2')
    assert updated_dict == {'key': ['value', 'value2']}

def test_updated_by_p02_simple_dict_key_exist_list():
    updated_dict = {'key': ['value']}
    kvargs.updated_by(updated_dict, 'key', ['value2', 'value3'])
    assert updated_dict == {'key': ['value', 'value2', 'value3']}

def test_updated_by_p03_simple_dict_key_not_exist_value():
    updated_dict = {}
    kvargs.updated_by(updated_dict, 'key', 'value2')
    assert updated_dict == {'key': ['value2']}

def test_updated_by_p04_simple_dict_key_not_exist_list():
    updated_dict = {}
    kvargs.updated_by(updated_dict, 'key', ['value2', 'value3'])
    assert updated_dict == {'key': ['value2', 'value3']}

def test_updated_by_f01_simple_not_dict():
    updated_dict = 'string'
    with pytest.raises(Exception):
        kvargs.updated_by(updated_dict, 'key', ['value2', 'value3'])


# ----------------------------------------
# the function name: def parser_merge_settings(parser, args, conf_files=None, args_default=None, args_parser_default=None,
def test_parser_merge_settings_p01_pass():
    parser = setup_parser()
    cmd_line = []

    args = parser.parse_args(cmd_line)
    vargs = vars(args)


# ----------------------------------------


def test_parse_and_parser_merge_settings_p01_blank_cmdline_no_parse():
    parser = setup_parser()
    cmd_line = []

    args = parser.parse_args(cmd_line)
    vargs = vars(args)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': None,
        'uri': 'http'
    }


def test_parse_and_parser_merge_settings_p02_blank_cmdline_parsed():
    parser = setup_parser()
    cmd_line = []
    args_default = {}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': None,
        'uri': 'http',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default'],
            'uri': ['args_parser_default']
        },
    }


def test_parse_and_parser_merge_settings_p03_blank_cmdline_parsed_arg_default_flag():
    parser = setup_parser()
    cmd_line = []
    args_default = {'disp_vargs': True}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': True,
        'display': False,
        'token': None,
        'uri': 'http',
        'vargs_updated_by': {
            'disp_vargs': ['args_default'],
            'display': ['args_parser_default'],
            'uri': ['args_parser_default']
        },
    }


def test_parse_and_parser_merge_settings_p04_blank_cmdline_parsed_arg_default_flag_false():
    parser = setup_parser()
    cmd_line = []
    args_default = {'disp_vargs': False}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': None,
        'uri': 'http',
        'vargs_updated_by': {
            'disp_vargs': ['args_default'],
            'display': ['args_parser_default'],
            'uri': ['args_parser_default']
        },
    }


def test_parse_and_parser_merge_settings_p04_blank_cmdline_parsed_arg_default_flag_dest_true():
    parser = setup_parser()
    cmd_line = []
    args_default = {'display': True}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': True,
        'token': None,
        'uri': 'http',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_default'],
            'uri': ['args_parser_default']
        },
    }


def test_parse_and_parser_merge_settings_p05_blank_cmdline_parsed_arg_default_str():
    parser = setup_parser()
    cmd_line = []
    args_default = {'token': 'default_token'}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': 'default_token',
        'uri': 'http',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default'],
            'token': ['args_default'],
            'uri': ['args_parser_default']
        },
    }


def test_parse_and_parser_merge_settings_p06_blank_cmdline_parsed_arg_default_str_blank():
    parser = setup_parser()
    cmd_line = []
    args_default = {'token': 'default_token', 'uri': ''}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': 'default_token',
        'uri': '',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default'],
            'token': ['args_default'],
            'uri': ['args_default']
        },
    }


def test_parse_and_parser_merge_settings_p06_blank_cmdline_parsed_arg_default_str_blank_dest():
    parser = setup_parser()
    cmd_line = []
    args_default = {'token': 'default_token', 'uri': ''}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': 'default_token',
        'uri': '',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default'],
            'token': ['args_default'],
            'uri': ['args_default']
        },
    }


def test_parse_and_parser_merge_settings_p06_blank_cmdline_parsed_arg_default_str_blank_cmd():
    parser = setup_parser()
    cmd_line = []
    args_default = {'token': 'default_token', 'url': ''}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    # url is added because we are not making cmdline expansions
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': 'default_token',
        'uri': 'http',
        'url': '',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default'],
            'token': ['args_default'],
            'uri': ['args_parser_default'],
            'url': ['args_default']},
    }


def test_parse_and_parser_merge_settings_p07_blank_cmdline_parsed_arg_default_new_value():
    parser = setup_parser()
    cmd_line = []
    args_default = {'new_value': 'new_value'}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': None,
        'uri': 'http',
        'new_value': 'new_value',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default'],
            'new_value': ['args_default'],
            'uri': ['args_parser_default']
        },
    }


# ----------------------------------------

def test_parse_and_parser_merge_settings_p01_cmdline_v1_parsed():
    parser = setup_parser()
    cmd_line = ['--disp_vargs']
    args_default = {}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': True,
        'display': False,
        'token': None,
        'uri': 'http',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default',
                           'cmdline'],
            'display': ['args_parser_default'],
            'uri': ['args_parser_default']
        },
    }


def test_parse_and_parser_merge_settings_p02_cmdline_v2_parsed():
    parser = setup_parser()
    cmd_line = ['--console']
    args_default = {}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': True,
        'token': None,
        'uri': 'http',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default',
                        'cmdline'],
            'uri': ['args_parser_default']
        },
    }


def test_parse_and_parser_merge_settings_p03_cmdline_v3_parsed():
    parser = setup_parser()
    cmd_line = ['--no_console']
    args_default = {}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': None,
        'uri': 'http',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default',
                        'cmdline'],
            'uri': ['args_parser_default']
        },

    }


def test_parse_and_parser_merge_settings_p04_cmdline_v4_parsed():
    parser = setup_parser()
    cmd_line = ['--token', 'cmdline_token']
    args_default = {}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'conf': None,
        'disp_vargs': False,
        'display': False,
        'token': 'cmdline_token',
        'uri': 'http',
        'vargs_updated_by': {
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default'],
            'token': ['cmdline'],
            'uri': ['args_parser_default']
        },
    }


# ----------------------------------------


def test_ken():
    parser = setup_parser()
    write_conf(conf, {'disp_vargs': True})
    cmd_line = ['--conf', 'kvargs1.json']
    parser.parse_args(cmd_line)


def test_parse_and_parser_merge_settings_p02_conf_cmdline_parsed():
    parser = setup_parser()
    write_conf(conf, {'disp_vargs': True})
    cmd_line = ['--conf', conf]
    args_default = {}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    # just clear sys.argv in order to test properly
    orig_sysargv = sys.argv
    sys.argv = ['pytest']
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    # and return it back to its original value
    sys.argv = orig_sysargv
    assert dict(vargs) == {
        'conf': conf,
        'conf_files_loaded': [conf],
        'disp_vargs': True,
        'display': False,
        'token': None,
        'uri': 'http',
        'vargs_updated_by': {
            'conf': ['cmdline'],
            'disp_vargs': ['args_parser_default',
                           'conf:kvargs1.json'],
            'display': ['args_parser_default'],
            'uri': ['args_parser_default']
        },
    }
    os.remove(conf)


def test_parse_and_parser_merge_settings_p03_conf_cmdline_parsed():
    parser = setup_parser()
    write_conf(conf, {'disp_vargs': True, 'url': 'https://conf_set'})
    cmd_line = ['--conf', conf]
    args_default = {}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    # just clear sys.argv in order to test properly
    orig_sysargv = sys.argv
    sys.argv = ['pytest']
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    # and return it back to its original value
    sys.argv = orig_sysargv
    assert vargs == {
        'conf': conf,
        'conf_files_loaded': ['kvargs1.json'],
        'disp_vargs': True,
        'display': False,
        'token': None,
        'uri': 'https://conf_set',
        'vargs_updated_by': {
            'conf': ['cmdline'],
            'disp_vargs': ['args_parser_default',
                           'conf:kvargs1.json'],
            'display': ['args_parser_default'],
            'uri': ['args_parser_default',
                    'conf:kvargs1.json']
        },
    }
    os.remove(conf)


def test_parse_and_parser_merge_settings_p04_conf_cmdline_parsed():
    parser = setup_parser()
    write_conf(conf, {'no_console': True, 'url': 'https://conf_set'})
    cmd_line = ['--conf', conf]
    args_default = {}
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    print('args_parser_default:', args_parser_default)
    # just clear sys.argv in order to test properly
    orig_sysargv = sys.argv
    sys.argv = ['pytest']
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    # return to its original value
    sys.argv = orig_sysargv
    assert vargs == {
        'conf': conf,
        'conf_files_loaded': ['kvargs1.json'],
        'disp_vargs': False,
        'display': False,
        'token': None,
        'uri': 'https://conf_set',
        'vargs_updated_by': {
            'conf': ['cmdline'],
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default', 'conf:kvargs1.json'],
            'uri': ['args_parser_default', 'conf:kvargs1.json']
        },
    }

    print('*' * 80)

    cmd_line = ['--conf', conf, '--console']
    # just clear sys.argv in order to test properly
    orig_sysargv = sys.argv
    sys.argv = ['pytest']
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    # return to its original value
    sys.argv = orig_sysargv
    assert dict(vargs) == {
        'conf': conf,
        'conf_files_loaded': ['kvargs1.json'],
        'disp_vargs': False,
        'display': True,
        'token': None,
        'uri': 'https://conf_set',
        'vargs_updated_by': {
            'conf': ['cmdline'],
            'disp_vargs': ['args_parser_default'],
            'display': ['args_parser_default',
                        'conf:kvargs1.json',
                        'cmdline'],
            'uri': ['args_parser_default',
                    'conf:kvargs1.json']
        },
    }

    os.remove(conf)


# ----------------------------------------

def test_parse_and_parser_merge_settings_p01_str_simple():
    cmd_line = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default="ken")
    assert parser.get_default("token") == "ken"

    args_default = kvargs.parser_extract_default_and_set_to_none(parser)
    assert args_default == {'token': 'ken'}
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert dict(vargs) == {'token': 'ken', 'vargs_updated_by': {'token': ['args_default']}}
    assert parser.get_default("token") is None


def test_parse_and_parser_merge_settings_p02_str_set_cmd():
    cmd_line = ['--token', 'sue']
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default="ken")
    assert parser.get_default("token") == "ken"

    args_default = kvargs.parser_extract_default_and_set_to_none(parser)
    assert args_default == {'token': 'ken'}
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'token': 'sue',
        'vargs_updated_by': {
            'token': ['args_default',
                      'cmdline']
        },
    }
    assert parser.get_default("token") is None


def test_parse_and_parser_merge_settings_p03_store_true_simple():
    cmd_line = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action="store_true")
    assert parser.get_default("token") is False

    args_default = kvargs.parser_extract_default_and_set_to_none(parser)
    assert args_default == {
        'token': False,
    }
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert dict(vargs) == {
        'token': False,
        'vargs_updated_by': {
            'token': ['args_default']
        }
    }
    assert parser.get_default("token") is None


def test_parse_and_parser_merge_settings_p04_store_true_set_cmd():
    cmd_line = ['--token']
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action="store_true")
    assert parser.get_default("token") is False

    args_default = kvargs.parser_extract_default_and_set_to_none(parser)
    assert args_default == {'token': False}
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'token': True,
        'vargs_updated_by': {
            'token': ['args_default',
                      'cmdline']
        },
    }
    assert parser.get_default("token") is None


def test_parse_and_parser_merge_settings_p05_two_flags():
    # cmd_line = ['--token']
    cmd_line = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action="store_true")
    parser.add_argument("--no_token", action="store_false", dest="token")
    assert parser.get_default("token") is False

    args_default = kvargs.parser_extract_default_and_set_to_none(parser, {'token': True})
    assert args_default == {'token': True}
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'token': True,
        'vargs_updated_by': {
            'token': ['args_default']
        }
    }
    assert parser.get_default("token") is None


def test_parse_and_parser_merge_settings_p06_two_flags_set_cmd():
    cmd_line = ['--no_token']
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action="store_true")
    parser.add_argument("--no_token", action="store_false", dest="token")
    assert parser.get_default("token") is False

    args_default = kvargs.parser_extract_default_and_set_to_none(parser, {'token': True})
    assert args_default == {'token': True}
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'token': False,
        'vargs_updated_by': {
            'token': ['args_default',
                      'cmdline']
        },
    }
    assert parser.get_default("token") is None


def test_parse_and_parser_merge_settings_p07_text_simple_defaults():
    cmd_line = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    assert parser.get_default("token") is None

    args_default = kvargs.parser_extract_default_and_set_to_none(parser, {'token': 'set_default'})
    assert args_default == {'token': 'set_default'}
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line)
    assert vargs == {
        'token': 'set_default',
        'vargs_updated_by': {'token': ['args_default']}
    }
    assert parser.get_default("token") is None


def test_parse_and_parser_merge_settings_p08_text_simple_defaults_conf():
    cmd_line = []
    test_args_conf = {'token': 'set_by_conf'}
    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    assert parser.get_default("token") is None

    #    args_default = kvargs.parser_extract_default_and_set_to_none(parser, {'token': 'set_default'})
    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    args_default = {'token': 'set_default'}
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_parser_default=args_parser_default,
                                                   args_default=args_default,
                                                   cmd_line=cmd_line,
                                                   test_args_conf=test_args_conf)
    assert dict(vargs) == {
        'conf_files_loaded': ['test_args_conf'],
        'token': 'set_by_conf',
        'vargs_updated_by': {
            'token': ['args_default',
                      'conf:test_args_conf']
        },
    }
    assert parser.get_default("token") is None


def test_parse_and_parser_merge_settings_p09_store_true_conf():
    cmd_line = []
    test_args_conf = {'token': True}
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action="store_true")
    assert parser.get_default("token") is False

    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    args_default = {}
    # just clear sys.argv in order to test properly
    orig_sysargv = sys.argv
    sys.argv = ['pytest']
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_default=args_default,
                                                   args_parser_default=args_parser_default,
                                                   cmd_line=cmd_line,
                                                   test_args_conf=test_args_conf)

    # return to its original value
    sys.argv = orig_sysargv
    assert dict(vargs) == {
        'conf_files_loaded': ['test_args_conf'],
        'token': True,
        'vargs_updated_by': {
            'token': ['args_parser_default',
                      'conf:test_args_conf']
        },
    }

    assert parser.get_default("token") is None


def test_parse_and_parser_merge_settings_p10_store_true_empty_conf_default():
    cmd_line = []
    test_args_conf = {}
    args_default = {'token': True}
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", action="store_true")
    assert parser.get_default("token") is False

    args_parser_default = kvargs.parser_defaults(parser, set_to_none=True)
    vargs = kvargs.parse_and_parser_merge_settings(parser,
                                                   args_default=args_default,
                                                   args_parser_default=args_parser_default,
                                                   cmd_line=cmd_line,
                                                   test_args_conf=test_args_conf)

    args_default['vargs_updated_by'] = {'token': ['args_default']}
    args_default['conf_files_loaded'] = ['test_args_conf']
    assert dict(vargs) == args_default
    assert parser.get_default("token") is None


# ----------------------------------------

def test_prep_parse_and_parser_merge_settings_p01_str_simple():
    cmd_line = []
    args_default = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default="ken")
    assert parser.get_default("token") == "ken"
    vargs = kvargs.prep_parse_and_merge_settings(parser,
                                                 args_default=args_default,
                                                 cmd_line=cmd_line)
    assert dict(vargs) == {
        'token': 'ken',
        'vargs_updated_by': {'token': ['args_parser_default']
                             }
    }
    assert parser.get_default("token") is None


# ----------------------------------------

# the function name: def prep_parse_and_merge_settings(parser, args_default=None, cmd_line=None, test_args_conf=None):
# def test_prep_parse_and_merge_settings_p01_pass():

# ----------------------------------------

# argparse test - making sure we know how this library works

def test_argparse_p01_nothing_on_cmd_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    parser.add_argument("--mount")
    args = parser.parse_args([])
    assert vars(args) == {
        "mount": None,
        "token": None
    }


def test_argparse_p02_nothing_on_cmd_line_with_default():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default="ken")
    parser.add_argument("--mount")
    args = parser.parse_args([])
    assert vars(args) == {
        "mount": None,
        "token": "ken",
    }


def test_argparse_p03_extract_const():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", action='store_true')
    parser_obj = parser.__dict__['_option_string_actions']["--copy2sub"]
    assert parser_obj.const


def test_argparse_p04_extract_dest():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", action='store_true', dest="ken")
    parser_obj = parser.__dict__['_option_string_actions']["--copy2sub"]
    assert parser_obj.dest == "ken"


def test_argparse_p05_extract_default_dest_const():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", action='store_true', dest="ken", default=True)
    assert parser.get_default("ken") is True


def test_argparse_p06_extract_default_const_true():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", action='store_true', default=True)
    assert parser.get_default("copy2sub") is True


def test_argparse_p07_extract_default_const_set_none():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", action='store_true', default=None)
    assert parser.get_default("copy2sub") is None


def test_argparse_p08_extract_default_const_not_set_returns_false():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", action='store_true')
    assert parser.get_default("copy2sub") is False


def test_argparse_p08_extract_default_const_not_set_returns_true():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", action='store_false')
    assert parser.get_default("copy2sub") is True


def test_argparse_p09_extract_default():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", default="ken")
    assert parser.get_default("copy2sub") == "ken"


def test_argparse_p10_extract_default_none():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub")
    assert parser.get_default("copy2sub") is None


def test_argparse_p11_set_default_none2value():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub")
    assert parser.get_default("copy2sub") is None
    parser.set_defaults(**{"copy2sub": "set_default"})
    assert parser.get_default("copy2sub") == "set_default"


def test_argparse_p12_set_default_none2none():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub")
    assert parser.get_default("copy2sub") is None
    parser.set_defaults(**{"copy2sub": None})
    assert parser.get_default("copy2sub") is None


def test_argparse_p13_set_default_value2none():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", default="orig_value")
    assert parser.get_default("copy2sub") == "orig_value"
    parser.set_defaults(**{"copy2sub": None})
    assert parser.get_default("copy2sub") is None


def test_argparse_p13_set_default_value2value():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", default="orig_value")
    assert parser.get_default("copy2sub") == "orig_value"
    parser.set_defaults(**{"copy2sub": "set_default"})
    assert parser.get_default("copy2sub") == "set_default"


def test_argparse_p14_cmd_str_single_dash():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c")
    parser_keys = list(parser.__dict__['_option_string_actions'].keys())
    cmd = parser_keys[-1]
    cmd_str = cmd.replace('-', '')
    assert cmd_str == "c"


def test_argparse_p15_cmd_str_double_dash():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub")
    parser_keys = list(parser.__dict__['_option_string_actions'].keys())
    cmd = parser_keys[-1]
    cmd_str = cmd.replace('-', '')
    assert cmd_str == "copy2sub"


def test_argparse_p30_extract_keys_single():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub")
    parser_keys = parser.__dict__['_option_string_actions'].keys()
    assert list(parser_keys) == ['-h', '--help', '--copy2sub']


def test_argparse_p31_extract_keys_multi_per_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub", '-c')
    parser_keys = parser.__dict__['_option_string_actions'].keys()
    assert list(parser_keys) == ['-h', '--help', '--copy2sub', '-c']


def test_argparse_p32_extract_keys_multi_add_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub")
    parser.add_argument('-c')
    parser_keys = parser.__dict__['_option_string_actions'].keys()
    assert list(parser_keys) == ['-h', '--help', '--copy2sub', '-c']


def test_argparse_p33_extract_keys_positional():
    parser = argparse.ArgumentParser()
    parser.add_argument("copy2sub")
    parser_keys = parser.__dict__['_option_string_actions'].keys()
    assert list(parser_keys) == ['-h', '--help']


def test_argparse_p40_execute_cmds_one_with():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub1", action='store_true', default=None)
    parser.add_argument("--copy2sub2", action='store_true', default=None)
    parser.add_argument("--copy2sub3", action='store_true', default=None)
    args = parser.parse_args(["--copy2sub1"])
    assert vars(args) == {'copy2sub1': True,
                          'copy2sub2': None,
                          'copy2sub3': None, }


def test_argparse_p41_execute_cmds_two():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub1", action='store_true', default=None)
    parser.add_argument("--copy2sub2", action='store_true', default=None)
    parser.add_argument("--copy2sub3", action='store_true', default=None)
    args = parser.parse_args(["--copy2sub1", "--copy2sub3"])
    assert vars(args) == {'copy2sub1': True,
                          'copy2sub2': None,
                          'copy2sub3': True, }


def test_argparse_p42_execute_cmds_two_with_dest():
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy2sub1", action='store_true', dest="ken", default=None)
    parser.add_argument("--copy2sub2", action='store_false', dest="ken", default=None)
    parser.add_argument("--copy2sub3", action='store_true', default=None)
    args = parser.parse_args(["--copy2sub1", "--copy2sub3"])
    assert vars(args) == {'ken': True,
                          'copy2sub3': True, }
