import logging
import sys

def create_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

    root = logging.getLogger()
    root.setLevel(logging.getLevelName('DEBUG'))

    #Add handler for standard output (console) any debug+
    #ch = logging.StreamHandler(sys.stdout)
    #ch.setLevel(logging.getLevelName('DEBUG'))
    #formatter = logging.Formatter('%(message)s')
    #ch.setFormatter(formatter)
    #root.addHandler(ch)
    
    return root