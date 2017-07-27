from BaseService import BaseService
import sys

#Dependencies
from urlparse import urljoin
import requests #pip based
import json
import re

class GitHubService(BaseService):
    SERVICE_NAME = "github"
    GIT_CONFIG_API_KEY = "postreview.github.token"
    API = "https://api.github.com"
    CLIENT_ID = '40435bdcc83a625b6c9b'
    CLIENT_SECRET = '81703a26b85a31127071c6bbbc54ac37ea970df3'

    def issue_pull_request(self, obj):

        try:
            merge_message = obj['message']
            api_token = obj['api_token']
        except KeyError:
            self.logger.fatal("GitHubService::issue_pull_request has incorrect parameters @%s" % obj)
            sys.exit()

        params = {
            'title': merge_message,
            'head': self.source_branch,
            'base': self.parent_branch
        }

        url = urljoin(self.API, 'repos/%s/%s/pulls' % (self.namespace, self.project))
        headers = {"Authorization": "token %s" % api_token}
        res = {}

        try:
            res = requests.post(
                url,
                headers = headers,
                data = json.dumps(params)
                )
        except Exception as e:
            self.logger.fatal(e)
            sys.exit()


        json_response = json.loads(res.text)
        if res.status_code >= 400:

            try:
                err_msg = json_response['errors'][0]['message']
            except:
                err_msg = ''

            return "Error: Could not create merge request, %s: %s" % (json_response['message'], err_msg)

        elif res.status_code == 201:
            try:
                pr_href = json_response["_links"]["html"]["href"]
            except:
                pr_href = "Merge request succeeded, but no URL was returned."

            return pr_href
        else:
            return json_response


    def _request_token(self, user, pw):
        url = urljoin(self.API, 'authorizations/clients/%s' % self.CLIENT_ID)
        #TODO: Add Fingerprint
        params = {
            'note': 'post-review cli utility (github, gitlab, etc)',
            'client_secret': self.CLIENT_SECRET,
            'scopes': ['public_repo', 'repo']
        }

        res = requests.put(
            url,
            auth = (user,pw),
            data = json.dumps(params)
            )

        j = json.loads(res.text)
        print(j)
        if res.status_code >= 400:
            return (-1, j.get('message', 'UNDEFINED ERROR (no error description from server)'))
        else:
            try:
                if not j['token'] and j['hashed_token']:
                    #TODO: token is not in config, but its created. so its lost in the ether
                    return (-1, 'Token lost in ether. Please revoke the token then re-run cmd: https://github.com/settings/applications')
                else:
                    return (j['token'], None)
            except KeyError:
                return (-1, "Successful response but unable to fetch credentials.")
