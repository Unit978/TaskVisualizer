__author__ = 'unit978'

import getpass
import platform

from TaskGraphicsItem import TaskGraphicsItem
from StateManager import StateManager

from PyQt4.QtCore import Qt, QRectF, QPointF, SIGNAL, QTimer
from PyQt4.QtGui import QBrush

PID_INDEX = 0
NAME_INDEX = 1
CPU_INDEX = 2
MEM_INDEX = 3
USER_INDEX = 4

USER_NAME = getpass.getuser()

# Check system
if platform.system().lower() == "linux":
    ROOT_NAME = "root"

else:
    ROOT_NAME = "---"


class Visualizer:

    def __init__(self, scene):
        self.taskItemsPool = list()

        # To determine which item to get from the pool of taskItems
        self._taskItemsCounter = 0

        self.cpu_scale = 2.0
        self.mem_scale = 1000

        self.scene = scene

        self.userTaskColor = Qt.red
        self.rootTaskColor = Qt.darkGray
        self.otherTaskColor = Qt.cyan

        # Spacing between each task graphical item
        self.taskItemSpacing = 20

        self.updateProcessDataTimer = QTimer()
        self.updateProcessDataTimer.timeout.connect(self.update_processes_data)

        self.updateItemsTimer = QTimer()
        self.updateItemsTimer.timeout.connect(self.update_items)

        for i in range(0, 200):
            self.add_new_task_graphics_item(False)

        self.updateProcessDataTimer.start(1000.0)
        #self.updateItemsTimer.start(1.0)

    def update_processes_data(self):

        self.deactivate_all()
        processes = StateManager.get_processes_data()

        # Update the graphical representations
        x = 0
        for p in processes:

            item = self.get_task_graphics_item()

            # CPU %
            diameter = p[CPU_INDEX] * self.cpu_scale + 2

            # MEM %
            y = p[MEM_INDEX] / 100.0 * self.mem_scale

            item.setRect(QRectF(x, y, diameter, diameter))

            #item.targetPos = QPointF(x, y)
            #item.targetRadius = diameter

            # Setup the name of the task.
            item.set_name(p[NAME_INDEX])

            if p[USER_INDEX] == USER_NAME:
                item.setBrush(QBrush(self.userTaskColor))
                item.textItem.setDefaultTextColor(Qt.white)

            elif p[USER_INDEX] == ROOT_NAME:
                item.setBrush(QBrush(self.rootTaskColor))
                item.textItem.setDefaultTextColor(self.rootTaskColor)

            else:
                item.setBrush(QBrush(self.otherTaskColor))
                item.textItem.setDefaultTextColor(Qt.white)

            x += diameter + self.taskItemSpacing

        # Update the scene so it can repaint properly
        self.scene.update()

    def update_items(self):
        for item in self.taskItemsPool:
            if item.isVisible():
                item.update()

    def get_task_graphics_item(self):

        # Add more graphic items if there isn't enough in the pool.
        if self._taskItemsCounter >= len(self.taskItemsPool):
            self.add_new_task_graphics_item()

        item = self.taskItemsPool[self._taskItemsCounter]
        item.setVisible(True)
        self._taskItemsCounter += 1
        return item

    def deactivate_all(self):
        for item in self.taskItemsPool:
            item.setVisible(False)
        self._taskItemsCounter = 0

    def add_new_task_graphics_item(self, visible=True):
        item = TaskGraphicsItem()
        item.setVisible(visible)
        self.taskItemsPool.append(item)
        self.scene.addItem(item)