import unittest
from mock import patch
import postreview
from postreview import cli
from postreview.cli import CliDriver
from postreview.GitServiceManager import GitServiceManager

import sys
import os

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')


class TestCliDriver(unittest.TestCase):
    def test_functional_incorrect_args(self):
        driver = CliDriver()
        rc = driver.main('parent frankenstein'.split())
        self.assertEqual(rc, 255)

    @patch('postreview.GitServiceManager.GitServiceManager.__init__')
    @patch('postreview.GitServiceManager.GitServiceManager.post_review')
    def test_functional_correct_args(self, post_review, init):
        init.return_value = None
        post_review.return_value = 1


        driver = CliDriver()
        rc = driver.main('--parent master'.split())
        self.assertEqual(rc, 1)

    def test_arg_parsing_correct(self):
        driver = CliDriver()
        parser = driver._create_parser()
        parsed, remaining = parser.parse_known_args('--parent master'.split())
        self.assertEqual(parsed.parent, 'master')
        self.assertEqual(remaining, [])

    def test_arg_parsing_incorrect(self):
        driver = CliDriver()
        parser = driver._create_parser()
        parsed, remaining = parser.parse_known_args('parent master'.split())
        self.assertEqual(parsed.parent, None)
        self.assertEqual(remaining, ['parent','master'])

