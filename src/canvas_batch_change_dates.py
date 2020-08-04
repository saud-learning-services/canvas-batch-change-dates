
""" This Script
This script has everything needed to update canvas course settings
## is a real comment
# is a commented out piece of code that would be needed to run this script alone
These pieces of code are provided by the appropriate Jupyter notebook

"""

from canvasapi import Canvas
import datetime, sys, pytz, getpass, os
import pandas as pd
from IPython.display import display, HTML
from helpers import createInstance, getCourseFromID, createCSV


""" User entry of date changes used for start and end date
local variable is set to Pacific timezone (Vancouver)
fmt is the format for output

API_URL - should be set in jupyter
API_KEY - should be set in jupyter
FOLDER = "Canvas Course Settings"
INPUT = "{}/input".format(FOLDER)
OUTPUT = "{}/output".format(FOLDER)
LOGS = "{}/logs".format(FOLDER)

"""
local = pytz.timezone("Canada/Pacific")
fmt = "%Y-%m-%d %I:%M:%S %p %Z%z"
successKey = "Everything should have worked!"

FOLDER = os.path.join(os.getcwd(), "src\csv")
INPUT = os.path.join(FOLDER,"input")
OUTPUT = os.path.join(FOLDER,"output")
COMPLETE = os.path.join(FOLDER,"complete")
print(INPUT)

API_URL = "https://ubc.test.instructure.com/"
#API_KEY = ""
#canvas = createInstance(API_URL, API_KEY)
#API_KEY = getpass.getpass("Enter token: ")
API_KEY = input("Enter token: ")
canvas = createInstance(API_URL, API_KEY.strip())

def checkDate(date_check, date_type):
    """ Date input to change in course
    Takes an input string from user. Checks that the input follows correct format
    If format correct will give user option to double check

    Returns:
    datetime in UTC
    """

    try:
        d = datetime.datetime.strptime(date_check, "%Y-%m-%d %H:%M")
        new_date = d.astimezone(local).strftime(fmt)
       # print("\n{} was entered. This will become\n{} in Canvas.\n".format(date_check, new_date))
        return(new_date)

    except:

        try:
            d = datetime.datetime.strptime(date_check, "%Y-%m-%d")

            if date_type == "start_date":
                date_time = "{} 00:00:00".format(date_check)

            elif date_type == "end_date":
                date_time = "{} 23:59:59".format(date_check)

            d = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            new_date = d.astimezone(local).strftime(fmt)
           # print("\n{} was entered. This will become\n{} in Canvas.\n".format(date_check, new_date))
            return(new_date)

        except Exception as e:
          #  print("Your date was formatted incorrectly. Please check your csv and re-run.\n")
            return("No_Date")

def getCoursesFile(file):
    """Tries to find supplied file
    and creates appropriate dataframe from file

    parameters:
    file (String): the name of the file with courses

    returns:
    df (Dataframe): dataframe with course ids
    """

    try:
        ## read file
        df = pd.read_csv(file)
        print("Successful load of csv file\n\n{}\n".format(df[["course_id", "start_date", "end_date"]]))

        return(df)

    except IOError as e:
        ## file not found
        print(e)
        print("\nYou should have the file indicated above in the same folder\
            \nas this notebook: {}\n".format(os.getcwd()))
        sys.exit(1)
    except KeyError as ke:
        ## file doesn't have course ids
        print(ke)
        print("\nThe file {} should have the columns course_id, start_date, and end_date.\n".format(file))
        sys.exit(1)

## Get appropriate course information
## If cannot get course information - then probably can't do other things either

def getCourseDetail(course_id, start_at, end_at, restrict_enrol=None):
    """ Creates output for course confirmation step

    Parameters:
    course_id: user input course_id
    start_at: new start date and time for course
    end_at: new end date and time for course
    restrict_enrol: new restrict enrol, if not given then pass original


    Returns:
    A dictionary with original and change details
    """

    ## create empty dictionary with course details
    ## will always have course_id
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
        ## access to course might be limited
        ## if it is, return proper error message
        course = canvas.get_course(course_id)
        course_details['course_name'] = course.name
        course_details['start_at_og'] = course.start_at
        course_details['end_at_og'] = course.end_at
        course_details['restrict_enrol_og'] = course.restrict_enrollments_to_course_dates


        if restrict_enrol == None:
            restrict_enrol = course.restrict_enrollments_to_course_dates

        ## update course_details dictionary with new information
        start_at_new= checkDate(str(start_at), "start_date")
        end_at_new = checkDate(str(end_at), "end_date")
        course_details["start_at_new"] = start_at_new
        course_details["end_at_new"] = end_at_new
        course_details["restrict_enrol_new"] = restrict_enrol
        course_details["note"] = "OK" if (start_at_new!= "No_Date" and end_at_new!="No_Date") else "Date error in start or end"


    except Exception as e:
        course_details["note"] = str(e)

    finally:
        ## always return course_details dictionary
        return(course_details)


