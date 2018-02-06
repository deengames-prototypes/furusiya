from attrdict import AttrDict
import json
import re
import file_watcher

# Global key/value pairs intended as global config. Reloads automatically.

data = {}


def load(raw_json):
    # remove comments (JSON doesn't officially support comments)
    raw_json = re.sub(r"//.*", "", raw_json)
    global data
    data = AttrDict(json.loads(raw_json))


def get(key):
    global data
    if key not in data:
        raise(Exception("There's no key called '{0}'. Keys: {1}".format(key, data.items())))
    else:
        return data[key]

file_watcher.watch('config.json', lambda raw_json: load(raw_json))