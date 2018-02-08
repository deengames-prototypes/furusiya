import os
import sys

path_ = os.path.join(os.getcwd(), 'furusiya')
sys.path.append(path_)

from model.config import config

with open(os.path.join(path_, 'config.json')) as f:
    config.load(f.read())