def updateCourse(course_id, start_at, end_at, restrict_enrol=None):
    """ Updates a course based on inputs

    Parameters:
    course_id: user input course_id
    start_at: new start date and time for course
    end_at: new end date and time for course
    restrict_enrol: new restrict enrol, if not given pass original


    Returns:
    A dictionary with original and change details
    """

    ## create empty dictionary with course details
    ## will always have course_id
    course_details = {
        "course_id": course_id,
        "change_success": None,
        "change_message": None,
        "start_at_new": None,
        "end_at_new": None,
        "restrict_enrol_new": None
    }

    try:
        ## access to course might be limited
        ## if it is, return proper error message, otherwise try update
        course = canvas.get_course(course_id)

        try:
            ## some courses you can 'see' details but can't make changes
            ## try to make change but if cannot, supply message
            if restrict_enrol == None:
                restrict_enrol = course.restrict_enrollments_to_course_dates

            start_at = checkDate(start_at, "start_date")
            end_at = checkDate(end_at, "end_date")

            course.update(
                course={
                    "start_at": start_at,
                    "end_at": end_at,
                    "restrict_enrollments_to_course_dates": restrict_enrol
                }
            )
            ## update course_details dictionary with new information
            print('{} course updated successfully'.format(str(course_id)))
            course_details["start_at_new"] = start_at
            course_details["end_at_new"] = end_at
            course_details["restrict_enrol_new"] = restrict_enrol
            course_details["change_success"] = True
            course_details["change_message"] = "course updated"

        except Exception as e:
            ## handles exceptions past accessing original course data
            print("{} course not updated".format(str(course_id)))
            course_details["change_success"] = False
            course_details["change_message"] = str(e)

    except Exception as e:
        ## handles exception when no original authorization
        print("{} course not updated".format(str(course_id)))
        course_details['change_success'] = False
        course_details['change_message'] = str(e)

    finally:
        ## always return course_details dictionary
        return(course_details)

def updateMultipleCourses(df, restrict_enrol=None):
    """iterates on df of course lists and creates a list of update details"""

    my_list_x = []

    for index, row in df.iterrows():
        course_id = row["course_id"]
        start_at = row["start_date"]
        end_at = row["end_date"]

        x = getCourseDetail(course_id, start_at, end_at, restrict_enrol)
        my_list_x.append(x)

    updateNotes = pd.DataFrame.from_dict(my_list_x)
    display(updateNotes[["course_id", "course_name", "note", "start_at_og", "start_at_new", "end_at_og", "end_at_new", "restrict_enrol_og", "restrict_enrol_new"]])

    userConfirm = None
    while userConfirm not in("y", "n"):

        userConfirm = input("Would you like to try to update the above? (y/n)\n")
        if userConfirm == "y":
            my_list_y = []
            for index, row in df.iterrows():
                course_id = row["course_id"]
                start_at = row["start_date"]
                end_at = row["end_date"]
                y = updateCourse(course_id, start_at, end_at, restrict_enrol)
                my_list_y.append(y)

            update_df = pd.DataFrame.from_dict(my_list_y)
            output_df = pd.merge(update_df, updateNotes.drop(["start_at_new", "end_at_new", "restrict_enrol_new"], axis=1), on="course_id")
            output_df = output_df[["course_id", "course_name", "change_success", "change_message", "note", "start_at_og", "start_at_new", "end_at_og", "end_at_new", "restrict_enrol_og", "restrict_enrol_new"]]

            return(output_df)

        elif userConfirm == "n":
            print("Update the course list and try again.")
            sys.exit(1)

        else:
            print("Please indicate if you would like to update 'y' or 'n'")
