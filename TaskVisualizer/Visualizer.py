__author__ = 'unit978'

import getpass
import platform

from TaskGraphicsItem import TaskGraphicsItem
from StateManager import StateManager

from PyQt4.QtCore import Qt, QRectF, QPointF, QTimer
from PyQt4.QtGui import QBrush, QPen, QGraphicsLineItem

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
    ROOT_NAME = "SYSTEM"


class Visualizer:

    def __init__(self, scene):

        self.scene = scene

        self.taskItemsPool = list()

        # To determine which item to get from the pool of taskItems
        self._taskItemsCounter = 0

        # Scales the visualization dimension for cpu%.
        self.cpuScale = 4.0

        # Setup memory axis visualization.
        self.memAxisLen = 1000
        self.memXOffset = -10
        self._memTickInterval = 0.1  # As a percentage of the memScale.
        self.memAxis = None
        self.setup_mem_axis()

        # Set the color codes for each task type.
        self.userTaskColor = Qt.red
        self.rootTaskColor = Qt.darkGray
        self.otherTaskColor = Qt.cyan

        # Spacing between each task graphical item
        self.taskItemSpacing = 20

        self.showRootTasks = False

        # Set up the timers to update the visualization.
        self.updateProcessDataTimer = QTimer()
        self.updateProcessDataTimer.timeout.connect(self.update_processes_data)
        self.updateItemsTimer = QTimer()
        self.updateItemsTimer.timeout.connect(self.update_items)

        # Fill the pool of task items.
        for i in range(0, 200):
            self.add_new_task_graphics_item(False)

        self.updateProcessDataTimer.start(1000.0)
        self.updateItemsTimer.start(80.0)

    def update_processes_data(self):

        self.deactivate_all()
        processes = StateManager.get_processes_data()

        # Update the graphical representations
        x = 0
        for p in processes:

            if p[USER_INDEX] == ROOT_NAME and not self.showRootTasks:
                continue

            item = self.get_task_graphics_item()

            # CPU %
            new_diameter = p[CPU_INDEX] * self.cpuScale + 2

            # MEM %
            y = p[MEM_INDEX] / 100.0 * self.memAxisLen

            # Center around on y-component.
            y -= new_diameter / 2.0

            # item.setRect(QRectF(x, y, new_diameter, new_diameter))

            pos = item.rect().topLeft()
            diameter = item.rect().width()
            item.setRect(QRectF(pos.x(), pos.y(), diameter, diameter))

            # Set position bounds.
            item.startPos = pos
            item.endPos = QPointF(x, y)

            # Setup diameter bounds.
            item.startDiameter = diameter
            item.endDiameter = new_diameter

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

            x += new_diameter + self.taskItemSpacing

        # Update the scene so it can repaint properly
        self.scene.update()

    def update_items(self):

        time_step = self.updateItemsTimer.interval() / float(self.updateProcessDataTimer.interval())

        for item in self.taskItemsPool:
            if item.isVisible():
                item.update(time_step)

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
        item = TaskGraphicsItem(QRectF(0, 0, 1, 1))
        item.setVisible(visible)
        self.taskItemsPool.append(item)
        self.scene.addItem(item)

    def setup_mem_axis(self):
        self.memAxis = QGraphicsLineItem(self.memXOffset, 0, self.memXOffset, self.memAxisLen, None, self.scene)
        self.memAxis.setPen(QPen(Qt.white))

        step = int(self._memTickInterval * self.memAxisLen)

        pen = QPen(Qt.CustomDashLine)
        pen.setDashPattern([2, 20])
        pen.setColor(Qt.lightGray)

        for y in range(step, self.memAxisLen + step, step):
            self.scene.addLine(self.memXOffset, y, 2500.0, y, pen)

    def update_mem_axis(self):

        # Set Length of line to the x value of the last active task item.
        pass