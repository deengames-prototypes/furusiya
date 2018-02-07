import os
import sys

import pytest

import config

path_ = os.path.join(os.getcwd(), 'furusiya')
sys.path.append(path_)


with open(os.path.join(path_, 'config.json')) as f:
    config.load(f.read())
