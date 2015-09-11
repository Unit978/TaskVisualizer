__author__ = 'unit978'

import getpass
from psutil import process_iter, AccessDenied
from TaskGraphicsItem import TaskGraphicsItem
from PyQt4.QtCore import QRectF, QTimer
from PyQt4.QtGui import QBrush

from PyQt4.QtCore import Qt

PID_INDEX = 0
NAME_INDEX = 1
CPU_INDEX = 2
MEM_INDEX = 3
USER_INDEX = 4

USER_NAME = getpass.getuser().split('/\\')[-1]


class Visualizer:

    def __init__(self, scene):
        self.taskItemsPool = list()

        # To determine which item to get from the pool of taskItems
        self._taskItemsCounter = 0

        self.cpu_scale = 2.0
        self.mem_scale = 1000

        self.scene = scene

        for i in range(0, 200):
            self.add_new(False)

    @staticmethod
    def get_processes_data():

        process_list = list()

        for p in process_iter():

            username = "N/A"

            # Collect the data about the process, such as id, cpu%, ...
            try:
                username = p.username()

            except AccessDenied:
                pass

            process_list.append([p.pid, p.name(), p.cpu_percent(), p.memory_percent(), username])

        return process_list

    def update(self):

        self.deactivate_all()

        # Get the updated processes data
        processes = Visualizer.get_processes_data()

        # Update the graphical representations
        x = 0
        for p in processes:

            item = self.get_task_graphics_item()

            # CPU %
            diameter = p[CPU_INDEX] * self.cpu_scale + 2

            # MEM %
            y = p[MEM_INDEX] / 100.0 * self.mem_scale

            item.setRect(QRectF(x, y, diameter, diameter))

            # Setup the name of the task.
            item.textItem.setPlainText(p[NAME_INDEX])
            x_text = x + item.boundingRect().width()/2 - item.textItem.boundingRect().height()/2
            y_text = y + 100 + item.textItem.boundingRect().width() + diameter
            item.textItem.setPos(x_text, y_text)

            if p[USER_INDEX] == USER_NAME:
                item.setBrush(QBrush(Qt.red))

            else:
                item.setBrush(QBrush(Qt.cyan))

            x += diameter + 15

        # Update the scene so it can repaint properly
        self.scene.update()

        # Update at every second
        QTimer.singleShot(1000.0, self.update)

    def get_task_graphics_item(self):

        # Not enough
        if self._taskItemsCounter >= len(self.taskItemsPool):
            self.add_new()

        item = self.taskItemsPool[self._taskItemsCounter]
        item.setVisible(True)
        self._taskItemsCounter += 1
        return item

    def deactivate_all(self):
        for item in self.taskItemsPool:
            item.setVisible(False)
        self._taskItemsCounter = 0

    def add_new(self, visible=True):
        item = TaskGraphicsItem()
        item.setVisible(visible)
        self.taskItemsPool.append(item)
        self.scene.addItem(item)