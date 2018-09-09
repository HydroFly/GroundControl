import sys, time, curses, threading, datetime, logging, logging.config

from BashKernel import BashKernel
from GroundControlApp import GroundControl
from Rocket import Rocket
from Logger import Logger

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)
    fh = logging.FileHandler('Logs/exceptions.log')
    fh.setLevel(logging.CRITICAL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info('something cool')

    try:
        app = 0
        app = GroundControl()
        while(True):
            app.mainLogicLoop()
    except(KeyboardInterrupt):
        app.close()
    except(Exception): # Error Logging TODO: add more details
        logger.exception("A fatal error has occured")
        app.close()