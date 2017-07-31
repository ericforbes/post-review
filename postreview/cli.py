from __future__ import absolute_import
from builtins import object
from .configprocesser import get_configuration
from .GitCommandRunner import GitCommandRunner as Git
from .GitServiceManager import GitServiceManager

import argparse
import sys
import os

def main():
    driver = CliDriver()
    return driver.main()

class CliDriver(object):

    def main(self, args=None):

        if args is None:
            args = sys.argv[1:]

        parser = self._create_parser()
        parsed, remaining = parser.parse_known_args(args)
        try:
            if parsed.target is None:
                raise ValueError()
            self.target = parsed.target
        except (AttributeError, ValueError):
            sys.stderr.write("===================================")
            sys.stderr.write("\n")
            sys.stderr.write("WARNING: missing --target argument")
            sys.stderr.write("\n")
            sys.stderr.write("===================================")
            sys.stderr.write("\n\n")
            parser.print_help()
            return 255

        git_service = GitServiceManager(self.target)
        return git_service.post_review()


    def _create_parser(self):
        parser = argparse.ArgumentParser(description="create a code review and merge request")
        #parser._action_groups.pop()
        required = parser.add_argument_group('Required Arguments')
        required.add_argument('--target', '-t', help='remote branch to diff/merge with.')
        return parser
