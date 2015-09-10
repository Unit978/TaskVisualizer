__author__ = 'unit978'

from PyQt4.QtGui import QMainWindow, QGraphicsScene
from InteractiveView import InteractiveView

from math import sqrt

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

        n = int(sqrt(100))
        for x in range(0, n):
            for y in range(0, n):
                self.scene.addRect(x*6, y*6, 5, 5)

        self.scene.addEllipse(0, 0, 200, 200)
        self.scene.addEllipse(300, 300, 200, 200)
        self.scene.addEllipse(-500, -500, 300, 300)
        self.scene.addEllipse(-500, 0, 100, 100)

        self.setCentralWidget(self.view)
        self.view.setSceneRect(INT_MIN/2, INT_MIN/2, INT_MAX, INT_MAX)
        self.view.centerOn(0, 0)
