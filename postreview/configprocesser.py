from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import sys
import os

#Get path relevant to where configprocesser.py is
def _config_path():
    mydir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(mydir, 'config.ini')

#TODO: Throw errors if not configuration or settings
def _fetch(section, key):
    config = SafeConfigParser()
    config.read(_config_path())
    
    try:
        data = config.get(section, key)
        return data
    except NoSectionError:
        #Logging Error
        print("%s section does not exist in config.ini" % section)
        sys.exit()
    except NoOptionError:
        #TODO LOGGING ERROR
        print("%s key does not exist in config.ini" % key)
        sys.exit()

def _insert(section, key, value):
    config = SafeConfigParser()
    config.read(_config_path())
    config.set(section, key, value)

    with open(_config_path(), 'wb') as configfile:
        config.write(configfile)
    return 1

def put_config(setting, key, value):
    return _insert(setting, key, value)

def get_user_setting(arg):
    return _fetch('user_settings', arg)

def put_user_setting(key, value):
    _insert('user_settings', key, value)

def get_configuration(arg):
    return _fetch('configuration', arg)

def get_endpoint(type='name'):
    service = get_user_setting('service')
    if type == 'name': return service
    return _fetch(service, 'url')