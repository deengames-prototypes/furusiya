import json
import re
import file_watcher

# Global key/value pairs intended as global config. Reloads automatically.

_data = {}

def load(raw_json):
    # remove comments (JSON doesn't officially support comments)
    raw_json = re.sub(r"//.*", "", raw_json)
    global _data
    _data = json.loads(raw_json)

def get(key):
    global _data
    if not key in _data:
        raise(Exception("There's no key called '{0}'. Keys: {1}".format(key, _data.items())))
    else:
        return _data[key]

file_watcher.watch('config.json', lambda raw_json: load(raw_json))
