class Meta(type):
    def __str__(self):
        return self.SERVICE_NAME

class BaseService(object):
    SERVICE_NAME = None

    def __init__(self, source, remote):
        self.source_branch = source
        self.remote_branch = remote

    __metaclass__ = Meta

    def push_to_remote(self):
        raise NotImplementedError()

    def issue_pull_request(self):
        raise NotImplementedError()

    @classmethod
    def check_service_name(child_impl_class, service_name):
        return service_name == child_impl_class.SERVICE_NAME