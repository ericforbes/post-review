import unittest
from mock import patch, MagicMock
from postreview.GitUtils import determine_git_domain, repo_url_attributes
import requests
import json


import sys
import os

#sys.stdoutff = open(os.devnull, 'w')
#sys.stderrff = open(os.devnull, 'w')

class TestGitUtils(unittest.TestCase):

    def test_ssh_repo_attributes(self):
        domain = determine_git_domain('git@github.com:ericforbes/post-review.git')
        self.assertEqual(domain, 'github.com')

    def test_https_repo_attributes(self):
        domain = determine_git_domain('https://github.com/ericforbes/post-review.git')
        self.assertEqual(domain, 'github.com')

    def test_subdomain_ssh_repo_attributes(self):
        domain = determine_git_domain('git@gitlab.company.com:ericforbes/post-review.git')
        self.assertEqual(domain, 'gitlab.company.com')
