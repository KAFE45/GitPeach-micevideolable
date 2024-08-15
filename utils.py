# mICE Project
# Utils: Common utilities for the project

import sys
import time
import os
from datetime import datetime
import pickle
import json
from dataclasses import dataclass, field
from enum import Enum
from threading import Thread
from colorsys import hsv_to_rgb

import numpy as np 
import cv2
from icecream import ic as log


def print_libversion():

    # print python version
    print(f"{sys.version=}")

    # print the version of numpy
    print(f"{np.__version__=}")

    # print the version of opencv
    print(f"{cv2.__version__=}")

    # check if icecream is installed
    print(f"{log=}")


def get_log_prefix():
    return f'{datetime.now().strftime("%H:%M:%S.%f")[:-3]} : '


def initLog():
    log.configureOutput(prefix=get_log_prefix)


def get_timestamp(ts=None):
    if ts:
        return datetime.fromtimestamp(ts).isoformat()
    else:
        return datetime.now().isoformat()


def from_timestamp(timestamp: str):
    return datetime.fromisoformat(timestamp)


def read_config():
    DEFAULT_CONFIG_PATH = os.path.join(os.getcwd(), 'config.json')
    with open(DEFAULT_CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config


# Run pre-configuration for logging
initLog()

if __name__ == '__main__':
    print_libversion()