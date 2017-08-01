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
        if matchObj.group('ssh_git_url'):
            return matchObj.group('ssh_git_url')

        return None


def repo_url_attributes(domain, remote_origin_url):
        domain_fixed = re.escape(domain)

        # git@gitlab.com:librid/my-postreview-test.git -> librid/my-postreview-test
        # https://gitlab.com/librid/my-postreview-test.git -> librid/my-postreview-test
        match = re.search(r'%s(:|\/)+?(.*)\.git' % domain_fixed, remote_origin_url)
        try:
            match_str = match.group(2).split("/")
            return (match_str[0], match_str[1])
        except IndexError:
            return (None, None)
