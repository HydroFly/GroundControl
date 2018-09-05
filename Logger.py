import sys, time, curses, threading, datetime

class Logger:
    def __init__(self):
        foo = 1
    
    def log(self, msg, log = "main"):
        # TODO: create Logs folder if it does not exist
        f = open("Logs/" + log + ".txt", "a")
        f.write("[GCS] <" + str(datetime.datetime.now()) + "> " + msg + "\n")