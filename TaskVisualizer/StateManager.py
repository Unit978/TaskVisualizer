__author__ = 'unit978'

import re
from psutil import process_iter, AccessDenied


# Gets the state of the machine (the running processes).
# Can also record the state of the machine at the dedicated interval
class StateManager:

    def __init__(self):

        # The amount of seconds to update the processes data.
        self.update_interval = 1.0

    # Collect data about the running processes, such as name, id, cpu%, ...
    @staticmethod
    def get_processes_data():

        process_list = list()

        for p in process_iter():

            username = "N/A"
            try:
                username = re.split(r"[/\\]", p.username())[-1]

            except AccessDenied:
                pass

            process_list.append([p.pid, p.name(), p.cpu_percent(), p.memory_percent(), username])

        return process_list

    def record_state(self):
        pass

    def save_session(self):
        pass