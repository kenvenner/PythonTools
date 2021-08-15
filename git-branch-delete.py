__version__ = '1.01'

import argparse
import sys
from attrdict import AttrDict
from pathlib import Path, PurePath

import re
import subprocess


def list_git_branches():
    """
    run the command to get the local list of git branches
    """

    git_branch_cmd = ['git', 'branch']

    output = subprocess.check_output(git_branch_cmd)

    return output.decode('ascii').split('\n')


def filter_to_jira_branches(git_branches, jira_branches=None):
    """
    filter out branches that match jira branches and pass back 
    this list of branches
    """

    if jira_branches is None:
        jira_branches = ['NCCWEB']

    return [branch for branch in git_branches for jbranch in jira_branches if jbranch in branch]


def git_branch_delete_command(git_branches):
    print('git checkout master')

    for line in git_branches:
        lstrip = line.strip()

        if lstrip.startswith('* '):
            lstrip = lstrip[2:]

        print(f'git branch -d {lstrip}')


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Git branch delete routines from JIRA')
    parser.add_argument("--jira", '-j', nargs='+',
                        help="list of jira project names in git branches")
    parser.add_argument("--debug", '-d', action='store_true',
                        help="Debugging outputs")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()
    vargs = AttrDict(vars(args))

    git_branches = list_git_branches()
    jira_branches = filter_to_jira_branches(git_branches, vargs.jira)
    git_branch_delete_command(jira_branches)
