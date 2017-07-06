import sys
import os
from logger import create_logger
from configprocesser import get_configuration, get_user_setting, put_user_setting, get_endpoint, put_config

def _setup_ssh(logger, profile):

    default_ssh_key = get_configuration('default_sshkey')
    user_setting_ssh_key = get_user_setting('sshkey')
    display_ssh_key = default_ssh_key
	
    if user_setting_ssh_key:
        display_ssh_key = user_setting_ssh_key

    valid_sshkey = False
    while not valid_sshkey:
        requested_ssh_key = raw_input("SSH Key [enter for %s]: " % display_ssh_key)

        if requested_ssh_key == "" and get_user_setting('sshkey'):
            valid_sshkey = True
        elif requested_ssh_key == "":
            logger.debug("setting ssh key: %s", display_ssh_key)
            put_user_setting('sshkey', display_ssh_key) #Needs to be here for initial setup
            valid_sshkey = True
        else:
            if os.path.isfile(os.path.expanduser(requested_ssh_key)):
                logger.debug("setting ssh key: %s", requested_ssh_key)
                put_user_setting('sshkey', requested_ssh_key)
                valid_sshkey = True
            else:
                print("Error: Not a valid SSH Key file")


def _setup_git_service(logger, profile):
    services = get_configuration('services')
    current_git_service = get_user_setting('service')
    display_git_service = services
    hosting_services = services.split(",")

    if current_git_service:
        display_git_service = current_git_service

    valid_option = False
    while not valid_option:
        requested_hosting_service = raw_input("Git Hosting Service [%s]: " % display_git_service)

        if requested_hosting_service == "" and current_git_service:
            valid_option = True
        elif requested_hosting_service in hosting_services:
            logger.debug("setting git service: %s", requested_hosting_service)
            put_user_setting('service', requested_hosting_service)
            valid_option = True
        else:
            print("Error: please choose a valid hosting option [%s]" % services)

    #Fetch specific URLs if GitLab or use current
    if get_endpoint() == 'gitlab':
        display_gitlab_url = 'gitlab.example.com'

        if get_endpoint(type='url'):
            display_gitlab_url = get_endpoint(type='url')

        valid_option = False
        while not valid_option:
            requested_gitlab_url = raw_input("Enter your enterprise GitLab URL [%s]: " % display_gitlab_url)

            if requested_gitlab_url == "" and get_endpoint(type='url'):
                valid_option = True
            elif requested_gitlab_url != "":
                logger.debug("setting gitlab url: %s", requested_gitlab_url)
                put_config('gitlab', 'url', requested_gitlab_url)
                valid_option = True
            else:
                print("Error: Enter valid enterprise GitLab URL (ex// gitlab.mycompany.com)")


def setup(profile='default'):
    logger = create_logger()
    _setup_git_service(logger, profile)
    _setup_ssh(logger, profile)
    put_user_setting('first_time_setup', 'False')