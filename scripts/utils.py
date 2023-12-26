import os
import logging
import inspect
import requests
from bs4 import BeautifulSoup
# import pickle
from markdownify import markdownify as md

class year_folder_setup:
    """
    A class that handles the initialization of the year folder structure for Advent of Code.
    """

    def initialize_year(year):
        """
        Initializes the year folder structure for the given year.

        Parameters:
        - year (str): The year for which the folder structure needs to be initialized.
        """

        year_folder = os.path.join(os.getcwd(), "year", str(year))
        log_file = os.path.join(os.getcwd(), "log.txt")

        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(pathname)s - %(message)s')

        if os.path.exists(year_folder):
            logging.info(f"Skipped creating year folder {year_folder} as it already exists.")
            return

        os.makedirs(year_folder)
        logging.info(f"Created folder for year {year}.")

        scripts_folder = os.path.join(year_folder, "scripts")
        if os.path.exists(scripts_folder):
            logging.info(f"Skipped creating scripts folder {scripts_folder} as it already exists.")
        else:
            os.makedirs(scripts_folder)
            with open(os.path.join(scripts_folder, "__init__.py"), 'w'):
                pass
            logging.info(f"Created scripts folder: {scripts_folder}")

        tests_folder = os.path.join(year_folder, "tests")
        if os.path.exists(tests_folder):
            logging.info(f"Skipped creating tests folder {tests_folder} as it already exists.")
        else:
            os.makedirs(tests_folder)
            logging.info(f"Created tests folder: {tests_folder}")

        day_folder = os.path.join(year_folder, "day")
        if os.path.exists(day_folder):
            logging.info(f"Skipped creating day folder {day_folder} as it already exists.")
        else:
            os.makedirs(day_folder)
            logging.info(f"Created day folder: {day_folder}")

            # Create folders 1 to 25 within the day folder
            for day in range(1, 26):
                day_folder_number = os.path.join(day_folder, str(day))
                if os.path.exists(day_folder_number):
                    logging.info(f"Skipped creating folder {day_folder_number} as it already exists.")
                else:
                    os.makedirs(day_folder_number)
                    with open(os.path.join(day_folder_number, "__init__.py"), 'w'):
                        pass
                    with open(os.path.join(day_folder_number, "notebook.ipynb"), 'w'):
                        pass
                    with open(os.path.join(day_folder_number, "solution.py"), 'w'):
                        pass
                    with open(os.path.join(day_folder_number, "README.md"), 'w'):
                        pass
                    path = f'{os.path.join(year_folder)}/day/{str(day)}'
                    day_folder_setup.make_markdown(day, year, path)
                    print(path)
                    logging.info(f"Created folder {day_folder_number} and added empty files.")


class day_folder_setup:
    @staticmethod
    def get_day_year(stack_index=1):
        caller_frame = inspect.stack()[stack_index]
        caller_path = caller_frame.filename
        calling_dir = os.path.dirname(caller_path)
        path_parts = calling_dir.split(os.sep)
        day = path_parts[-1]
        year = path_parts[-3]
        return day, year, calling_dir
    
    def get_description(day, year):
              
        url = f'https://adventofcode.com/{year}/day/{day}'
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        desription = soup.find('article')
        description_md = md(str(desription))
        first_sentence = description_md.find('-')
        if first_sentence != -1:
            description_md = '## ' + description_md[:first_sentence + 1] + description_md[first_sentence + 1:]
        return url, description_md
    
    @staticmethod
    def make_markdown(day, year, path):
        #day, year, calling_dir = day_folder_setup.get_day_year(stack_index=2)
        url, description_md = day_folder_setup.get_description(day, year)
        with open(os.path.join(path, 'Task description.md'), 'w') as td:
            td.write(f'# AoC - Task description day {day}\n')
            td.write(f'`{url}`\n')
            td.write(f'---\n')
            td.write(f'{description_md}')