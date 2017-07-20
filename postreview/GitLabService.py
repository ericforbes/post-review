from BaseService import BaseService

from urlparse import urljoin
from urllib import urlencode
import requests
import json
import sys

class GitLabService(BaseService):
    SERVICE_NAME = "gitlab"
    GIT_CONFIG_API_KEY = "postreview.gitlab.key"

    def push_to_remote(self):
        print self.remote_branch
        print "GitLab: push to remote"

    def issue_pull_request(self):
        print self.remote_branch
        print "GitLab: issue pull request"

    def issue_pull_request(self, obj):

        try:
            merge_message = obj['message']
            api_token = obj['api_token']
        except KeyError:
            self.logger.fatal("GitHubService::issue_pull_request has incorrect parameters @%s" % obj)
            sys.exit()

        params = {
            'id': "%s%2F%s" % (self.namespace, self.project),
            'source_branch': self.source_branch,
            'target_branch': self.parent_branch,
            'title': merge_message
        }


    def _request_token(self, u, p):
        print(self.origin_domain)
        print("Domain above")
        url = urljoin('https://%s/' % self.origin_domain, 'api/v4/user')
        print(url)
        #TODO: Add Fingerprint
        params = {
            'grant_type': 'password',
            'username': u,
            'password': p
        }

        res = requests.get(
            url,
            headers = {"PRIVATE-TOKEN": "%s" % "a2ftiJ267x4J8zrTSPtN"}
            )
        j = json.loads(res.text)
        print(j)
        return(None, None)

        #if res.status_code >= 400:
        ##    return (-1, j.get('message', 'UNDEFINED ERROR (no error description from server)'))
        #else:
        #    try:
        #        if not j['token'] and j['hashed_token']:
        ##            #TODO: token is not in config, but its created. so its lost in the ether
        #            return (-1, 'Token lost in ether. Please revoke the token then re-run cmd: https://github.com/settings/applications')
        ##        else:
         #           return (j['token'], None)
         #   except KeyError:
         #       return (-1, "Successful response but unable to fetch credentials.")