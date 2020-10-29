# Batch Change Dates Module

Python script for the function of batch changing the start and end dates for courses listed in a CSV using Jupyter notebook interface:

1. List of courses to change with corresponding start and end dates are entered in `./data/input/start_end_courses.csv`
2. Jupyter Notebook interface will guide user through script, asking for relevant user input when necessary
3. Errors will be shown when necessary in the interface

## To Run

### Sauder Operations

_Are you Sauder Operations Staff? Please go [here](https://github.com/saud-learning-services/instructions-and-other-templates/blob/master/sauder-ops-guide-jupyter-env-and-launch.md#-ran-it-before-start-here) for detailed instructions to run in Jupyter. ("The Project", or "the-project" is "canvas-batch-change-dates" or "Canvas Batch Change Dates")._

### General (terminal instructions)

> Project uses **conda** to manage environment (See official **conda** documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file))

#### First Time

1. Ensure you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed (Python 3.7 version)
1. Clone **canvas-batch-change-dates** repository
1. Import environment (once): `$ conda env create -f environment.yml`
1. `$ conda env create -f environment.yml`

#### Every Time

1. `$ conda activate canvas-batch-change-dates`
1. `$ jupyter notebook`
1. The previous command will have opened up a tab in your browser, select 'Canvas Batch Change Dates.ipynb' and follow the instructions listed.

## Inputs for Module

1. Canvas API Token
2. start_end_courses.csv (edit file as needed)
