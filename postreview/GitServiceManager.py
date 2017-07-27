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
from urlparse import urlparse

class GitServiceManager(object):
    GIT_SERVICES = [GitHubService, GitLabService]

    def __init__(self, target_branch):
        self.logger = create_logger()

        if not self._inside_working_tree():
            self.logger.error("you are not in a working git directory. please navigate to your current project")
            sys.exit()

        self.source_branch = self._determine_current_branch()
        self.parent_branch = target_branch

        if self.parent_branch == self.source_branch:
            self.logger.error("source branch (%s) cannot be the same as the one to merge with (%s)" % (self.source_branch, self.parent_branch))
            sys.exit()

        git_domain_url = self._determine_git_domain()
        print(git_domain_url)
        print("domain")
        if not git_domain_url:
            self.logger.fatal("Unable to determine git hosting service: %s" % self.remote_origin_url)
            self.logger.fatal("Are you using a relative URL path instead of a (sub)domain?")
            sys.exit()

        (self.namespace, self.project) = self._repo_url_attributes(git_domain_url, self.remote_origin_url)
        if not self.namespace or not self.project:
            self.logger.fatal("Unable to determine project and/or namespace from: %s" % self.remote_origin_url)
            sys.exit()

        self.git_service_engine = self._choose_engine(git_domain_url)
        self._get_set_api_token()


    def _get_last_commit_msg(self):
        return self._run_cmd("git log -1 --pretty=%B").strip()

    def _inside_working_tree(self):
        in_git_tree = self._run_cmd("git rev-parse --is-inside-work-tree").strip()
        if in_git_tree == 'true':
            return True
        return False


    def _get_set_api_token(self):
        #Get API token
        key = self._run_cmd("git config %s" % self.git_service_engine.GIT_CONFIG_API_KEY).strip()
        if (not key) or (key == "None"):
            self.logger.info("(One Time Setup) Please enter credentials to request API key")
            user = raw_input("%s username: " % self.git_service_engine.SERVICE_NAME)
            pw = getpass.getpass("%s password: " % self.git_service_engine.SERVICE_NAME)
            key, err = self.git_service_engine._request_token(user, pw)

            if (key == -1):
                self.logger.fatal('Could not request token. Please try again')
                sys.exit()

            self._run_cmd("git config %s %s" % (self.git_service_engine.GIT_CONFIG_API_KEY, key))

        return key


    def _push_branch_to_remote(self):
        cmd = "git push origin HEAD:%s" % self.source_branch
        u = raw_input("\n\nPushing local branch [%s] to remote [%s]:  Yes or no? " % (self.source_branch, self.source_branch))
        if u.lower() != 'yes' and u.lower() != 'y':
            self.logger.info("Exiting..")
            sys.exit()

        output = self._run_cmd(cmd)
        self.logger.info(output)


    def _determine_current_branch(self):
        branch = self._run_cmd("git rev-parse --abbrev-ref HEAD").rstrip()
        if not branch:
            self.logger.fatal("Unable to determine current git branch: git rev-parse --abbrev-ref HEAD")
            sys.exit()

        return branch


    def _determine_git_domain(self):
        #Handles both SSH and HTTPS
        #No support for relative URL path, only (sub)domain: https://docs.gitlab.com/omnibus/settings/configuration.html
        self.remote_origin_url = self._run_cmd("git config --get remote.origin.url").rstrip()

        #HTTPS URLS
        url = urlparse(self.remote_origin_url)
        print url
        if url.netloc:
            return url.netloc

        #SSH URLS
        matchObj = re.search(r'@+(?P<ssh_git_url>.*)?:', self.remote_origin_url)
        if matchObj.group('ssh_git_url'):
            return matchObj.group('ssh_git_url')

        return None


    def _choose_engine(self, domain):
        for engine in GitServiceManager.GIT_SERVICES:
            if engine.SERVICE_NAME in domain:
                return engine(self.source_branch, self.parent_branch, domain, self.namespace, self.project, self.logger)
        self.logger.fatal('%s is not a supported service [%s]' % (domain, GIT_SERVICES))


    def _repo_url_attributes(self, domain, remote_origin_url):
        domain_fixed = re.escape(domain)

        # git@gitlab.com:librid/my-postreview-test.git -> librid/my-postreview-test
        # https://gitlab.com/librid/my-postreview-test.git -> librid/my-postreview-test
        match = re.search(r'%s(:|\/)+?(.*)\.git' % domain_fixed, remote_origin_url)
        try:
            match_str = match.group(2).split("/")
            return (match_str[0], match_str[1])
        except IndexError:
            return (None, None)


    def post_review(self):

        self._push_branch_to_remote()
        token = self._get_set_api_token()

        params = {}
        if self.git_service_engine.SERVICE_NAME == 'github':
            params = {'message': self._get_last_commit_msg(), 'api_token': token}
        elif self.git_service_engine.SERVICE_NAME == 'gitlab':
            params = {'stuff': 'here'} 

        url = self.git_service_engine.issue_pull_request(params)
        self.logger.info(url)


    def _run_cmd(self, cmd):
        cmd_list = cmd.split()
        try:
            p = subprocess.Popen(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
            output = p.communicate()

            if not output[0]:
                return output[1]
            return output[0]

        except OSError as e:
            self.logger.fatal("Fatal: '%s' is either not in your path or is not installed" % cmd_list[0])
            sys.exit()
        except IndexError as e:
            self.logger.error("Error: Unexpected response from `%s`" % cmd)
            sys.exit()