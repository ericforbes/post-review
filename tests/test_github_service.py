import unittest
from mock import patch, MagicMock
from postreview.GitHubService import GitHubService
import requests
import json


import sys
import os

sys.stdoutff = open(os.devnull, 'w')
sys.stderrff = open(os.devnull, 'w')


class TestGitHubService(unittest.TestCase):
    

    @patch("postreview.GitHubService.requests.post")
    def test_github_pull_request(self, mock_requests):
        code_review_message = "my first code review"
        api_token = "1234abcd"
        local = "NewFeatureBranch"
        remote = "master"
        merge_url = "https://github.com/ericforbes/post-review/mergerequest/4"

        mock_requests.side_effect = [
        MagicMock(status_code=201, headers={'content-type':"application/json"},
                         text=json.dumps(
                            {'_links':
                                {'html':
                                    {'href': merge_url}
                                }
                            }
                        )
                )
        ]
        service = GitHubService(local, remote, 'git@github.com:ericforbes/post-review.git', 'ericforbes', 'post-review', None)
        params = {'message': code_review_message, 'api_token': api_token}
        msg, err = service.issue_pull_request(params)

        self.assertEqual(msg, merge_url)

        data = {"title": code_review_message, "head": local, "base": remote}
        mock_requests.assert_called_with(
            'https://api.github.com/repos/ericforbes/post-review/pulls',
            data=json.dumps(data),
            headers={'Authorization': 'token %s' % api_token}
        )

    @patch("postreview.GitHubService.requests.put")
    @patch("postreview.GitHubService.GitHubService._req_user_pass")
    def test_github_fetch_token(self, fetch_credentials, mock_request):
        username = "frank"
        pw = "bigg13123"
        mock_request.side_effect = [MagicMock(status_code=201, headers={'content-type':"application/json"},
                         text=json.dumps({'token':'1231100343-413-134'}))]
        fetch_credentials.side_effect = [(username,pw)]
        local = "NewFeatureBranch"
        remote = "master"
        service = GitHubService(local, remote, 'git@github.com:ericforbes/post-review.git', 'ericforbes', 'post-review', None)
        key, err = service._setup_token()

        data = {"client_secret": GitHubService.CLIENT_SECRET, "scopes": ["public_repo", "repo"], "note": "post-review cli utility (github, gitlab, etc)"}
        mock_request.assert_called_with(
            'https://api.github.com/authorizations/clients/40435bdcc83a625b6c9b',
            auth=(username, pw),
            data=json.dumps(data)
        )
        self.assertEqual(key, '1231100343-413-134')
