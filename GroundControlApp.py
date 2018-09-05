import sys, time, curses, threading, datetime
from BashKernel import BashKernel
from Logger import Logger
from Rocket import Rocket

class GroundControl:
    def __init__(self):
        self.bash = BashKernel()
        self.logger = Logger()
        self.rocket = Rocket()
        self.logger.log("A new instance of the GCS app has been created")
        # self.sdr = RtlSdr()

        # configure device
        # self.sdr.sample_rate = 2.048e6  # Hz
        # self.sdr.center_freq = 70e6     # Hz
        # self.sdr.freq_correction = 60   # PPM
        # self.sdr.gain = 'auto'

    def mainIOLoop(self):
        if(self.shouldCommunicate):
            # Do communications
            self.rocket.z = 5
            # samples = self.sdr.read_samples(256*1024)
            # self.logger.log(samples, "traffic")
            # self.rocket.t = samples.t

            # # Save to logs
            # self.logger.log(samples, "flight1")
    
    def mainLogicLoop(self):
        self.bash.draw_cycle([], self)

    def close(self):
        self.shouldCommunicate = False
        self.bash.close()
        self.logger.log("The app has successfully shut down.")
        SystemExit(0)