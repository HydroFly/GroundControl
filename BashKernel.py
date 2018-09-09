import curses, redis
import time, datetime
from curses.textpad import Textbox, rectangle
from builtins import object
import re    

class BashKernel:
    def __init__(self):
        # Set cursor positions 
        self.cursor_x=0
        self.cursor_y=0

        self.rocketheight = 10

        # Initialize a new screen
        self.stdscr = curses.initscr()

        self.r = redis.StrictRedis('localhost', 6379, decode_responses=True)

        # Clean out the terminal
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.start_color()

        # Don't let the user type traditional input while in the app
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)  
        curses.curs_set(0)

        # Measure the screen
        self.height, self.width = self.stdscr.getmaxyx()

        # Set up color pairs
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_GREEN)

        # Set initial variables
        self.message = ""
        self.commandresults1 = ""
        self.commandresults2 = "" 
        self.commandresults3 = ""
        self.confirming = False

    def draw_cycle(self, data, app):
        self.height, self.width = self.stdscr.getmaxyx()

        self.app = app
        # self.stdscr.clear()
        self.height, self.width = self.stdscr.getmaxyx()
        self.draw_titlebar()
        self.draw_statusbar()
        self.draw_screen()
        self.draw_commandbar()
        self.draw_commandresults()
        self.stdscr.refresh()
    
    def draw_titlebar(self):
        time.ctime() # 'Mon Oct 18 13:35:29 2010'
        clock = time.strftime('%l:%M%p on %b %d, %Y') # ' 1:36PM EDT on Oct 18, 2010'
        titlebarstr = "HydroFly - Flight #{} - {}".format(1, clock)

        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(0,0,titlebarstr)
        self.stdscr.addstr(0, len(titlebarstr), " " * (self.width - len(titlebarstr) -1 ))
        self.stdscr.attroff(curses.color_pair(3))    

    def draw_commandresults(self): # Ranges from -6 to -3
        self.stdscr.addstr(self.height-5,0,self.commandresults1, curses.color_pair(7))
        self.stdscr.addstr(self.height-5,len(self.commandresults1), " " * (self.width - len(self.commandresults1) - 1 ),curses.color_pair(7))
        self.stdscr.addstr(self.height-4,0,self.commandresults2, curses.color_pair(7))
        self.stdscr.addstr(self.height-4,len(self.commandresults2), " " * (self.width - len(self.commandresults2) - 1 ),curses.color_pair(7))
        self.stdscr.addstr(self.height-3,0,self.commandresults3, curses.color_pair(7))
        self.stdscr.addstr(self.height-3,len(self.commandresults3), " " * (self.width - len(self.commandresults3) - 1 ),curses.color_pair(7))

    def exec_command(self, command):
        if(command == "launch"):
            if(self.app.rocket.launched):
                self.commandresults1 = "The rocket has already launched"
                return
            self.app.rocket.launched = True
            self.app.rocket.t = 0
            self.commandresults1 = "Rocket has launched"

        elif(command=="break"):
            raise Exception()
        
        elif(command=="quit" or command == "q" or command=="exit"):
            self.commandresults2 = "$ " + command
            self.commandresults3 = "Are you sure you want to quit? (y/n)"
            self.confirming = True

        elif(command=="abort"):
            self.commandresults1 = "Rocket launch aborted"
            self.r.set('abort', True)
            # self.app.rocket.abort_launch()
            self.app.rocket.launched = False

        elif(command=="logs"):
            self.commandresults1 = "Which log file do you want to access?"

        elif(command=="clear"):
            self.commandresults1, self.commandresults2, self.commandresults3 = "", "", ""

        else:
            self.commandresults1 = "Command is not recognized"

        if(self.confirming):
            if(command=="y" and self.confirming):
                self.app.close()
                raise KeyboardInterrupt
            if(command=="n" and self.confirming):
                self.confirming = False
                self.commandresults1, self.commandresults2, self.commandresults3 = "", "", ""

    def draw_commandbar(self):
        commandprompt = "rweas@HYDROFLY: $ " + self.message
        # self.stdscr.move(self.height-2,len(commandprompt))
        self.stdscr.addstr(self.height-2,0,commandprompt,curses.color_pair(6))
        self.stdscr.addstr(self.height-2,len(commandprompt), " " * (self.width - len(commandprompt) - 1 ),curses.color_pair(6))
        
        self.stdscr.nodelay(True)
        self.message.strip('\n').strip('\t')

        k = self.stdscr.getch()
        
        if(k!=-1 and k<122 and k != 9): # Character must exist and must be standard Unicode
            self.app.logger.log(str(k), "klog")
            char = chr(k)
            re.sub(r'\W+', '', char)
            self.message += char
            
        if(k==10): # Enter key
            self.app.logger.log("(user rweas) " + self.message, "cprompt")
            self.exec_command(self.message.strip('\n').strip('\t'))
            self.message = ""

        if(k==263): # Backspace key
            mess = self.message
            self.message = mess[:-2]
        
    def draw_statusbar(self):
        statusbarstr = "Flight Status | Enter 'quit' to exit | All systems nominal "
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(self.height-1,0,statusbarstr)
        self.stdscr.attroff(curses.color_pair(3))
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(self.height-1, len(statusbarstr), " " * (self.width - len(statusbarstr) -1 ))
        self.stdscr.attroff(curses.color_pair(3))

    def draw_screen(self):
        h = self.r.lpop('data:height')
        if h is not None:
            self.rocketheight = h
        self.stdscr.addstr(1,0, "Flight Data: LIVE")
        self.stdscr.addstr(2,0," " * self.width)
        # foo = ''
        # foo = '{0:.2f}'.format(self.rocketheight)
        self.stdscr.addstr(2,0," Rocket height: {} ft".format(self.rocketheight))
        self.stdscr.addstr(3,0," Time-of-flight: {} sec".format(self.app.rocket.t))
        self.stdscr.addstr(4,0," Water remaining: 4.5 gal")
        self.stdscr.addstr(5,0," Nozle pressure: 10 psi")
        self.stdscr.addstr(6,0," Distance from GCS: 30 ft")
        self.stdscr.addstr(7,0,"GCS Info")
        self.stdscr.addstr(8,0," Data logging: Strict")
        if(self.app.rocket.launched):
            self.app.rocket.z += 0.0009

    def write_to_commandresults(self, data):
        # TODO: 
        foo = 1
    
    def close(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()