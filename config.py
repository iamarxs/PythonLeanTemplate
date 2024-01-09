"""
Common configurations
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv

LOGGERNAME = "LeanPython"
LOG_FOLDER = "logs"

LOG_LEVEL = logging.DEBUG if "-d" in sys.argv else logging.INFO

# For this to work, config.py must be in the root folder of the project.
ROOT_DIR = Path(__file__).resolve().parents[0]

# Add all project folders here. Check the bottom of the file for why.
LIB_DIR = ROOT_DIR / "lib"
PROJECT_PATHS = [LIB_DIR, ROOT_DIR]


def read_next_argument(arg):
    """
    Checks for a specific argument in sys.argv and reads the next argument into a variable.
    Args:
        arg (str): The argument to search for in sys.argv.

    Returns:
        str or None: The value of the next argument if found, None otherwise.

    """
    if arg not in sys.argv:
        return None
    try:
        return int(sys.argv[sys.argv.index(arg) + 1])
    except IndexError:
        return None


# If we want to give a parameter from command line, we can use the read_next_argument function to
# read the next argument from what's configured here. In the below example, --somenumber 15
# would set SOME_CMD_ARGUMENT_WITH_PARAM variable to 15. If no cmd argument is given, or is faulty,
# the default is used.
SOME_CMD_ARG_WITH_PARAM = read_next_argument("--somenumber") or 10

# --date includes a datetime as a suffix to our log file.
LOG_FILE = LOGGERNAME + (
    datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
    if len(sys.argv) > 1 and "--date" in sys.argv
    else ""
)

# Variables can easily be set to boolean values from command line, as in the below example.
# If no -b argument is given, BOOLEAN_EXAMPLE will be set to False, otherwise True.
BOOLEAN_EXAMPLE = "-b" in sys.argv

# Create the log path if it does not exist
LOG_PATH = ROOT_DIR / LOG_FOLDER
LOG_PATH.mkdir(exist_ok=True)

# A handy SimpleNamespace object that can be imported from this file, that will contain
# all required project configurations. An easy way to keep th configs in one location.
# i.e.
# from config import CONFIG
#
# ...
#
# if CONFIG.BOOLEAN_EXAMPLE:
#    *do stuff if CONFIG.BOOLEAN_EXAMPLE is True*

PRINT_HELP = """
    \033[1m\033[92mCommand line arguments:

    Project options:
    --somenumber <number>        Set SOME_CMD_ARG_WITH_PARAM variable to <number> Default is 10.
    -b                           Set BOOLEAN_EXAMPLE to True. Defaults to False.

    Logging configurations:
    -d                           Set logging level to DEBUG. Defaults to INFO.
    --date                       Suffix the log file with a date
    \033[0m
    """

PRINT_MENU = """
    \033[96m
    1) Print help
    2) Pretty print CONFIG - Test out different command line arguments and see the changes
    3) Check the environment for any .env imports
    4) Demonstrate BorgLogger and importing from other subfolders of the project
    5) Quit
    \033[0m
    """

PRINT_LOGGER_DEMO_MENU = """
    \033[95m
    1) Demonstrate LoggerAdapter
    2) Demonstrate using the actual Logger
    3) Demonstrate exception errors
    4) Back
    \033[0m
    """

CONFIG = SimpleNamespace(
    LOG_LEVEL=LOG_LEVEL,
    LOG_PATH=LOG_PATH,
    LOG_FILE=LOG_FILE,
    LOGGERNAME=LOGGERNAME,
    BOOLEAN_EXAMPLE=BOOLEAN_EXAMPLE,
    SOME_CMD_ARG_WITH_PARAM=SOME_CMD_ARG_WITH_PARAM,
    PRINT_HELP=PRINT_HELP,
    PRINT_MENU=PRINT_MENU,
    PRINT_LOGGER_DEMO_MENU=PRINT_LOGGER_DEMO_MENU,
)

# Load the .env file secrets into the run-time environment,
# if it exists.
# This gets executed immediately as anything from config.py is imported.
# i.e.
# from config import CONFIG
# variable = os.getenv("WHATEVER_VARIABLE_WAS_IN_DOT_ENV_FILE")
#
# No need to explicitly run load_dotenv anywhere else.
DOTENV_FILE = ROOT_DIR / ".env"
if DOTENV_FILE.exists() and DOTENV_FILE.is_file():
    load_dotenv(dotenv_path=DOTENV_FILE)


# Pulling hairs from your head, trying to get relative imports to work?
# If you filled the PROJECT_PATHS list at the top of the file with all subfolders of your project,
# importing anything from config.py results in all those folders being added to PYTHONPATH.
# i.e.
# Want to import lib/BorgLogger.py from res/tools.py?
# No problem! Just "from BorgLogger import BorgLogger" anywhere within the project folders works.


def project_to_path() -> None:
    # pylint: disable=W1203
    """
    Sets the import paths for the project.
    """
    for path in PROJECT_PATHS:
        if path not in sys.path:
            sys.path.insert(0, str(path))


project_to_path()
