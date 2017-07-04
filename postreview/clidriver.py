from ConfigParser import SafeConfigParser
import argparse
import sys
import os
from config import setup

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
    elif get_user_setting('first_time_setup') == 'True':
        SetupConfiguration()
        sys.exit()

    if len(sys.argv) == 1:
        parser.print_help();
        sys.exit()