__author__ = 'unit978'

from PyQt4.QtGui import QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem, QPen, QColor
from PyQt4.QtCore import Qt


class TaskGraphicsItem (QGraphicsEllipseItem):

    def __init__(self, rect=None):
        super(TaskGraphicsItem, self).__init__()

        if rect is not None:
            self.setRect(rect)

        self.setPen(QPen(Qt.NoPen))

        # Setup the text item
        self.textItem = QGraphicsTextItem()
        self.textItem.setParentItem(self)
        self.textItem.rotate(-90)
        self.textItem.setDefaultTextColor(QColor(255, 255, 255))
        # self.textItem.setFlag(QGraphicsItem.ItemIgnoresTransformations)

    def mousePressEvent(self, event):
        print "Clicked On Ellipse at: ", self.rect().topLeft()