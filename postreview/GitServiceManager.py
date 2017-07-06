from GitHubService import GitHubService
from GitLabService import GitLabService

class GitServiceManager(object):
    GIT_SERVICES = [GitHubService, GitLabService]

    def __init__(self, service_name, source_branch, remote_branch):
        self.service_name = service_name
        self.source_branch = source_branch
        self.remote_branch = remote_branch
        self.git_service_engine = self.choose_engine()

    def choose_engine(self):
        for engine in GitServiceManager.GIT_SERVICES:
            if engine.check_service_name(self.service_name):
                print self.service_name
                print engine
                return engine(self.source_branch, self.remote_branch)

    def post_review(self):
        self.git_service_engine.push_to_remote()
        self.git_service_engine.issue_pull_request()