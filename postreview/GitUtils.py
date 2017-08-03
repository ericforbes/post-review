from future import standard_library
standard_library.install_aliases()
import re
from urllib.parse import urlparse

def determine_git_domain(origin_url):
        #Handles both SSH and HTTPS
        #No support for relative URL path, only (sub)domain: https://docs.gitlab.com/omnibus/settings/configuration.html

        #HTTPS URLS
        url = urlparse(origin_url)
        if url.netloc:
            return url.netloc

        #SSH URLS
        matchObj = re.search(r'@+(?P<ssh_git_url>.*)?:', origin_url)

        try:
            if matchObj.group('ssh_git_url'):
                return matchObj.group('ssh_git_url')
        except:
            return None


def repo_url_attributes(domain, remote_origin_url):
        domain_fixed = re.escape(domain)

        # git@gitlab.com:ericforbes/my-postreview-test.git -> ericforbes/
        # https://gitlab.com/ericforbes/private/my-postreview-test.git -> ericforbes/private/
        namespace_match = re.search(r'%s(:|\/)(?P<namespace>.*\/)' % domain_fixed, remote_origin_url)

        # git@gitlab.com:ericforbes/private/my-postreview-test.git -> my-postreview-test
        # https://gitlab.com/ericforbes/my-postreview-test.git -> my-postreview-test
        project_match = re.search(r'%s(:|\/).*\/(?P<project>.*).git' % domain_fixed, remote_origin_url)

        try:
            # Remove any leading or trailing slashes -> ericforbes/private
            namespace = namespace_match.group('namespace').strip("/")

            project = project_match.group('project')

            return (namespace, project)
        except:
            return (None, None)
