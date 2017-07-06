from BaseService import BaseService

class GitLabService(BaseService):
    SERVICE_NAME = "gitlab"

    def push_to_remote(self):
        print self.remote_branch
        print "GitLab: push to remote"

    def issue_pull_request(self):
        print self.remote_branch
        print "GitLab: issue pull request"