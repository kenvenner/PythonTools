__version__ = '1.03'

import argparse
import sys
from attrdict import AttrDict
from pathlib import Path, PurePath

import re
import subprocess

"""
the the list of branches for the directory currently in
remove branches that meet the filter conditions
change branch to the desired branch (master)
git pull
then go to each of the other branches - and merge them with the desired branch
push any updates back to the remote repository
"""

def list_git_branches():
    """
    run the command to get the local list of git branches
    """

    git_branch_cmd = ['git', 'branch']

    output = subprocess.check_output(git_branch_cmd)

    return output.decode('ascii').split('\n')

def filter_to_skip_branches(git_branches, skip_branches=None):
    """
    filter out branches that match jira branches and pass back 
    this list of branches

    :params git_branches: (list of string) - list of branches
    :params skip_branches: (list of string) - list of words that cause us to remove this branch from our list of branches 

    """

    if skip_branches is None:
        skip_branches = ['legacy', 'master']

    filtered_branches = list()
    for branch in git_branches:
        if not branch:
            continue
        skip_branch = False
        for jbranch in skip_branches:
            if jbranch in branch:
                skip_branch = True
        if skip_branch:
            continue
        filtered_branches.append(branch)
    return filtered_branches
    

def git_branch_merge_command(git_branches, merge_branch=None):
    """
    list out of commands used to pull the desired branch and then generate the merge commands

    :params git-branches: (list of string) - list of branches
    :params merge_branch: (string) - the branch we consider as the branch we puill to and then merge from

    """
    
    if merge_branch is None:
        merge_branch = 'master'
    print('@ECHO ON')
    print(f'echo Pull from git {merge_branch}')
    print(f'git checkout {merge_branch}')
    print('git pull')
    print('@ECHO OFF')
    print('REM')
    
    for line in git_branches:
        lstrip = line.strip()
        if lstrip.startswith('* '):
            lstrip = lstrip[2:]
        print(f'echo Updating branch {lstrip}')
        print('@ECHO ON')
        print(f'git checkout {lstrip}')
        print(f'git merge {merge_branch}')
        print('@ECHO OFF')
        print("""if %ERRORLEVEL% == 1 (
    echo .
    echo Git Merge had issues - please clean up and rerun
    goto merge_issue
)""")
        print('@ECHO ON')
        print('git push')
        
    print(f'git checkout {merge_branch}')
    print('@ECHO OFF')
    print('goto exit')
    print(f':merge_issue')
    print(f'echo Merge issues need to be cleaned up')
    print(f':exit')
# ---------------------------------------------------------------------------
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Git merge branches')
    parser.add_argument("--skip", '-s', nargs='+',
                        help="list of project names to skip merge in git branches")
    parser.add_argument("--branch", '-b',
                        help="branch that we pull and then merge into other branches (default:  master)")
    parser.add_argument("--debug", '-d', action='store_true',
                        help="Debugging outputs")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()
    vargs = AttrDict(vars(args))

    git_branches = list_git_branches()
    remaining_branches = filter_to_skip_branches(git_branches, vargs.skip)
    git_branch_merge_command(remaining_branches, vargs.branch)
