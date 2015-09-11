__author__ = 'unit978'

from PyQt4.QtGui import QGraphicsEllipseItem, QGraphicsTextItem, QPen, QColor
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

    def set_name(self, str_name):
        self.textItem.setPlainText(str_name)

        rect = self.boundingRect()
        text_rect = self.textItem.boundingRect()

        # Center text (on the x-axis) and offset (on the y-axis) so it doesn't overlap the ellipse item.
        x_text = rect.x() + rect.width()/2 - text_rect.height()/2
        y_text = rect.y() + 100 + text_rect.width() + rect.height()

        self.textItem.setPos(x_text, y_text)

    def mousePressEvent(self, event):
        print "Clicked On Ellipse at: ", self.rect().topLeft()