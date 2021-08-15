__version__ = '1.02'

import argparse
import sys
from attrdict import AttrDict
from pathlib import Path, PurePath

import re
import subprocess


def grep_function_def(filename):
    """
    grep the filename and pull out all the function definition lines

    :param filename: (string)
    """

    grep_cmd = ['grep', 'def ', filename]

    output = subprocess.check_output(grep_cmd)

    return output.decode('ascii').split('\n')


def parse_test_function_names(function_name_list):
    """
    Parse out the function name from a list of test_function lines

    This list of lines is taken from:
    grep "def " test_transform.py

    and create the count by function that we testing

    :param function_name_list: (list)

    :return  function_stats: (dict) - function name and count of tests for it
    """
    re_tests = [
        re.compile(r'def\s+test\_raises\_exception\_on\_(.*)\_[fp]\d+_'),
        re.compile(r'def\s+test\_(.*)\_[fp]\d+_'),
    ]
    func_test = dict()
    for line in function_name_list:
        for reTest in re_tests:
            m = reTest.match(line)
            if m:
                if m.group(1) in func_test:
                    func_test[m.group(1)] += 1
                else:
                    func_test[m.group(1)] = 1
                break
    return func_test


def parse_function_names(function_name_list):
    """
    Parse out the function name from a list of function lines

    This list of lines is taken from:
    grep "def " test_transform.py

    and create the count by function that we testing

    :param function_name_list: (list)

    :return  function_stats: (dict) - function name and count of tests for it
    """
    re_test = re.compile(r'\s*def\s+(.*)\(')
    func_test = dict()
    for line in function_name_list:
        m = re_test.match(line)
        if m:
            if m.group(1) in func_test:
                func_test[m.group(1)] += 1
            else:
                func_test[m.group(1)] = 1
    return func_test


# ---------------------------------------------------------------------------
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Windows copy command for same files in two dirs ')
    parser.add_argument('file',
                        help="filename we evaluate")
    parser.add_argument("--test", '-t',
                        help="test filename associated with filename")
    parser.add_argument("--debug", '-d', action='store_true',
                        help="Debugging outputs")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    vargs = AttrDict(vars(args))

    if vargs.test is None:
        vargs.test = 'test_' + vargs.file

    if not Path(vargs.file).is_file():
        print(f'{vargs.file} is not a file')
        sys.exit(1)
    if not Path(vargs.test).is_file():
        print(f'{vargs.test} is not a file')
        sys.exit(1)

    file_lines = grep_function_def(vargs.file)
    file_func = parse_function_names(file_lines)
    test_lines = grep_function_def(vargs.test)
    test_func = parse_test_function_names(test_lines)

    if vargs.debug:
        print('file_lines:')
        print(file_lines)
        print('file_func:')
        print(file_func)

        print()

        print('test_lines:')
        print(test_lines)
        print('test_func:')
        print(test_func)

    not_tested = 0
    for k in sorted(file_func.keys()):
        if k not in test_func:
            print(f'{vargs.file}:{k} - not tested in {vargs.test}')
            not_tested += 1

    if not_tested:
        print(f'{vargs.file}:{not_tested} of {len(file_func)} functions not tested')

    test_no_func = 0
    for k in sorted(test_func.keys()):
        if k not in file_func:
            print(f'{vargs.test}:{k} - tests non-existing function in {vargs.file}')
            test_no_func += 1
    if test_no_func:
        print(f'{vargs.file}:{test_no_func} of {len(test_func)} functions test non-existing functions')
