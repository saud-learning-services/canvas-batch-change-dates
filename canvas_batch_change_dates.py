
"""
This module contains functions that are imported and executed in Jupyter Notebook
It also contains helper functions
All functionality is around changing course dates on Canvas and reading/writing to CSVs
"""

from canvasapi import Canvas
import datetime
import settings
import shutil
import sys
import getpass
import os
import pandas as pd
from IPython.display import display
from termcolor import cprint

# Functions to run in Notebook


def initialize():
    '''
    Main entry point for Jupyter Notebook
    '''
    settings.TOKEN = getpass.getpass('Enter token: ').strip()
    settings.CANVAS = create_instance(settings.INSTANCE, settings.TOKEN)

def create_courses_file():

    #TODO - this function is incomplete - needs to ask user if they want to create
    #TODO - give option to do this or choose existing
    #TODO - enrollment_term filter
    
    """Creates a file to work with get_courses_df from subaccount_id

    parameters:
    subaccount_id (Int): the subaccount to run in

    returns:
    df (Dataframe): dataframe with course ids and current course information
    """
    account_id = getpass.getpass('Enter subaccount_id: ').strip()
    account = settings.CANVAS.get_account(account_id)
    courses = account.get_courses()

    for c in courses:
    course_dict = {'course_id': c.id,
        'course_name': c.name,
        'term': c.enrollment_term_id,
        'course_subaccount': c.account_id,
        'course_subaccount_name': CANVAS.get_account(c.account_id).name,
        'start_at' : c.start_at,
        'end_at' : c.end_at,
        'timezone' : c.time_zone}
    
    course_info.append(course_dict)
    
    df = pd.DataFrame(course_info)
    
    df.to_csv(f'{settings.ROOT_PATH}/data/output/{account_id}-course information.csv')


def get_courses_df(file):
    """Tries to read and return file as df

    parameters:
    file (String): the name of the file with courses

    returns:
    df (Dataframe): dataframe with course ids
    """

    try:
        # read file
        df = pd.read_csv(file)
        cprint('Successfully loaded csv file', 'green')

        return(df)

    except IOError as e:
        # file not found
        print(e)
        print("\nYou should have the file indicated above in the same folder\
            \nas this notebook: {}\n".format(os.getcwd()))
        sys.exit(1)
    except KeyError as ke:
        # file doesn't have course ids
        print(ke)
        print("\nThe file {} should have the columns course_id, start_date, and end_date.\n".format(file))
        sys.exit(1)


def create_course_update_df(df, restrict_enrol=None):
    """iterates on df of course lists and creates a list of update details"""

    my_list_x = []

    for index, row in df.iterrows():
        course_id = row["course_id"]
        start_at = row["start_date"]
        end_at = row["end_date"]

        x = get_course_detail(course_id, start_at, end_at, restrict_enrol)
        my_list_x.append(x)

    updateNotes = pd.DataFrame.from_dict(my_list_x)
    display(updateNotes[["course_id", "course_name", "note", "start_at_og", "start_at_new",
                         "end_at_og", "end_at_new", "restrict_enrol_og", "restrict_enrol_new"]])

    userConfirm = None
    while userConfirm not in ("y", "n"):

        userConfirm = input(
            "Would you like to try to update the above? (y/n)\n")
        if userConfirm == "y":
            my_list_y = []
            for index, row in df.iterrows():
                course_id = row["course_id"]
                start_at = row["start_date"]
                end_at = row["end_date"]
                y = update_course(course_id, start_at, end_at, restrict_enrol)
                my_list_y.append(y)

            update_df = pd.DataFrame.from_dict(my_list_y)
            output_df = pd.merge(update_df, updateNotes.drop(
                ["start_at_new", "end_at_new", "restrict_enrol_new"], axis=1), on="course_id")
            output_df = output_df[["course_id", "course_name", "change_success", "change_message", "note",
                                   "start_at_og", "start_at_new", "end_at_og", "end_at_new", "restrict_enrol_og", "restrict_enrol_new"]]

            return(output_df)

        elif userConfirm == "n":
            print("Update the course list and try again.")
            sys.exit(1)

        else:
            print("Please indicate if you would like to update 'y' or 'n'")


def output_csv(df):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
    output_folder = 'data/output'
    file_name = f'canvas_course_settings_{now}.csv'

    output_path = output_folder + '/' + file_name

    cprint('Details:', 'blue')
    print(f'    CSV NAME: "{file_name}""')
    print(f'    OUTPUT FOLDER: "{output_folder}"\n')

    while True:
        confirmation = input(
            "Do you want to generate the csv with these details? (y/n): ")
        if confirmation == "y":
            df.to_csv(output_path, index=False)
            cprint('\n"{}" CREATED IN "{}"'.format(
                file_name, output_folder), 'green')
            print('\nGoodbye!')
            break
        elif confirmation == "n":
            print(
                "\nCsv not created. You can run the script again or exit for no further action.\n")
            break
        else:
            print("Please enter 'y' to accept or 'n' to exit\n")
            continue

    # Copy the input CSV to /complete and timestamp
    original = f'{settings.ROOT_PATH}/data/input/start_end_courses.csv'
    target = f'{settings.ROOT_PATH}/data/complete/start_end_courses_{now}.csv'

    shutil.copyfile(original, target)

# Helpers


