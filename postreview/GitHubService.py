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
            remote_url = obj['remote_url']
            merge_message = obj['message']
            api_token = obj['api_token']
        except KeyError:
            self.logger.fatal("GitHubService::issue_pull_request has incorrect parameters @%s" % obj)
            sys.exit()

        owner, project_name = self._repo_information(remote_url)

        params = {
            'title': merge_message,
            'head': self.source_branch,
            'base': self.parent_branch
        }
        #/repos/:owner/:repo/pulls
        #"Authorization: token OAUTH-TOKEN"
        # TODO  before EVERY REQUEST... BEFORE!!.. check if current API key is valid. add a @handler at top to do this.
        #  for example. i run this tool and it creates the key. i go into github and delete it. 
        url = urljoin(self.API, 'repos/%s/%s/pulls' % (owner, project_name))
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

            self.logger.fatal("Error: Could not create merge request, %s: %s" % (json_response['message'], err_msg))
            sys.exit()
        elif res.status_code == 201:
            try:
                pr_href = json_response['html']['href']
            except:
                pr_href = "Merge request succeeded, but no URL was returned."

            self.logger.info(pr_href)
        else:
            self.logger.info(json_response)


    def _repo_information(self, remote_origin):
        match_str = ""
        matchObj = re.search(r'git@github.com:(?P<ssh_owner_project>.*)\.git|https://github.com/(?P<https_owner_project>.*)\.git', remote_origin)
        if matchObj.group('ssh_owner_project'):
            match_str = matchObj.group('ssh_owner_project').split("/")
        elif matchObj.group('https_owner_project'):
            match_str = matchObj.group('https_owner_project').split("/")
        else:
            self.logger.error("Error: Unable to determine owner of GitHub repository")
            sys.exit()

        if not match_str[0] and not match_str[1]:
            self.logger.error("Error: Unable to find both owner and project from giturl")
            sys.exit()

        owner = match_str[0]
        project_name = match_str[1]
        return (owner, project_name)

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

        if res.status_code >= 400:
            msg = j.get('message', 'UNDEFINED ERROR (no error description from server)')
            self.logger.error("Fatal: Could not request API token      Reason: %s " % msg)
            sys.exit()
        if not j['token'] and j['hashed_token']: #TODO: token is not in config, but its created. so its lost in the ether, create a new one
            #TODO: Will need to delete current token, then re-request. Make sure no infinite loop occurs.
            self.logger.fatal('Fatal: Please revoke the token then re-run cmd: https://github.com/settings/applications')
        elif j['token']:
            self.api_token = j['token']
            return j['token']
        else:
            self.logger.fatal('Fatal: Eronious error fetching github credentials')

        #print j['token']