import logging
import sys
from configprocesser import get_configuration

def create_logger():
    logging.basicConfig(filename=get_configuration('logfile'), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

    root = logging.getLogger()
    root.setLevel(logging.getLevelName('DEBUG'))

    #Add handler for standard output (console) any debug+
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.getLevelName('INFO'))
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    return root