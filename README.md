# Canvas Batch Change Dates

> - name: canvas-batch-change-dates
> - ops-run-with: jupyter
> - python>=3.7
> - canvasapi>=2.0.0

## Summary

**Canvas Batch Change Dates** is a Python script for changing the start/end dates for courses. This script can process multiple courses at once - all courses and start/end dates can be adjusted to preference in `./data/input/start_end_courses.csv`.

## Inputs

1. `start_end_courses.csv`: List all courses by id and enter start and end date values in respective columns

   > ex. to change course (12345) to begin Jan-01-2020 and end Jan-01-2021 we'd enter:

   | course_id | start_date |   end_date |
   | :-------- | :--------: | ---------: |
   | 12345     | 2020-01-01 | 2021-01-01 |

1. **Canvas API Token**: Found in _Canvas > Account > Settings > Approved Integrations_ (prompted by the Jupyter Notebook)

## Output

1. `./data/output/canvas-course-settings_{YYYY-MM-DD HH.MM.SS}.csv`: Details status of last run including affected courses, original start/end dates, new start/end dates and any changes to enrollment restrictions
2. `./data/completed/start_end_courses_{YYYY-MM-DD HH.MM.SS}`: This is a copy of your `start_end_courses.csv` copied over at the end of the run and timestamped. These will automatically get stored in the `./data/complete` folder.

## ⚠️ Important Caveats

- **The changes applied here can be difficult to reverse, so ensure all documentation (README.md and Jupyter Notebook) has been looked at and understood before running**
- The Jupyter Notebook will create a few additional prompts to get the API Token and confirm outcomes

## Getting Started

### Sauder Operations

_Are you Sauder Operations Staff? Please go [here](https://github.com/saud-learning-services/instructions-and-other-templates/blob/master/sauder-ops-guide-jupyter-env-and-launch.md#-ran-it-before-start-here) for detailed instructions to run in Jupyter. ("The Project", or "the-project" is "canvas-batch-change-dates" or "Canvas Batch Change Dates")._

### General (terminal instructions)

> Project uses **conda** to manage environment (See official **conda** documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file))

#### First Time

1. Ensure you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed (Python 3.7 version)
1. Clone **canvas-batch-change-dates** repository
1. Import environment (once): `$ conda env create -f environment.yml`

#### Every Time

1. Run
   1. `$ conda activate canvas-batch-change-dates`
   1. `$ jupyter notebook`
   1. The previous command will have opened up a tab in your browser, select 'Canvas Batch Change Dates.ipynb' and follow the instructions listed.
