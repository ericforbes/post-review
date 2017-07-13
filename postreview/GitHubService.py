from BaseService import BaseService
import sys

#Dependencies
from urlparse import urljoin
import requests
import json

class GitHubService(BaseService):
    SERVICE_NAME = "github"
    GIT_CONFIG_API_KEY = "postreview.github.oath"
    API = "https://api.github.com"
    CLIENT_ID = '40435bdcc83a625b6c9b'
    CLIENT_SECRET = '81703a26b85a31127071c6bbbc54ac37ea970df3'

    def issue_pull_request(self, message):
        owner, project_name = self._owner_of_repo(self)

        params = {
            'title': message,
            'head': self.source_branch,
            'base': self.parent_branch
        }


        print self.remote_branch
        print "GitHub: issue pull request"

    def _owner_of_repo(self):
        match_str = ""
        matchObj = re.search(r'git@github.com:(?P<ssh_git_url_path>.*)/|https://github.com/(?P<https_git_url_path>.*)/', self.remote_origin_url)
        if matchObj.group('ssh_git_url_path'):
            match_str = matchObj.group('ssh_git_url_path').split("/")
        elif matchObj.group('https_git_url_path'):
            match_str = matchObj.group('https_git_url_path').split("/")
        else:
            self.logger.error("Error: Unable to determine owner of GitHub repository")
            sys.exit()

        owner = match_str[0]
        project_name = match_str[1]
        return (owner, project_name)

    def _request_token(self, u, p):
        url = urljoin(self.API, 'authorizations/clients/%s' % self.CLIENT_ID)
        #TODO: Add Fingerprint
        params = {
            'note': 'post-review cli utility (github, gitlab, etc)',
            'client_secret': self.CLIENT_SECRET,
            'scope': ['public_repo', 'repo']
        }
        print url
        res = requests.put(
            url,
            auth = (u,p),
            data = json.dumps(params)
            )

        j = json.loads(res.text)
        print j
        if res.status_code >= 400:
            msg = j.get('message', 'UNDEFINED ERROR (no error description from server)')
            self.logger.error(msg)
            sys.exit()
        if not j['token'] and j['hashed_token']: #TODO: token is not in config, but its created. so its lost in the ether, create a new one
            #TODO: Will need to delete current token, then re-request. Make sure no infinite loop occurs.
            self.logger.fatal('Fatal: Please revoke the token then re-run cmd: https://github.com/settings/applications')
        elif j['token']:
            return j['token']
        else:
            self.logger.fatal('Fatal: Eronious error fetching github credentials')

        #print j['token']