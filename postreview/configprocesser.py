from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from configparser import SafeConfigParser, NoSectionError, NoOptionError
import sys
from .logger import create_logger
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
        logger.fatal("%s section does not exist in config.ini" % section)
        sys.exit()
    except NoOptionError:
        #TODO LOGGING ERROR
        logger.fatal("%s key does not exist in config.ini" % key)
        sys.exit()

#def _insert(section, key, value):
#    config = SafeConfigParser()
#    config.read(_config_path())
#    config.set(section, key, value)

#    with open(_config_path(), 'wb') as configfile:
#        config.write(configfile)
#    return 1

#def put_config(section, key, value):
#    return _insert(section, key, value)

def get_configuration(arg):
    return _fetch('configuration', arg)