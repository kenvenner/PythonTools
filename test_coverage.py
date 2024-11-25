__version__ = '1.06'

import argparse
import sys
#from attrdict import AttrDict
from pathlib import Path, PurePath

import re
import subprocess

import pprint
pp = pprint.PrettyPrinter(indent=4)


def grep_function_def(filename):
    """
    grep the filename and pull out all the function definition lines

    :param filename: (string)
    """

    grep_cmd = ['grep', 'def ', filename]

    output = subprocess.check_output(grep_cmd)

    return output.decode('ascii').split('\n')


def grep_function_class_def(filename):
    """
    grep the filename and pull out all the function definition
    and class definitoin lines

    :param filename: (string)
    """

    grep_cmd = ['grep', '-P', '^class |def ', filename]

    output = subprocess.check_output(grep_cmd)

    return output.decode('ascii').split('\n')

def remove_comment_lines(lines):
    """"
    remove the lines that are comment lines
    """
    re_comment = re.compile(r'^\s*#')
    return [x for x in lines if not re_comment.match(x)]

def parse_test_function_names(function_name_list):
    """
    Parse out the function name from a list of test_function lines

    This list of lines is taken from:
    grep "def " test_transform.py

    and create the count by function that we testing

    :param function_name_list: (list)

    :return  function_stats: (dict) - function name and count of tests for it
    """
    re_comment = re.compile(r'^\s*#')
    re_tests = [
        re.compile(r'\s*def\s+test\_raises\_exception\_on\_(.*)\_[fp]\d+_'),
        re.compile(r'\s*def\s+test\_(.*)\_[fp]\d+_'),
    ]
    func_test = dict()
    for idx, line in enumerate(function_name_list):
        # check for comment line and skip
        c = re_comment.match(line)
        if c:
            # print('skipped: ' + line)
            continue

        # print(line)
        
        for reTest in re_tests:
            m = reTest.match(line)
            if m:
                func_name = m.group(1)
                # print(func_name, line)
                if func_name in func_test:
                    func_test[func_name] += 1
                else:
                    func_test[func_name] = 1
                break
    return func_test


def parse_function_names(function_name_list):
    """
    Parse out the function name from a list of function lines

    This list of lines is taken from:
    grep "def " transform.py

    and create the count by function that we testing

    :param function_name_list: (list)

    :return  function_stats: (dict) - function name and count of tests for it
    """
    re_comment = re.compile(r'^\s*#')
    re_class= re.compile(r'^class\s+(.*)\(')
    re_func = re.compile(r'^\s*def\s+(.*)\(')
    prior_func = ''
    last_class = ''
    func_test = dict()
    for idx, line in enumerate(function_name_list):
        # check for comment line and skip
        c = re_comment.match(line)
        if c:
            # print('skipped: ' + line)
            continue

        # debugg
        #print(idx, line)
        
        c = re_class.match(line)
        if c:
            last_class = c.group(1)
            continue
        m = re_func.match(line)
        if m:
            if line[0] != ' ':
                # if the line is not indented
                # we exited class functions
                # so clear the class name
                last_class = ''
            # build up function name that will match our test case definitions
            func_name = '_'.join([last_class, m.group(1)]) if last_class else m.group(1)
            if func_name in func_test:
                # seen again - count occurences
                func_test[func_name]['cnt'] += 1
                func_test[func_name]['line'] = line
                func_test[func_name]['idx'] = idx
                func_test[func_name]['prior'] = prior_func
            else:
                # first time seen
                func_test[func_name] = {
                    'cnt': 1,
                    'line': line,
                    'idx': idx,
                    'prior': prior_func
                }
            prior_func = func_name

    # debug
    # pprint.pprint(func_test)
    
    return func_test


# ---------------------------------------------------------------------------
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Function Test Coverage for Python and Python-Test files')
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
    #vargs = AttrDict(vars(args))
    vargs = vars(args)

    if vargs['test'] is None:
        vargs['test'] = 'test_' + vargs['file']

    if not Path(vargs['file']).is_file():
        print(f"{vargs['file']} is not a file")
        sys.exit(1)
    if not Path(vargs['test']).is_file():
        print(f"{vargs['test']} is not a file")
        sys.exit(1)

    file_lines = grep_function_class_def(vargs['file'])
    file_lines = remove_comment_lines(file_lines)
    file_func = parse_function_names(file_lines)
    test_lines = grep_function_def(vargs['test'])
    test_lines = remove_comment_lines(test_lines)
    test_func = parse_test_function_names(test_lines)

    if vargs['debug']:
        print('file_lines:')
        pprint.pprint(file_lines)
        print('file_func:')
        pprint.pprint(file_func)

        print()

        print('test_lines:')
        pprint.pprint(test_lines)
        print('test_func:')
        pprint.pprint(test_func)

    print_hdr = True
    def_lines=dict()
    not_tested_list=list()
    not_tested = 0
    for k in sorted(file_func.keys()):
        if k not in test_func and \
           'test_' + k not in test_func:
            not_tested += 1
            if not print_hdr:
                print(f"{vargs['file']} / {vargs['test']}")
                print_hdr = False
            print(f"{vargs['file']}:{k} - not tested in {vargs['test']}")
            def_lines[file_func[k]['idx']] = {
                'line': file_func[k]['line'],
                'prior': file_func[k]['prior'],
                'func': k
            }
            
    if not_tested:
        print(f"{vargs['file']}:{not_tested} of {len(file_func)} functions not tested")

    test_no_func = 0
    for k in sorted(test_func.keys()):
        if k not in file_func:
            print(f"{vargs['test']}:{k} - tests non-existing function in {vargs['file']}")
            test_no_func += 1
    if test_no_func:
        print(f"{vargs['file']}:{test_no_func} of {len(test_func)} functions test non-existing functions")

    if def_lines:
        last_prior = ''
        for dl in sorted(def_lines.keys()):
            print('#'*40)
            dlv = def_lines[dl]
            if last_prior != dlv['prior']:
                print('# prior function:', dlv['prior'])

            print('# the function name:', dlv['line'])
            print('#', 'def test_' + dlv['func']+'_p01_pass(self):')
            last_prior = dlv['func']

# eof
