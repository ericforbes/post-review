from ConfigParser import SafeConfigParser
import argparse
import sys
import os
from config import setup
from configprocesser import get_user_setting, get_endpoint
from GitServiceManager import GitServiceManager

def SetupConfiguration():
    setup()
    
def main():

    parser = argparse.ArgumentParser(description="create a code review and merge request")
    parser._action_groups.pop()
    required = parser.add_argument_group('Required Arguments')
    optional = parser.add_argument_group('Optional Arguments')
    required.add_argument('--parent', '-p', help='remote branch to diff/merge with.')
    optional.add_argument('--new-remote', help='remote branch to push your local changes to. Default=current_branch_name')
    args = parser.parse_args()

    #if args.configure:
    #    SetupConfiguration()
    #    sys.exit()
    #elif get_user_setting('first_time_setup') == 'True': #TODO: Remove FirstTimeSetup, replace by checking for default
        #First time setup for default credentials
    #    SetupConfiguration()
    #    sys.exit()


    if len(sys.argv) == 1:
        parser.print_help();
        sys.exit()

    git_service = GitServiceManager(args.parent)
    git_service.post_review()