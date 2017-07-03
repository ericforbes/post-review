from ConfigParser import SafeConfigParser, NoSectionError
import sys
import os

#Get path relevant to where configprocesser.py is
def _config_path():
    mydir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(mydir, 'config.ini')

#TODO: Throw errors if not configuration or settings
def _fetch(type, arg):
    config = SafeConfigParser()
    config.read(_config_path())
    try:
        data = config.get(type, arg)
        return data
    except NoSectionError:
        #Logging Error
        print("%s section does not exist in config.ini")
        sys.exit()
    except NoOptionError:
        #TODO LOGGING ERROR
        print("%s key does not exist in config.ini")
        sys.exit()

def _insert(type, key, value):
    config = SafeConfigParser()
    config.read(_config_path())
    config.set(type, key, value)
    with open(_config_path(), 'wb') as configfile:
        config.write(configfile)
    return 1

def put_config(setting, key, value):
    return _insert(setting, key, value)

def get_user_setting(arg):
    type = 'user_settings'
    return _fetch(type, arg)

def put_user_setting(key, value):
    type = 'user_settings'
    _insert(type, key, value)

def get_configuration(arg):
    type = 'configuration'
    return _fetch(type, arg)

def get_endpoint(type='name'):
    service = get_user_setting('service')
    if type == 'name': return service
    return _fetch(service, 'url')