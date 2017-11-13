# Watches our config.json file, updating the in-memory version if the file
# ever changes on disk. Thus, we're (almost) guaranteed the latest values. 

# We don't use "watchdog", because a) it requires a folder (or custom code)
# to just watch a file, and b) it locks the file; see:
# https://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes
import time
from changquan.timer.repeating_timer import RepeatingTimer

class ConfigWatcher:

    CONFIG_FILE_NAME = 'config.json'
    instance = None

    def __init__(self):
        ConfigWatcher.instance = self
        self.timer = RepeatingTimer(1, self.poll_file_for_changes)
        self.timer.start()        

    def poll_file_for_changes(self):
        print("POLLING!!!")

    def dispose(self):
        self.timer.stop()
        print("DEAD")