__author__ = 'unit978'

from PyQt4.QtGui import QMainWindow, QGraphicsScene, QColor, QBrush
from PyQt4.QtCore import Qt
from InteractiveView import InteractiveView
from Visualizer import Visualizer

INT_MIN = -2147483647 - 1
INT_MAX = 2147483647


class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()

        self.scene = QGraphicsScene()

        # Scene is the parent of the view in order to show the graphical items.
        # the View must also be the parent of the scene in order to avoid
        # bizarre segmentation faults with GTK
        self.view = InteractiveView(self.scene)
        self.scene.setParent(self.view)

        self.setCentralWidget(self.view)
        self.view.setSceneRect(INT_MIN/2, INT_MIN/2, INT_MAX, INT_MAX)
        self.view.centerOn(0, 0)

        self.visualizer = Visualizer(self.scene)
        self.visualizer.update_processes_data()

        # Set a dark background color
        back_color = QColor(25, 20, 45)
        self.view.setBackgroundBrush(QBrush(back_color))

    def keyPressEvent(self, event):
        super(MainWindow, self).keyPressEvent(event)

        # Quit via escape key.
        if event.key() == Qt.Key_Escape:
            self.close()

        if event.key() == Qt.Key_R:
            self.visualizer.showRootTasks = not self.visualizer.showRootTasks