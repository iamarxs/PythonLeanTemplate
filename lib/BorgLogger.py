"""
A configurable logger that can be used to pull new LoggerAdapters instead of creating new loggers
for every module.
"""

import contextlib

# pylint: disable=W0212
import logging
import sys
import traceback
from pathlib import Path

from config import CONFIG, ROOT_DIR


def _customFormatException(exc_info):
    """Formats the exception information into a tuple."""

    error = str(exc_info[0]).split("'", maxsplit=2)[1]
    return (exc_info[2].tb_lineno, error, exc_info[1], exc_info[0].__doc__)


def detailed_exception(exc_info):
    """
    Prints detailed tracebacks inside exceptions. A logger.critical replacement,
    which is why exc_info is included though not used here.
    """
    err_file = Path(traceback.extract_stack(exc_info[2].tb_frame, limit=1)[0][0])
    with contextlib.suppress(ValueError):
        err_file.relative_to(ROOT_DIR)
        err_file = f"{err_file.parts[-2]}/{err_file.parts[-1]}"
    line, error, error_text, description = _customFormatException(exc_info)
    return f"Exception in {err_file}:{line} - {error} - {error_text} - {description}"


class BorgLogger:
    """
    A custom logger "manager" class that provides a shared logger instance.

    This class implements a singleton pattern to ensure that only one logger instance is created.
    The logger can be configured with a specified log level, log file path, and log format.
    """

    _shared_state = {
        "name": CONFIG.LOGGERNAME,
        "main_logger": None,
        "root_level": CONFIG.LOG_LEVEL,
        "log_file_path": Path(CONFIG.LOG_PATH),
        "log_file_name": Path(f"{CONFIG.LOG_FILE}.log"),
    }

    def __new__(cls, config=None):
        """
        Overwrite __new__, which usually handles the object creation before __init__
        """
        if isinstance(config, dict):
            for key, value in config.items():
                if key in cls._shared_state:
                    cls._shared_state[key] = value

        if not cls._shared_state["main_logger"]:
            cls._config_logger()
        return cls
        # return cls._shared_state["main_logger"]

    @classmethod
    def _config_logger(cls):
        """
        Configure the main logger with the specified log level, log file path, and log format.

        This method sets up the main logger by creating file and console handlers with the
        specified log level. The log format includes the timestamp, logger name, log level,
        process name, filename, line number, and log message.
        """
        root_level = cls._shared_state["root_level"]
        # Use the logging module's internal function to validate given log level.
        # Raises an exception if not valid.
        logging._checkLevel(root_level)
        log_file_path = cls._shared_state["log_file_path"] / cls._shared_state["log_file_name"]
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S]",
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(root_level)

        # Console output should be slightly more ascetic.
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
            datefmt="[%H:%M:%S]",
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(root_level)

        # Create the main logger.
        # main_logger = logging.getLogger(cls._shared_state["name"])
        main_logger = CustomLogger(cls._shared_state["name"])
        main_logger.addHandler(console_handler)
        main_logger.addHandler(file_handler)
        main_logger.setLevel(root_level)
        # main_logger.exception = logger_exception
        cls._shared_state["main_logger"] = main_logger

    @classmethod
    def get_logger(cls):
        """
        Get the shared instance of the logger.
        """

        if not cls._shared_state["main_logger"]:
            cls._config_logger()
        return cls._shared_state["main_logger"]

    @classmethod
    def get_adapter(cls, context_info=None):
        """
        Get a logger adapter with the specified context information.
        THIS IS THE PREFERRED METHOD TO PULL NEW LOGGERS (adapters) TO USE!

        Args:
            context_info: Additional context information to be included in log messages.
        """

        if not cls._shared_state["main_logger"]:
            cls._config_logger()
        return ContextAdapter(cls._shared_state["main_logger"], context_info)


class CustomLogger(logging.Logger):
    """A custom logger class that extends the logging.Logger class.

    This class modifies the exception log message
    to include detailed exception information when necessary.
    """

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        kwargs["extra"]["is_exception"] = True
        super().error(msg, *args, exc_info=exc_info, **kwargs)

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=2):
        """
        Log a message at the specified level.

        This method is called to log a message at the specified level.
        If the `extra` argument is a dictionary and it contains the key "is_exception",
        the log message is modified to include detailed exception information.
        """

        if isinstance(extra, dict) and "is_exception" in extra:
            msg = f"{msg} [{detailed_exception(sys.exc_info())}]"
            stacklevel += 1
        super()._log(
            level,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )


class ContextAdapter(logging.LoggerAdapter):
    """
    Adapters are a class of pseudologgers that point to an actual logger and use that, but also
    carry some extra contextual info with them.

    This class subclasses the actual LoggerAdapter class and overwrites the "process"
    method so that it can handily insert our context data into the message about to be logged.

    The extra data can either be in the form of a dict, list or a string.

    During initialization, you can give the extra context info with
    ``logger = ContextAdapter(logger, extra: Union[list, dict, str, None]=extra_info)``

    """

    def process(self, msg, kwargs):
        """
        Add the context info in front of the regular message so no other
        special handling needs to be done.

        Returns:
            Modified message that includes the context info in [] brackets in front of the
            original msg if info has been provided, otherwise returns the original message.
        """
        if isinstance(self.extra, dict):
            context_text = str(f"{key}: {value}, " for key, value in self.extra.items())
            context_text = context_text[:-2]
            msg = f"[{context_text}] {msg}"
        elif isinstance(self.extra, str):
            msg = f"[{self.extra}] {msg}"
        return msg, kwargs

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        Flag the error message as an exception, so that more info can be added to the message later.
        """
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        kwargs["extra"]["is_exception"] = True
        super().exception(msg, *args, exc_info=exc_info, **kwargs)
