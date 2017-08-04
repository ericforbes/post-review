from __future__ import absolute_import
from builtins import object
from .logger import create_logger
from future.utils import with_metaclass

class Meta(type):
    def __str__(self):
        return self.SERVICE_NAME

class BaseService(with_metaclass(Meta, object)):
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

    

    def issue_pull_request(self, obj):
        raise NotImplementedError()

    def _setup_token(self):
        raise NotImplementedError()

    def parent_branch_exists(self, token):
        raise NotImplementedError()

    @classmethod
    def check_service_name(child_impl_class, service_name):
        return service_name == child_impl_class.SERVICE_NAME