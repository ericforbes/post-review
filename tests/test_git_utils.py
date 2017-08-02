

import unittest
from postreview.GitUtils import determine_git_domain, repo_url_attributes
import requests
import json


import sys
import os

#sys.stdoutff = open(os.devnull, 'w')
#sys.stderrff = open(os.devnull, 'w')

class TestGitUtils(unittest.TestCase):


    def test_ssh_determine_domain(self):
        domain = determine_git_domain('git@github.com:ericforbes/post-review.git')
        self.assertEqual(domain, 'github.com')


    def test_https_determine_domain(self):
        domain = determine_git_domain('https://github.com/ericforbes/post-review.git')
        self.assertEqual(domain, 'github.com')


    def test_subdomain_determine_domain(self):
        domain = determine_git_domain('git@gitlab.company.com:ericforbes/post-review.git')
        self.assertEqual(domain, 'gitlab.company.com')


    def test_error_determine_domain(self):
        domain = determine_git_domain('www.google.com')
        self.assertEqual(domain, None)


    def test_ssh_repo_attributes(self):
        domain = 'gitlab.company.com'
        remote_origin_url = 'git@gitlab.company.com:ericforbes/private-repos/my-postreview-test.git'
        namespace, project = repo_url_attributes(domain, remote_origin_url)
        self.assertEqual(namespace, 'ericforbes/private-repos')
        self.assertEqual(project, 'my-postreview-test')


    def test_https_repo_attributes(self):
        domain = 'github.com'
        remote_origin_url = 'https://github.com/ericforbes/my-postreview-test.git'
        namespace, project = repo_url_attributes(domain, remote_origin_url)
        self.assertEqual(namespace, 'ericforbes')
        self.assertEqual(project, 'my-postreview-test')


    def test_error_repo_attributes(self):
        domain = 'github'
        remote_origin_url = 'https://bitbucket.com/ericforbes/my-postreview-test.git'
        namespace, project = repo_url_attributes(domain, remote_origin_url)
        self.assertEqual(namespace, None)
        self.assertEqual(project, None)


if __name__ == '__main__':
    unittest.main()