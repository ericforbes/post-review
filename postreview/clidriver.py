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
    parser.add_argument('--parent', help='remote branch to diff/merge with. Default=master')
    parser.add_argument('--configure', action='store_true', help='configure local git service repo settings')
    args = parser.parse_args()

    if args.configure:
        SetupConfiguration()
        sys.exit()
    elif get_user_setting('first_time_setup') == 'True': #TODO: Remove FirstTimeSetup, replace by checking for default
        #First time setup for default credentials
        SetupConfiguration()
        sys.exit()

    if len(sys.argv) == 1:
        parser.print_help();
        sys.exit()

    git_service = GitServiceManager(get_endpoint(), 'p-TNGSSOD-255', 'master09')
    git_service.post_review()