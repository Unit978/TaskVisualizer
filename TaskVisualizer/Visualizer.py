__author__ = 'unit978'

from TaskGraphicsItem import TaskGraphicsItem
from StateManager import *

from PyQt4.QtCore import Qt, QRectF, QPointF, QTimer
from PyQt4.QtGui import QBrush, QPen, QGraphicsLineItem


class Visualizer:

    def __init__(self, scene):

        self.scene = scene

        # Pool of items to grab from when needed.
        self.taskItemPool = list()

        # The items that are active and to be updated.
        self.activeItems = list()

        # Dictionary of PIDs and an associated item to represent the process.
        self.taskItemPids = dict()

        # Scales the visualization dimension for cpu%.
        self.cpuScale = 2.0

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
        self.updateItemsTimer.start(50.0)

    def update_processes_data(self):

        # Reset USED flag in order to determine which task items are unused. This
        # will happen when an item's process does not exist anymore.
        for item in self.activeItems:
            item.used = False

        processes = StateManager.get_processes_data()

        # Update the graphical representations
        x = 0
        for p in processes:

            if p[USER_INDEX] == ROOT_NAME and not self.showRootTasks:
                continue

            pid = p[PID_INDEX]

            # Pid still exists.
            if pid in self.taskItemPids:

                item = self.taskItemPids[pid]

                # Check if PID returned after it ended. This means that the mapped
                # item MAY be associated with another process.
                if item.pid != pid:
                    item = self.fetch_task_item()
                    self.taskItemPids[pid] = item
                    item.pid = pid

                # Remove from pool and add to active.
                elif item in self.taskItemPool:
                    self.taskItemPool.remove(item)
                    self.activeItems.append(item)

                # ELSE: reuse item, the process returned continuously.
                item.setVisible(True)
                item.used = True

            # Pid not in dictionary, Add task item.
            else:
                item = self.fetch_task_item()
                self.taskItemPids[pid] = item
                item.pid = pid
                item.used = True

            # CPU %
            new_diameter = p[CPU_INDEX] * self.cpuScale + 2

            # MEM %
            y = p[MEM_INDEX] / 100.0 * self.memAxisLen

            # Center around on y-component.
            y -= new_diameter / 2.0

            pos = item.rect().topLeft()
            diameter = item.rect().width()

            # Set position bounds.
            item.startPos = pos
            item.endPos = QPointF(x, y)

            # Setup diameter bounds.
            item.startDiameter = diameter
            item.endDiameter = new_diameter

            x += new_diameter + self.taskItemSpacing

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

        self.recycle_unused_items()

        # Update the scene so it can repaint properly
        self.scene.update()

    def update_items(self):

        time_step = self.updateItemsTimer.interval() / float(self.updateProcessDataTimer.interval())

        for item in self.activeItems:
            item.update(time_step)

    def fetch_task_item(self):

        # Add more graphic items if there isn't enough in the pool.
        if len(self.taskItemPool) == 0:
            self.add_new_task_graphics_item()

        item = self.taskItemPool.pop()
        item.setVisible(True)
        self.activeItems.append(item)

        return item

    def recycle_task_item(self, item):
        item.setVisible(False)
        self.taskItemPool.append(item)

    # Items without an active process are recycled
    def recycle_unused_items(self):

        # Recycle unused.
        for item in self.activeItems:
            if not item.used:
                self.recycle_task_item(item)

        # Only keep the used items.
        self.activeItems = [item for item in self.activeItems if item.used]

    def add_new_task_graphics_item(self, visible=True):
        item = TaskGraphicsItem(QRectF(0, 0, 1, 1))
        item.setVisible(visible)
        self.taskItemPool.append(item)
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