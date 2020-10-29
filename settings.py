"""
settings.py
This file is responsible for defining/initializing global variables.
"""
import os
import pytz

# Canvas API Token
TOKEN = None

# Global canvasapi Canvas object for making api calls
CANVAS = None

# Canvas INSTANCE - https://ubc.instructure.com by default - set in Jupyter Notebook
INSTANCE = 'https://ubc.instructure.com/'

# Global constants for representing and formatting time
LOCAL_TIMEZONE = pytz.timezone('Canada/Pacific')
TIME_FORMAT = '%Y-%m-%d %I:%M:%S %p %Z%z'

# Path to root project folder
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
