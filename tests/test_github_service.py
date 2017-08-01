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



if __name__ == '__main__':
    unittest.main()