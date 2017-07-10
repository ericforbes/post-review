from BaseService import BaseService

class GitLabService(BaseService):
    SERVICE_NAME = "gitlab"
    GIT_CONFIG_API_KEY = "postreview.gitlab.key"

    def __str__(self):
        return SERVICE_NAME

    def push_to_remote(self):
        print self.remote_branch
        print "GitLab: push to remote"

    def issue_pull_request(self):
        print self.remote_branch
        print "GitLab: issue pull request"