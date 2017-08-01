try:
    import mock
except ImportError:
    from unittest import mock

import unittest

from postreview.GitHubService import GitHubService
import requests
import json


import sys
import os

#sys.stdoutff = open(os.devnull, 'w')
#sys.stderrff = open(os.devnull, 'w')


class TestGitHubService(unittest.TestCase):
    

    @mock.patch("postreview.GitHubService.requests.post")
    def test_github_pull_request(self, mock_requests):
        code_review_message = "my first code review"
        api_token = "1234abcd"
        local = "NewFeatureBranch"
        remote = "master"
        merge_url = "https://github.com/ericforbes/post-review/mergerequest/4"

        mock_requests.side_effect = [
        mock.MagicMock(status_code=201, headers={'content-type':"application/json"},
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

        args, kwargs = mock_requests.call_args
        expected_data = {"title": code_review_message, "head": local, "base": remote}
        self.assertEqual(json.loads(kwargs.get('data'))['title'], expected_data['title'])
        self.assertEqual(json.loads(kwargs.get('data'))['base'], expected_data['base'])
        self.assertEqual(json.loads(kwargs.get('data'))['head'], expected_data['head'])
        self.assertEqual(kwargs.get('url'), 'https://api.github.com/repos/ericforbes/post-review/pulls')
        self.assertEqual(kwargs.get('headers')['Authorization'], 'token %s' % api_token)


    @mock.patch("postreview.GitHubService.requests.put")
    @mock.patch("postreview.GitHubService.GitHubService._req_user_pass")
    def test_github_fetch_token(self, fetch_credentials, mock_request):
        username = "frank"
        pw = "bigg13123"
        mock_request.side_effect = [mock.MagicMock(status_code=201, headers={'content-type':"application/json"},
                         text=json.dumps({'token':'1231100343-413-134'}))]
        fetch_credentials.side_effect = [(username,pw)]
        local = "NewFeatureBranch"
        remote = "master"
        service = GitHubService(local, remote, 'git@github.com:ericforbes/post-review.git', 'ericforbes', 'post-review', None)
        key, err = service._setup_token()

        args, kwargs = mock_request.call_args
        expected_data = {'client_secret': GitHubService.CLIENT_SECRET, 'scopes': ['public_repo', 'repo'], 'note': 'post-review cli utility (github, gitlab, etc)'}
        self.assertEqual(json.loads(kwargs.get('data'))['client_secret'], expected_data['client_secret'])
        self.assertEqual(json.loads(kwargs.get('data'))['scopes'], expected_data['scopes'])
        self.assertEqual(json.loads(kwargs.get('data'))['note'], expected_data['note'])
        self.assertEqual(kwargs.get('url'), 'https://api.github.com/authorizations/clients/%s' % GitHubService.CLIENT_ID)
        self.assertEqual(kwargs.get('auth'), (username, pw))

        self.assertEqual(key, '1231100343-413-134')


if __name__ == '__main__':
    unittest.main()