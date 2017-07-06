import logging
from configprocesser import get_configuration

def create_logger():
    logging.basicConfig(filename=get_configuration('logfile'), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.getLevelName('DEBUG'))
    return logger