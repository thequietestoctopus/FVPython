from task import TaskList
from user import InputHandler
import sys

""" Algorithm function needs to take in a list (or tuple) of tasks; i.e. needs to be ordred iterable
    Each task needs to be aware of: 1) Whether it's marked, 2) Whether it's completed
    Globally need to track: -Benchmark (most recent marked task), -Last completed task """

# test algorithm
test_tasks = ["Wake", "Eat", "Drink", "Run", "Sleep"]
test_list = TaskList(test_tasks)


def evaluate(tasklist):

    while tasklist.incomplete_count() > 0:

        # Does benchmark exist?
        if not tasklist.benchmark:
            # print("No benchmark found")
            # If not, make lowest marked task (highest index in entry list) new benchmark
            marked_tasks = tasklist.marked_tasks()
            if marked_tasks:
                tasklist.benchmark = tasklist.bottom_marked()
            else:
                # If no tasks are marked, assign earliest incomplete task (lowest index) as new benchmark (root task)
                for i in tasklist.entries:
                    if not i.completed:
                        i.mark()
                        tasklist.benchmark = i
                        break

        tasklist.rich_print()

        # TODO: logic for skipping comparison to next unmarked task after the last task to be completed
        # TODO: switchting tasklist benchmark when appropriate <-- already taken care of by above block?? hmm

        # for each incomplete task after benchmark
        for t in tasklist.entries:
            if tasklist.get_index(t) <= tasklist.get_index(tasklist.benchmark):
                continue
            if t.completed:
                continue

            select_task = tasklist.prompt_for_input(t)
            # if user responds 'yes' to doing task t then mark task t
            if select_task:
                t.mark()

            # Check if we are at the end of tasklist
            if not tasklist.end_of_list(t):
                # If we are NOT at the end of the task list continue down
                if t.marked:
                    # If task in focus was just marked by user it becomes the new benchmark
                    tasklist.benchmark = t
                    # TODO: get rid of this print call when functioning (only for debugging purposes)
                    tasklist.rich_print()
                else:
                    # Clear last line of the console
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")
                # continue
            else:
                # If we are at the end of the task list:
                # TODO: More robust prompt function for asking when task is complete
                tasklist.active = tasklist.bottom_marked()
                response = input(
                    "{} now - type 'done' when finished: ".format(
                        tasklist.active.content
                    )
                )
                if response.lower() == "done":
                    tasklist.add_to_completed(tasklist.active)
                    tasklist.active = None
                    tasklist.benchmark = None
                # TODO: accept inputs other than 'done'; i.e. 'not a valid response' and allow for quitting and asking to display the list
                # ^probably needs to be a loop to be able to reshow the same active task prompt


if __name__ == "__main__":
    evaluate(test_list)
