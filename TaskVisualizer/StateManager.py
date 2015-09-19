__author__ = 'unit978'

import re
import getpass
import platform
from psutil import process_iter, AccessDenied

PID_INDEX = 0
NAME_INDEX = 1
CPU_INDEX = 2
MEM_INDEX = 3
USER_INDEX = 4

USER_NAME = getpass.getuser()

# Check system
systemName = platform.system().lower()
if systemName == "linux":
    ROOT_NAME = "root"

elif systemName == "windows":
    ROOT_NAME = "SYSTEM"

else:
    ROOT_NAME = "---"


# Gets the state of the machine (the running processes).
# Can also record the state of the machine at the dedicated interval
class StateManager:

    def __init__(self):

        # The amount of seconds to update the processes data.
        self.update_interval = 1.0

        self.process_data = ""

    # Collect data about the running processes, such as name, id, cpu%, ...
    @staticmethod
    def get_processes_data():

        process_list = list()

        for p in process_iter():

            # Skip System Idle Process for Windows.
            if p.pid == 0 and systemName == "windows":
                continue

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