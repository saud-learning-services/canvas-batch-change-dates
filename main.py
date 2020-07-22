from src.interface import get_user_inputs
from termcolor import cprint
import src.settings as settings

def main():

    # initialize global variables - call only once
    settings.init()

    # get user inputs
    url, course_id, quiz_id = get_user_inputs()

    cprint('ACCESS USER INPUTS RETURNED BY get_user_inputs() LIKE THIS:', 'blue')
    print(f'URL: {url}')
    print(f'COURSE ID: {course_id}')
    print(f'QUIZ ID: {quiz_id}')

    print('\n=================================\n')

    cprint('ACCESS GLOBAL VARIABLES FROM SETTINGS MODULE LIKE THIS:', 'blue')
    print(f'Course name: {settings.course.name}')
    print(f'Quiz name: {settings.quiz.title}')


if __name__ == "__main__":
    main()
