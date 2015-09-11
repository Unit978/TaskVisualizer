__author__ = 'unit978'

from PyQt4.QtGui import QGraphicsEllipseItem, QPen
from PyQt4.QtCore import Qt


class TaskGraphicsItem (QGraphicsEllipseItem):

    def __init__(self, rect=None):
        super(TaskGraphicsItem, self).__init__()

        if rect is not None:
            self.setRect(rect)

        self.setPen(QPen(Qt.NoPen))

    def mousePressEvent(self, event):
        print "Clicked On Ellipse at: ", self.rect().topLeft()