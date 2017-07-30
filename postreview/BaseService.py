from __future__ import absolute_import
from .logger import create_logger

class Meta(type):
    def __str__(self):
        return self.SERVICE_NAME

class BaseService(object):
    SERVICE_NAME = None
    GIT_CONFIG_API_KEY = None
    API = None

    def __init__(self, source, parent, origin_domain, namespace, project, logger):
        self.source_branch = source
        self.parent_branch = parent
        self.origin_domain = origin_domain
        self.namespace = namespace
        self.project = project
        self.logger = logger

    __metaclass__ = Meta


    def issue_pull_request(self, obj):
        raise NotImplementedError()

    def _setup_token(self):
        raise NotImplementedError()

    def parent_branch_exists(self):
        raise NotImplementedError()

    @classmethod
    def check_service_name(child_impl_class, service_name):
        return service_name == child_impl_class.SERVICE_NAME