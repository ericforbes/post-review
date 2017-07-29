from BaseService import BaseService
import sys

#Dependencies
from urlparse import urljoin
import requests #pip based
import json
import re
import getpass

class GitHubService(BaseService):
    SERVICE_NAME = "github"
    API = "https://api.github.com"
    CLIENT_ID = '40435bdcc83a625b6c9b'
    CLIENT_SECRET = '81703a26b85a31127071c6bbbc54ac37ea970df3'

    def parent_branch_exists(self):
        url = urljoin(self.API, '/repos/%s/%s/branches/%s' % (self.namespace, self.project, self.parent_branch))
        try:
            res = requests.get(url)
        except Exception as e:
            self.logger.fatal(e)
            sys.exit()

        json_response = json.loads(res.text)
        if res.status_code == 404:
            return False
        return True

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
        if res.status_code == 401:
            # Invalid credentials. Revoke token and start over.
            return (None, res.status_code)
        elif res.status_code >= 400:
            try:
                detailed_err_msg = json_response['errors'][0]['message']
            except:
                detailed_err_msg = ''

            try: 
                err_msg = json_response['message']
            except:
                err_msg = ''
            return ("Error: Could not create merge request. %s. %s" % (err_msg, detailed_err_msg), res.status_code)

        elif res.status_code == 201:
            try:
                pr_href = json_response["_links"]["html"]["href"]
            except:
                pr_href = "Merge request succeeded, but no URL was returned."
            return (pr_href, None)
            
        else:
            return (json_response, None)


    def _req_user_pass(self):
        self.logger.info("\n\n(One Time Setup) Please enter credentials to request API key")
        user = raw_input("%s username: " % self.SERVICE_NAME)
        pw = getpass.getpass("%s password: " % self.SERVICE_NAME)
        return (user, pw)

    def _setup_token(self):
        u,p = self._req_user_pass()
        url = urljoin(self.API, 'authorizations/clients/%s' % self.CLIENT_ID)
        #TODO: Add Fingerprint
        params = {
            'note': 'post-review cli utility (github, gitlab, etc)',
            'client_secret': self.CLIENT_SECRET,
            'scopes': ['public_repo', 'repo']
        }

        res = requests.put(
            url,
            auth = (u,p),
            data = json.dumps(params)
            )

        j = json.loads(res.text)
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
