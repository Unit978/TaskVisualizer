__author__ = 'unit978'

from PyQt4.QtGui import QGraphicsEllipseItem, QGraphicsTextItem, QPen, QBrush, QColor
from PyQt4.QtCore import Qt, QPointF, QRectF


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

        # The dimensions to reach via a LERP.
        self.startPos = QPointF(0, 0)
        self.endPos = QPointF(0, 0)
        self.startDiameter = 1
        self.endDiameter = 1

        self.centerMark = QGraphicsEllipseItem()
        self.centerMark.setBrush(QBrush(Qt.white))
        self.centerMark.setPen(QPen(Qt.NoPen))
        self.centerMark.setParentItem(self)

        self.pid = -1

        # To determine if it is associated with an active process.
        self.used = False

    def mousePressEvent(self, event):
        print "Clicked On Ellipse at: ", self.rect().topLeft()

    def set_pid(self, pid):
        self.pid = pid

    def set_name(self, str_name):
        self.textItem.setPlainText(str_name)

    def update_name_pos(self):

        rect = self.boundingRect()
        text_rect = self.textItem.boundingRect()

        # Center text (on the x-axis) and offset (on the y-axis) so it doesn't overlap the ellipse item.
        x_text = rect.x() + rect.width()/2 - text_rect.height()/2
        y_text = rect.y() + 100 + text_rect.width() + rect.height()

        self.textItem.setPos(x_text, y_text)

    # Time step is in seconds.
    def update(self, time_step):

        diameter = self.rect().width() + self.lerp_rate(self.startDiameter, self.endDiameter, time_step)
        if diameter <= 1:
            diameter = 1

        pos = self.rect().topLeft()

        x = pos.x() + self.lerp_rate(self.startPos.x(), self.endPos.x(), time_step)
        y = pos.y() + self.lerp_rate(self.startPos.y(), self.endPos.y(), time_step)

        self.setRect(QRectF(x, y, diameter, diameter))
        self.update_name_pos()
        self.update_center_mark()

    def update_center_mark(self):
        scale = self.scene().views()[0].currentScale

        hwidth = self.rect().width() / 2.0
        diam = 2.0 / scale

        # Only mark center for large enough items.
        if hwidth * 0.2 > diam:

            self.centerMark.setVisible(True)

            hdiam = diam / 2.0
            pos = self.rect().topLeft()

            x = pos.x() - hdiam + hwidth
            y = pos.y() - hdiam + hwidth
            self.centerMark.setRect(QRectF(x, y, diam, diam))

        else:
            self.centerMark.setVisible(False)

    # Return the linear interpolation rate. Reach start to end at a rate of 'growth rate'
    @staticmethod
    def lerp_rate(start, end, time_step):
        return (end - start) * time_step