def check_date(date_check, date_type):
    """ Date input to change in course
    Takes an input string from user. Checks that the input follows correct format
    If format correct will give user option to double check

    Returns:
    datetime in UTC
    """

    try:
        date = datetime.datetime.strptime(date_check, "%Y-%m-%d %H:%M")
        new_date = (
            date
            .astimezone(settings.LOCAL_TIMEZONE)
            .strftime(settings.TIME_FORMAT)
        )
        return(new_date)

    except:

        try:
            d = datetime.datetime.strptime(date_check, "%Y-%m-%d")

            date_time = ''

            if date_type == "start_date":
                date_time = "{} 00:00:00".format(date_check)

            elif date_type == "end_date":
                date_time = "{} 23:59:59".format(date_check)

            d = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            new_date = d.astimezone(settings.LOCAL_TIMEZONE).strftime(
                settings.TIME_FORMAT)
           # print("\n{} was entered. This will become\n{} in Canvas.\n".format(date_check, new_date))
            return(new_date)

        except Exception as e:
          #  print("Your date was formatted incorrectly. Please check your csv and re-run.\n")
            return("No_Date")


def get_course_detail(course_id, start_at, end_at, restrict_enrol=None):
    """ Creates output for course confirmation step

    Parameters:
    course_id: user input course_id
    start_at: new start date and time for course
    end_at: new end date and time for course
    restrict_enrol: new restrict enrol, if not given then pass original


    Returns:
    A dictionary with original and change details
    """

    # create empty dictionary with course details
    # will always have course_id
    course_details = {
        "course_id": course_id,
        "course_name": None,
        "note": None,
        "start_at_og": None,
        "end_at_og": None,
        "restrict_enrol_og": None,
        "start_at_new": None,
        "end_at_new": None,
        "restrict_enrol_new": None
    }

    try:
        # access to course might be limited
        # if it is, return proper error message
        course = settings.CANVAS.get_course(course_id)
        course_details['course_name'] = course.name
        course_details['start_at_og'] = course.start_at
        course_details['end_at_og'] = course.end_at
        course_details['restrict_enrol_og'] = course.restrict_enrollments_to_course_dates

        if restrict_enrol == None:
            restrict_enrol = course.restrict_enrollments_to_course_dates

        # update course_details dictionary with new information
        start_at_new = check_date(str(start_at), "start_date")
        end_at_new = check_date(str(end_at), "end_date")
        course_details["start_at_new"] = start_at_new
        course_details["end_at_new"] = end_at_new
        course_details["restrict_enrol_new"] = restrict_enrol
        course_details["note"] = "OK" if (
            start_at_new != "No_Date" and end_at_new != "No_Date") else "Date error in start or end"

    except Exception as e:
        course_details["note"] = str(e)

    finally:
        # always return course_details dictionary
        return(course_details)


def update_course(course_id, start_at, end_at, restrict_enrol=None):
    """ Updates a course based on inputs

    Parameters:
    course_id: user input course_id
    start_at: new start date and time for course
    end_at: new end date and time for course
    restrict_enrol: new restrict enrol, if not given pass original


    Returns:
    A dictionary with original and change details
    """

    # create empty dictionary with course details
    # will always have course_id
    course_details = {
        "course_id": course_id,
        "change_success": None,
        "change_message": None,
        "start_at_new": None,
        "end_at_new": None,
        "restrict_enrol_new": None
    }

    try:
        # access to course might be limited
        # if it is, return proper error message, otherwise try update
        course = settings.CANVAS.get_course(course_id)

        try:
            # some courses you can 'see' details but can't make changes
            # try to make change but if cannot, supply message
            if restrict_enrol == None:
                restrict_enrol = course.restrict_enrollments_to_course_dates

            start_at = check_date(start_at, "start_date")
            end_at = check_date(end_at, "end_date")

            course.update(
                course={
                    "start_at": start_at,
                    "end_at": end_at,
                    "restrict_enrollments_to_course_dates": restrict_enrol
                }
            )
            # update course_details dictionary with new information
            cprint('\n{} course updated successfully'.format(
                str(course_id)), 'green')
            course_details["start_at_new"] = start_at
            course_details["end_at_new"] = end_at
            course_details["restrict_enrol_new"] = restrict_enrol
            course_details["change_success"] = True
            course_details["change_message"] = "course updated"

        except Exception as e:
            # handles exceptions past accessing original course data
            cprint('{} course not updated'.format(str(course_id)), 'red')
            course_details["change_success"] = False
            course_details["change_message"] = str(e)

    except Exception as e:
        # handles exception when no original authorization
        cprint('{} course not updated'.format(str(course_id)), 'red')
        course_details['change_success'] = False
        course_details['change_message'] = str(e)

    finally:
        # always return course_details dictionary
        return(course_details)


def create_instance(API_URL, API_TOKEN):
    '''
    Tries to create a canvas instance
    Throws an error is exception is thrown by canvasapi
    Otherwise returns canvas objects and prints Welcome {user}
    '''
    try:
        canvas = Canvas(API_URL, API_TOKEN)
        # set the validated token so it's globally accessible in settings
        user = canvas.get_user('self')
        cprint('\nToken Valid', 'green')

        first_name = user.name.split(' ')[0]
        cprint(f'\nHello {first_name}', 'blue')

        settings.TOKEN = API_TOKEN

        return canvas
    except Exception as e:
        # This is the hideous syntax for getting error messages from canvasapi Exceptions
        message = e.message[0]['message']

        # Print the error to console in red and exit
        cprint(f'\nERROR: {message}', 'red')
        sys.exit(1)
