from logger import create_logger

class Meta(type):
    def __str__(self):
        return self.SERVICE_NAME

class BaseService(object):
    SERVICE_NAME = None
    GIT_CONFIG_API_KEY = None
    API = None

    def __init__(self, source, remote, logger):
        self.source_branch = source
        self.remote_branch = remote
        self.logger = logger

    __metaclass__ = Meta

    def push_to_remote(self):
        raise NotImplementedError()

    def issue_pull_request(self):
        raise NotImplementedError()

    def _request_token(self, u, p):
        raise NotImplementedError()

    @classmethod
    def check_service_name(child_impl_class, service_name):
        return service_name == child_impl_class.SERVICE_NAME