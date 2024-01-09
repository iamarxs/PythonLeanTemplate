"""Example script that demonstrates the quality of life helpers introduced in this repo."""
import msvcrt
from os import getenv
from pprint import pprint

from __initpkg__ import CONFIG

# pylint: disable=E0401
from lib.BorgLogger import BorgLogger

# Thanks to __initpkg__, also
# from BorgLogger import BorgLogger
# works!


class ExampleClass:
    """
    A class that demonstrates various functionalities and interactions.

    This class demonstrates the usage of the singleton logger and its adapter
    and the centralized config.
    """

    def __init__(self) -> None:
        """Initialize the ExampleClass instance."""

        self.actions = [
            self.print_menus,
            self.pretty_print_config,
            self.check_env,
            self.demonstrate_borg_logger,
            self.exit,
        ]

        self.logger_demo_actions = [
            self.demo_logger_adapter,
            self.demo_logger_actual,
            self.demo_exception_errors,
        ]

    @staticmethod
    def print_menus(text=CONFIG.PRINT_HELP):
        """Print the given menu/help text."""
        print(text)

    @staticmethod
    def demo_logger_adapter():
        """
        Demonstrate the usage of a logger adapter.

        This method demonstrates the creation and usage of a logger adapter.
        It shows how to create a logger adapter and log messages using it.
        """

        print("Let's create a logger adapter. A logger adapter is a 'wrapper' to an actual logger.")
        print("The BorgLogger uses a singleton class that only creates a single actual logger.")
        print("The preferred method for modules is to import an adapter for that logger, then")
        print("use that as one would a regular logger. Let's create a Loggeradapter.")
        print("No need to worry if the actual logger has been instantiated. If not,")
        print("it will be configured in the background, before serving the adapter to us.")
        print("Syntax: logger_adapter = BorgLogger.get_adapter(context_info='context info here')")
        user_given_context = input(
            "\033[1mPlease enter a context text to be added to the adapter: "
        )
        print("\033[0m")
        logger_adapter = BorgLogger.get_adapter(context_info=user_given_context)
        logger_adapter.info("Hello! This is the BorgLogger adapter from example.py!")
        logger_adapter.warning("This is a warning")
        logger_adapter.error("This is an error")
        logger_adapter.debug("This gets only logged if -d was given as a cmd arg")

    @staticmethod
    def demo_logger_actual():
        """
        Demonstrate the usage of the actual logger.

        This method demonstrates the usage of the actual logger.
        It shows how to import the actual logger and log messages using it.
        """

        print("If, for some reason, we need the actual logger, we can import that as well.")
        print("Syntax: logger = BorgLogger.get_logger()")
        logger = BorgLogger.get_logger()
        logger.info("This is the actual logger logging, not the addapter.")
        logger.warning("This is a warning")
        logger.error("This is an error")
        logger.debug("This gets only logged if -d was given as a cmd arg")

    @staticmethod
    def demo_exception_errors():
        """
        Demonstrate exception errors and logging.

        This method demonstrates causing exceptions and logging error messages.
        It shows how to handle exceptions and log detailed error messages.
        """

        print("Let's cause some exceptions with out BorgLogger and see the info provided")
        print("We'll print an exception log message both with the actual logger, and the addapter.")
        print("\033[1mLet's try. Press any key to continue.\033[0m\n")
        msvcrt.getch()
        logger = BorgLogger.get_logger()
        logger_adapter = BorgLogger.get_adapter(context_info="Exception Adapter")
        try:
            1 / 0
        except ZeroDivisionError:
            logger.exception(
                "Whoa there! You just tried to divide by zero. We checked with the math wizards, "
                "and they said this is how black holes start. To avoid being sucked into a cosmic "
                "void, let's try a number that actually exists in this dimension!",
            )
            print()
            logger_adapter.exception(
                "Oops! It seems you tried to divide by zero. "
                "Our servers are currently hiding in a bunker from the mathematical apocalypse "
                "you almost caused. Please use a non-zero number to keep the universe intact!"
            )
        print("\nHandy. If the traceback is not needed, we can clean up the message a bit.")
        print("Simply provide use exc_info=False when calling the exception from either logger.")
        print("Syntax: logger_adapter.exception('Oh noes, an exception!', exc_info=False)")
        print("\033[1mLet's try. Press any key to continue.\033[0m\n")
        msvcrt.getch()
        try:
            1 / 0
        except ZeroDivisionError:
            logger.exception(
                "Error 404: Division by zero. This number is on a coffee break. "
                "Please try a different one!",
                exc_info=False,
            )
            print()
            logger_adapter.exception(
                "Divide by zero attempt detected. Quick, grab a calculator! "
                "This isn't a job for mere mortals.",
                exc_info=False,
            )
        print("\nA bit neater, if the traceback is not required!\n")

    def demonstrate_borg_logger(self):
        """
        Demonstrate the usage of the BorgLogger.

        This method presents a menu and performs actions based on user input.
        It demonstrates the usage of the BorgLogger.
        """

        while True:
            self.print_menus(CONFIG.PRINT_LOGGER_DEMO_MENU)
            user_input = input("\033[1mPlease enter a valid number: ")
            print("\033[0m")  # Clear text bolding and handily give a newline before action.
            if user_input.isdigit() and 1 <= int(user_input) <= len(self.logger_demo_actions) + 1:
                if int(user_input) == len(self.logger_demo_actions) + 1:
                    return
                self.logger_demo_actions[int(user_input) - 1]()

    @staticmethod
    def pretty_print_config():
        """
        Pretty print the configuration.

        This method pretty prints the configuration.
        It shows how to access and print the configuration values, derived from the centralized
        config.
        """

        pprint(CONFIG)
        print("\nCan be used as such: log_level=CONFIG.LOG_LEVEL\n")
        print(f"Has -b been given as a command line argument? {CONFIG.BOOLEAN_EXAMPLE=}\n")

    def check_env(self):
        """
        Check environment variables.

        This method demonstrates how importing anything from config.py automatically injects the
        variables from the .env file within the project root into the run-time environment.
        """

        print("Is SECRET_API_TOKEN loaded into ENV?")
        if secret := getenv("SECRET_API_TOKEN"):
            print(f"Yes it is! Contents: {secret}")
        else:
            print("Nope :(")
        print("Is USER loaded into ENV?")
        if secret := getenv("USER"):
            print(f"Yes it is! Contents: {secret}")
        else:
            print("Nope :(")
        print("Is PASSWORD loaded into ENV?")
        if secret := getenv("PASSWORD"):
            print(f"Yes it is! Contents: {secret}")
        else:
            print("Nope :(")

    @staticmethod
    def exit():
        """Exits demonstration script"""
        print("Goodbye!")
        exit()

    def main_loop(self):
        """
        Main loop of the example program.

        This method runs the main loop of the program.
        It presents a menu and performs actions based on user input.
        """

        while True:
            self.print_menus(CONFIG.PRINT_MENU)
            user_input = input("\033[1mPlease enter a valid number: ")
            print("\033[0m")  # Clear text bolding and handily give a newline before action.
            if user_input.isdigit() and 1 <= int(user_input) <= len(self.actions):
                self.actions[int(user_input) - 1]()


if __name__ == "__main__":
    example = ExampleClass()
    example.main_loop()
