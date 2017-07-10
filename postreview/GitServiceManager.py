from GitHubService import GitHubService
from GitLabService import GitLabService
import subprocess
import re
import sys
from logger import create_logger

#required depedendies
from requests.auth import HTTPBasicAuth
import requests
import getpass

class GitServiceManager(object):
    GIT_SERVICES = [GitHubService, GitLabService]

    def __init__(self, remote_branch):
        self.logger = create_logger()
        git_domain_url = self._determine_git_service()
        self.logger.error('fadsfa')
        self._remote_exists(remote_branch)
        print "what"
        self.source_branch = self._determine_current_branch()
        self.remote_branch = remote_branch
        self.git_service_engine = self._choose_engine(git_domain_url)
        self._get_set_api_token()

    def _get_set_api_token(self):
        #Get API token
        key = self._run_cmd("git config %s" % self.git_service_engine.GIT_CONFIG_API_KEY)
        print key
        if not key:
            u = raw_input("%s username: " % self.git_service_engine.SERVICE_NAME)
            p = getpass.getpass("%s password: " % self.git_service_engine.SERVICE_NAME)
            key = self.git_service_engine._request_token(u, p)

            self._run_cmd("git config %s %s" % (self.git_service_engine.GIT_CONFIG_API_KEY, key))

        #If no token, request it
        #

    def _determine_current_branch(self):
        branch = self._run_cmd("git rev-parse --abbrev-ref HEAD").rstrip()
        if not branch:
            self.logger.fatal("Unable to determine current git branch: git rev-parse --abbrev-ref HEAD")
            sys.exit()

        return branch

    def _remote_exists(self, branch):
        print("running: git ls-remote --heads")
        output = self._run_cmd("git ls-remote --heads")
        print "a"
        matchObj = re.search(r'refs/heads/%s' % branch, output)
        print "b"
        if not matchObj:
            self.logger.fatal("Remote branch does not exist: %s" % branch)
            sys.exit()

    def _determine_git_service(self):
        #Handles both SSH and HTTPS
        #No support for relative URL path, only (sub)domain: https://docs.gitlab.com/omnibus/settings/configuration.html
        remote_origin_url = self._run_cmd("git config --get remote.origin.url").rstrip()
        matchObj = re.search(r'@+(?P<ssh_git_url>.*)?:|https://(?P<https_git_url>.*)?/', remote_origin_url)
        print "1"
        if not matchObj.group('ssh_git_url') and not matchObj.group('https_git_url'):
            self.logger.fatal("Unable to determine git hosting service: %s" % remote_origin_url)
            self.logger.fatal("Are you using a relative URL path instead of a (sub)domain?")
            sys.exit()
        print "2"
        return matchObj.group('ssh_git_url') or matchObj.group('https_git_url')

    def _choose_engine(self, domain):
        for engine in GitServiceManager.GIT_SERVICES:
            if engine.SERVICE_NAME in domain:
                return engine(self.source_branch, self.remote_branch, self.logger)
        self.logger.fatal('%s is not a supported service [%s]' % (self.service_url, GIT_SERVICES))

    def post_review(self):
        self.git_service_engine.push_to_remote()
        self.git_service_engine.issue_pull_request()


    def _run_cmd(self, cmd):
        cmd_list = cmd.split()
        try:
            p = subprocess.Popen(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
            output = p.communicate()

            return output[0]

        except OSError as e:
            self.logger.fatal("'%s' is either not in your path or is not installed" % cmd_list[0])
            sys.exit()
        except IndexError as e:
            self.logger.error("Unexpected response from `%s`" % cmd)
            sys.exit()