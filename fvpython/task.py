import sys
from rich import color
from rich import style
import shortuuid
from rich.style import Style
from rich.console import Console


class Task:
    """An individual task object within the FVP task list.

    Args:
        id_ (int): The uuid (universally unique identifier) of this task
        content (str): The textual content of the task entered by and displayed back to the user
        marked (bool, optional): Whether the task has been marked by the user, for formatting purposes
        completed (bool, optional): Whether the task has been identified as completed, for formatting purposes
        deleted (bool, optional): Whether the task has been identified as being not relevant, for formatting purposes
    """

    def __init__(self, id_, content, marked=False, completed=False, deleted=False):
        self.id_: int = id_
        self.content: str = content
        self.marked: bool = marked
        self.completed: bool = completed
        self.deleted: bool = deleted

    def mark(self):
        self.marked = True

    def complete(self):
        self.completed = True


class TaskList:
    """The FVP task list object containing the tasks entered by the user and information about their states."""

    def __init__(self, entries):
        """
        Attributes:
            entries: list of Task objects
            active: current task meant to be completed by the user
            benchmark: most recently marked task
            last_completed: the most recently completed task
        """
        self.entries = self.list_generation(entries)
        self._active = None
        self._benchmark = None
        # TODO: append completed tasks into list and evaluate last_completed as completed[-1]
        self.last_completed = None
        self.completed_tasks = []

    def list_generation(self, input_tasks):
        """Takes in unformatted list of tasks as strings and returns them as a shuffled list of Task objects"""
        output_tasks = []
        for t in input_tasks:
            su = shortuuid.uuid()
            con = str(t)
            output_tasks.append(Task(su, con))
        return output_tasks

    @property
    def active(self):
        """Get active task object"""
        return self._active

    @active.setter
    def active(self, task):
        self._active = task

    @property
    def benchmark(self):
        """Get current benchmark task object"""
        return self._benchmark

    @benchmark.setter
    def benchmark(self, task):
        self._benchmark = task

    def get_index(self, task):
        return self.entries.index(task)

    def rich_print(self):
        COLOR = "blue"
        SYM_DEFAULT = "   "
        SYM_MARKED = " · "
        SYM_COMPLETED = " x "
        SYM_ACTIVE = " > "
        STANDARD = Style(color=COLOR)
        DIMMED = Style(color=COLOR, dim=True)
        STRIKETHROUGH = Style(color=COLOR, dim=True, strike=True)
        BOLD = Style(color=COLOR, bold=True)
        CONSOLE = Console()

        def print_task(symbol, text, text_style=STANDARD, symbol_style=STANDARD):
            CONSOLE.print("{}".format(symbol), style=symbol_style, end="")
            CONSOLE.print("{}".format(text), style=text_style)

        for e in self.entries:
            if e.deleted:
                print_task(SYM_DEFAULT, e.content, text_style=STRIKETHROUGH)
            elif e.completed:
                print_task(SYM_COMPLETED, e.content, text_style=DIMMED)
            elif e.marked:
                print_task(SYM_MARKED, e.content, symbol_style=BOLD)
            elif e == self._active:
                print_task(SYM_ACTIVE, e.content, text_style=BOLD)
            else:
                print_task(SYM_DEFAULT, e.content)

    def entry_count(self):
        """Returns total number of contained task objects as int"""
        return len(self.entries)

    def incomplete(self):
        incomplete_tasks = [i for i in self.entries if not i.completed]
        return incomplete_tasks

    def incomplete_count(self):
        """Returns number of contained tasks yet to be marked as completed as int"""
        incomplete_tasks = self.incomplete()
        return len(incomplete_tasks)

    def marked_tasks(self):
        marked_tasks = [i for i in self.entries if i.marked and not i.completed]
        return marked_tasks

    def bottom_marked(self):
        """Returns the lowest (highest index) task that is both marked and incomplete"""
        marked_tasks = self.marked_tasks()
        bottom_marked = max(marked_tasks, key=lambda x: self.get_index(x))
        return bottom_marked

    def end_of_list(self, task):
        """Return True if no incomplete tasks are lower than the input task in entry list"""
        task_index = self.get_index(task)
        incomplete_tasks = self.incomplete()
        lowest_task = max(incomplete_tasks, key=lambda x: self.get_index(x))
        lowest_task_index = self.get_index(lowest_task)
        if task_index >= lowest_task_index:
            return True
        else:
            return False

    def prompt_for_input(self, task_in_focus):
        affirmative = {"y", "yes"}
        negative = {"n", "no"}
        exit_script = {"q", "quit"}
        display_tasks = {"l", "list"}
        help_menu = {"h", "help"}

        while True:
            query = "Do you want to {} more than {}?".format(
                task_in_focus.content, self._benchmark.content
            )
            response = input(f"{query} [y/n]: ")
            response = response.lower()

            if response in affirmative:
                return True
            elif response in negative:
                return False
            elif response in exit_script:
                sys.exit()
            elif response in display_tasks:
                self.rich_print()
            elif response in help_menu:
                # TODO: configure help menu text
                pass
            else:
                # TODO: invalid response followed by help menu text
                pass

    def add_to_completed(self, task):
        """Adds uuid of task passed in as argument to self.completed_tasks and calls method to change task.completed attribute to 'True'"""
        task_uuid = task.id_
        self.completed_tasks.append(task_uuid)
        task.complete()


if __name__ == "__main__":
    with open("/Users/workbook/dev/FVPython/fvpython/test.txt", "r") as f:
        test_tasks = f.read().splitlines()
    t_list = TaskList(test_tasks)

    t_list.entries[0].marked = True
    t_list.entries[2].deleted = True
    t_list.entries[3].marked = True
    t_list.entries[5].completed = True
    t_list.active = t_list.entries[7]

    for n in t_list.entries:
        print(n.__dict__)
    t_list.rich_print()

    total_tasks = t_list.entry_count()
    remaining_tasks = t_list.incomplete_count()
    print(f"{remaining_tasks} of {total_tasks} tasks remaining")
