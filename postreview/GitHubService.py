from BaseService import BaseService

class GitHubService(BaseService):
    SERVICE_NAME = "github"

    def push_to_remote(self):
        print self.remote_branch
        print "GitHub: push to remote"

    def issue_pull_request(self):
        print self.remote_branch
        print "GitHub: issue pull request"
