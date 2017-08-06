from __future__ import absolute_import
from builtins import object
from .GitHubService import GitHubService
from .GitLabService import GitLabService
from .GitCommandRunner import GitCommandRunner as Git
from .GitUtils import determine_git_domain, repo_url_attributes
from .configprocesser import get_configuration
from .logger import create_logger

import sys

#required depedendies
import requests


class GitServiceManager(object):
    GIT_SERVICES = [GitHubService, GitLabService]

    def __init__(self, target_branch):
        self.logger = create_logger()
        self.git_config_token_key = get_configuration('git_config_token_key')
        self.remote_origin_url = Git.get_remote_origin_url()
        self.source_branch = Git.get_current_branch()
        self.parent_branch = target_branch
        git_domain_url = determine_git_domain(self.remote_origin_url)
        (self.namespace, self.project) = repo_url_attributes(git_domain_url, self.remote_origin_url)

        if not Git.inside_working_tree():
            self.logger.error("you are not in a working git directory. please navigate to your current project")
            sys.exit()

        if self.parent_branch == self.source_branch:
            self.logger.error("source branch (%s) cannot be the same as the one to merge with (%s)" % (self.source_branch, self.parent_branch))
            sys.exit()

        if not git_domain_url:
            self.logger.fatal("Unable to determine git hosting service: %s" % self.remote_origin_url)
            self.logger.fatal("Are you using a relative URL path instead of a (sub)domain?")
            sys.exit()

        if not self.namespace or not self.project:
            self.logger.fatal("Unable to determine project and/or namespace from: %s" % self.remote_origin_url)
            sys.exit()

        self.git_service_engine = self._choose_engine(git_domain_url)
        self._get_set_api_token()


    def _get_set_api_token(self):
        #Get API token
        val = Git.get_api_token(self.git_config_token_key)
        if (not val) or (val == "None"):
            val, err = self.git_service_engine._setup_token()

            if (val== -1):
                if (err):
                    self.logger.fatal(err)
                else:
                    self.logger.fatal('Could not request token. Please try again')
                sys.exit()

            Git.add_api_token(self.git_config_token_key, val)

        return val


    def _choose_engine(self, domain):
        for engine in GitServiceManager.GIT_SERVICES:
            if engine.SERVICE_NAME in domain:
                return engine(self.source_branch, self.parent_branch, domain, self.namespace, self.project, self.logger)
        self.logger.fatal('%s is not a supported service [%s]' % (domain, GIT_SERVICES))


    def post_review(self):
        Git.push_branch_to_remote(self.source_branch)
        token = self._get_set_api_token()

        if not self.git_service_engine.parent_branch_exists(token):
            self.logger.fatal("Target branch does not exist. Please try again")
            sys.exit()

        params = {'message': Git.get_last_commit_msg(), 'api_token': token}

        (msg, error) = self.git_service_engine.issue_pull_request(params)
        if error == 401:
            Git.remove_api_token(self.git_config_token_key)
            self.logger.fatal("API token is invalid. Please re-run the command to create a new token")
            sys.exit()

        self.logger.warn(msg+'\n')
