import time
import threading
from threading import Thread
from threading import Event

# Mostly inspired by https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
# Stoppable timer, runs in a separate thread
class RepeatingTimer(Thread):
    def __init__(self, interval_seconds, callback):
        Thread.__init__(self)
        self.stop_event = Event()
        self.interval_seconds = interval_seconds
        self.callback = callback
        self.setDaemon(True)

    def start(self):
        while not self.stop_event.wait(self.interval_seconds):
            self.callback()
    
    def stop(self):
        self.stop_event.set()