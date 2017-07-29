from BaseService import BaseService

from urlparse import urljoin
from urllib import quote
import requests
import json
import sys

class GitLabService(BaseService):
    SERVICE_NAME = "gitlab"

    def _API(self):
        return urljoin('https://%s/' % self.origin_domain, 'api/v4/')


    def parent_branch_exists(self):
        url_path = '/projects/%s/repository/branches/%s' % (self._url_encoded_path(), self.parent_branch)
        url = self._API() + url_path

        try:
            res = requests.get(url)
        except Exception as e:
            self.logger.fatal(e)
            sys.exit()

        if res.status_code == 404:
            return False
        return True


    def issue_pull_request(self, obj):
        try:
            merge_message = obj['message']
            api_token = obj['api_token']
        except KeyError:
            self.logger.fatal("GitLabService::issue_pull_request has incorrect parameters @%s" % obj)
            sys.exit()

        params = {
            'source_branch': self.source_branch,
            'target_branch': self.parent_branch,
            'title': merge_message
        }

        url = urljoin(self._API(), 'projects/%s/merge_requests' % self._url_encoded_path())
        headers = {"PRIVATE-TOKEN": api_token}
        res = {}

        try:
            res = requests.post(
                url,
                headers = headers,
                data = params
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
                err_msg = str(json_response['message'][0])
            except:
                err_msg = ''
            return ("Error: Could not create merge request %s" % (err_msg), res.status_code)

        elif res.status_code == 201:
            try:
                pr_href = json_response["web_url"]
            except:
                pr_href = "Merge request succeeded, but no URL was returned."
            return (pr_href, None)

        else:
            return (json_response, None)


    def _url_encoded_path(self):
        # https://docs.gitlab.com/ce/api/README.html#namespaced-path-encoding
        return quote('%s/%s' % (self.namespace, self.project), safe='')


    def _setup_token(self):
        self.logger.info("\n\n(One Time Setup) Please create a Personal Access Token")
        self.logger.info("https://%s/profile/personal_access_tokens" % self.origin_domain)
        self.logger.info("Scope: API, Expires: Never\n")
        token = raw_input("Please enter your Personal Access Token:  ")

        # Make request to resource that requires us to be authenticated
        url = urljoin(self._API(), 'projects/%s/deploy_keys' % self._url_encoded_path())

        res = requests.get(
            url,
            headers = {"PRIVATE-TOKEN": token}
            )

        if res.status_code == 200:
            return(token, None)
        return(-1, "Invalid Personal Access Token")

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