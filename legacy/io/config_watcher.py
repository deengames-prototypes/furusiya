# Watches our config.json file, updating the in-memory version if the file
# ever changes on disk. Thus, we're (almost) guaranteed the latest values. 

# We don't use "watchdog", because a) it requires a folder (or custom code)
# to just watch a file, and b) it locks the file; see:
# https://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes
import json
from json.decoder import JSONDecodeError
import os

from legacy.timer.repeating_timer import RepeatingTimer


class ConfigWatcher:

    CONFIG_FILE_NAME = 'assets/data/config.json'
    instance = None

    def __init__(self):
        ConfigWatcher.instance = self

        self._data = {}
        self._last_changed_on = None
        self.poll_file_for_changes()

        self._timer = RepeatingTimer(1, self.poll_file_for_changes)
        self._timer.start()  

    def poll_file_for_changes(self):
        modified_on = os.path.getmtime(ConfigWatcher.CONFIG_FILE_NAME)
        if modified_on != self._last_changed_on:
            self._last_changed_on = modified_on
            self.refresh_config()

    def refresh_config(self):
        with open(ConfigWatcher.CONFIG_FILE_NAME) as json_data:
            try:
                self._data = json.load(json_data)
                print("Config.json updated: {0}".format(self._data))
            except JSONDecodeError as ex:
                print("Error updating config.json: {0}".format(ex))
                # traceback.print_exc() # prints the stack-trace
                # don't "raise", we want to keep retrying

    def has(self, key):
        return key in self._data

    def get(self, key):
        return self._data[key]

    def dispose(self):
        self._timer.stop()
