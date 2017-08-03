from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import input
from builtins import str
from .BaseService import BaseService

import json
import sys

#required
from urllib.parse import urljoin
from urllib.parse import quote
import requests


class GitLabService(BaseService):
    SERVICE_NAME = "gitlab"

    def _API(self):
        url = 'https://%s/' % self.origin_domain
        path = 'api/v4/'
        return urljoin(str(url), str(path))


    def parent_branch_exists(self, token):
        url_path = 'projects/%s/repository/branches/%s' % (self._url_encoded_path(), self.parent_branch)
        url = self._API() + url_path

        try:
            res = requests.get(
                url,
                headers={"PRIVATE-TOKEN": token}
            )
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

        path = 'projects/%s/merge_requests' % self._url_encoded_path()
        url = urljoin(str(self._API()), str(path))
        headers = {"PRIVATE-TOKEN": api_token}
        res = {}

        try:
            res = requests.post(
                url,
                headers=headers,
                data=params
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
            return ("Could not create merge request %s" % (err_msg), res.status_code)

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
        self.logger.warn("\n\n(One Time Setup) Please create a Personal Access Token")
        self.logger.warn("https://%s/profile/personal_access_tokens" % self.origin_domain)
        self.logger.warn("Scope: API, Expires: Never\n")
        token = input("Please enter your Personal Access Token:  ")

        # Make request to resource that requires us to be authenticated
        path = 'projects/%s/labels' % self._url_encoded_path()
        url = urljoin(str(self._API()), path)

        res = requests.get(
            url,
            headers={"PRIVATE-TOKEN": token}
            )

        if res.status_code == 200:
            return(token, None)
        return(-1, "Invalid Personal Access Token")
