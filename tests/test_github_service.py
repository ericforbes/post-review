import unittest
from mock import patch, MagicMock
from postreview.GitHubService import GitHubService
import requests
import json


import sys
import os

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')


class TestGitHubService(unittest.TestCase):
    def test_ssh_repo_information(self):
        service = GitHubService('NewFeatureBranch', 'master', 'git@github.com:ericforbes/post-review.git', None)
        owner, project_name = service._repo_information()
        self.assertEqual(owner, 'ericforbes')
        self.assertEqual(project_name, 'post-review')

    def test_https_repo_information(self):
        service = GitHubService('NewFeatureBranch', 'master', 'https://github.com/ericforbes/post-review.git', None)
        owner, project_name = service._repo_information()
        self.assertEqual(owner, 'ericforbes')
        self.assertEqual(project_name, 'post-review')

    @patch("postreview.GitHubService.requests.post")
    def test_github_pull_request(self, mock_requests):
        code_review_message = "my first code review"
        api_token = "1234abcd"
        local = "NewFeatureBranch"
        remote = "master"

        mock_requests.side_effect = [
        MagicMock(status_code=201, headers={'content-type':"application/json"},
                         text=json.dumps({'status':True}))
        ]

        service = GitHubService(local, remote, 'git@github.com:ericforbes/post-review.git', None)
        params = {'message': code_review_message, 'api_token': api_token}
        x = service.issue_pull_request(params)
        

        data = {"title": code_review_message, "head": local, "base": remote}
        mock_requests.assert_called_with(
            'https://api.github.com/repos/ericforbes/post-review/pulls',
            data=json.dumps(data),
            headers={'Authorization': 'token %s' % api_token}
        )

    @patch("postreview.GitHubService.requests.put")
    def test_github_fetch_token(self, mock_request):
        mock_request.side_effect = [MagicMock(status_code=201, headers={'content-type':"application/json"},
                         text=json.dumps({'status':True}))]

        local = "NewFeatureBranch"
        remote = "master"
        username = "frank"
        pw = "bigg13123"
        service = GitHubService(local, remote, 'git@github.com:ericforbes/post-review.git', None)
        key = service._request_token(username, pw)

        data = {"client_secret": GitHubService.CLIENT_SECRET, "scopes": ["public_repo", "repo"], "note": "post-review cli utility (github, gitlab, etc)"}
        mock_request.assert_called_with(
            'https://api.github.com/authorizations/clients/40435bdcc83a625b6c9b',
            auth=(username, pw),
            data=json.dumps(data)
        )
