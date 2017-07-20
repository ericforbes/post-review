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
    driver = CliDriver()
    return driver.main()

class CliDriver(object):

    def main(self, args=None):

        if args is None:
            args = sys.argv[1:]

        parser = self._create_parser()
        parsed, remaining = parser.parse_known_args(args)

        if not parsed.parent:
            sys.stderr.write("===================================")
            sys.stderr.write("\n")
            sys.stderr.write("WARNING: missing --parent argument")
            sys.stderr.write("\n")
            sys.stderr.write("===================================")
            sys.stderr.write("\n\n")
            parser.print_help()
            return 255
        else:
            self.parent = parsed.parent
            git_service = GitServiceManager(self.parent)
            #return git_service.post_review()


    def _create_parser(self):
        parser = argparse.ArgumentParser(description="create a code review and merge request")
        #parser._action_groups.pop()
        required = parser.add_argument_group('Required Arguments')
        #optional = parser.add_argument_group('Optional Arguments')
        required.add_argument('--target', '-t', help='remote branch to diff/merge with.')
        #optional.add_argument('--new-remote', help='remote branch to push your local changes to. Default=current_branch_name')
        return parser
