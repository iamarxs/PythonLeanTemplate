# Python QoL Template for Projects

A Lean template for a Python project with several quality-of-life improvements.

## What it does

- Contains a custom logger that uses LoggerAdapters instead of creating new loggers for every file.
- Makes it easy to import from different folders within the project.
- Centralizes configuration.
- Automatically reads secrets from a .env file placed at the root of the project and places them into the environment for the duration of the execution.

## What you need to do

- Uncomment .env from .gitignore when using it for actual secrets.
- Add your project configurations to config.py. Examples are provided within the file.
- In subfolders, be sure to `import __initpkg__.py` in all your files (okay, it is possible not every file will need to).
  - `from __initpkg__ import CONFIG` makes sure the configurations in config.py take place, and all project folders get inserted into PYTHONPATH. Also, the configurations in the CONFIG variable will now be accessible.

## How to run examples

- `python -m venv venv`
- Win: `source ./venv/Scripts/activate` Linux: `source ./venv/bin/activate`
- `pip install -r requirements.txt`
- `python examples/example.py`

## Free to use

- Free to use. If anyone finds the template useful, I'd be glad to know!
- <https://github.com/iamarxs/PythonLeanTemplate>
