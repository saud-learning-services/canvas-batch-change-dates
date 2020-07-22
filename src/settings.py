"""
settings.py
This file is responsible for defining/initializing global variables.

authors:
@markoprodanovic

last edit:
Friday, July 10, 2020
"""


def init():

    # Canvas object to provide access to Canvas API
    global course

    # Quiz object representing Canvas quiz specified by user input
    global quiz

    # Object containing information about students in course
    global students

    # Authorization for API Calls
    global auth_header
