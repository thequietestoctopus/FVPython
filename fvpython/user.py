import sys


class InputHandler:
    """Responsible for communicating with, and executing commands given by, user"""

    def prompt_for_input(self, active, benchmark):
        query = "Do you want to {} more than {}?".format(active, benchmark)
        response = input(f"{query} [y/n]: ")
        if response == "y":
            return True
        elif response == "n":
            return False
        elif response == "q":
            sys.exit()
