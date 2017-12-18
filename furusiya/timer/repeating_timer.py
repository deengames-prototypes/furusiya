import time
import threading
from threading import Thread
from threading import Event

# Mostly inspired by https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
# Stoppable timer, runs in a separate thread
class RepeatingTimer(Thread):
    def __init__(self, interval_seconds, callback):
        super().__init__()
        self._stop_event = Event()
        self._interval_seconds = interval_seconds
        self._callback = callback
        self.setDaemon(True)


    def run(self):
        while not self._stop_event.wait(self._interval_seconds):
            self._callback()
            time.sleep(0)
    
    
    def stop(self):
        self._stop_event.set()
