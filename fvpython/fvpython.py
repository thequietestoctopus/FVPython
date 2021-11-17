import argparse
import os
from rich.style import Style
from rich.console import Console

task_list = []


def read_file(_file):
    if not os.path.isfile(_file):
        raise FileNotFoundError(f"'{_file}' could not be found")

    with open(_file, "r") as f:
        # for line in f.readlines():
        #     task_list.append(line)
        tasks = f.read().splitlines()
    return tasks


def main():
    # rich console printer object
    my_console = Console()

    test_style = Style(color="purple")

    # create a parser object
    parser = argparse.ArgumentParser(
        description="A CLI tool for the FVP time management algorithm"
    )

    parser.add_argument(
        "File",
        type=str,
        nargs=1,
        metavar="<FILE>",
        default=None,
        help="Text file to be used as task list",
    )

    args = parser.parse_args()

    if args.File != None:
        print(args.File[0])
        task_list = read_file(args.File[0])

    # testing input in terminal
    input_test = input("Proceed? [y/n]: ")
    if input_test == "y":
        for t in task_list:
            # print(f" ·  {t}")
            my_console.print(f" x  {t}", style=test_style)
    elif input_test == "n":
        print("Quitting...")
    else:
        print("Invalid response")


if __name__ == "__main__":
    main()
