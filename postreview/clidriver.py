from ConfigParser import SafeConfigParser
import argparse
import sys
from configprocesser import get_configuration, get_user_setting, put_user_setting, get_endpoint, put_config

def SetupConfiguration():
    services = get_configuration('services')
    hosting_services = services.split(",")

    valid_option = False
    while not valid_option:
        requested_hosting_service = raw_input("Git Hosting Service [%s]: " % services)
        if requested_hosting_service in hosting_services:
            valid_option = True
        else:
            print("  please choose a valid hosting option.")
    put_user_setting('service', requested_hosting_service)

    if get_endpoint() == 'gitlab':
        requested_gitlab_url = raw_input("Enter your enterprise GitLab URL [gitlab.example.com]: ")
        put_config('gitlab', 'url', requested_gitlab_url)
    put_user_setting('first_time_setup', 'False')



def main():
    #Fetch from config
    ## Git Hosting Service [gitlab,github,bitbucket]: gitlab
    ## Service Endpoint []:
    ## Default private key [~/.ssh/id_rsa]: INPUT HERE

    parser = argparse.ArgumentParser(description="create a code review and merge request")
    parser.add_argument('--parent', help='remote branch to diff/merge with. Default=master')
    parser.add_argument('--configure', action='store_true', help='configure local git service repo settings')
    args = parser.parse_args()

    if args.configure:
        SetupConfiguration()
        sys.exit()
    elif get_user_setting('first_time_setup') == 'True':
        SetupConfiguration()

    if len(sys.argv) == 1:
        parser.print_help();
        sys.exit()



    print('sdfds')