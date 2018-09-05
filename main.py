import sys, time, curses, threading, datetime

from BashKernel import BashKernel
from GroundControlApp import GroundControl
from Rocket import Rocket
from Logger import Logger

if __name__ == '__main__':
    try:
        app = 0
        app = GroundControl()
        while(True):
            app.mainLogicLoop()
            # app.mainIOLoop()
            # time.sleep(.01)
    except(KeyboardInterrupt):
        app.close()
    except: # Error Logging TODO: add more details
        if app!=0:
            app.logger.log(str(sys.exc_info()[0]), "errors")
            app.close()
        else:
            logger = Logger()
            logger.log(str(sys.exc_info()[0]), "errors")