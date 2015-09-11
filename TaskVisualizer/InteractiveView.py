__author__ = 'unit978'

from PyQt4.QtGui import QGraphicsView, QBrush, QColor
from PyQt4.QtCore import Qt, QPoint


class InteractiveView (QGraphicsView):

    def __init__(self, parent=None):
        super(InteractiveView, self).__init__(parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set a dark background color
        self.setBackgroundBrush(QBrush(QColor(50, 50, 80)))

        self.zoomDelta = 0.1
        self.currentScale = 1.0

        self.panSpeed = 4.0
        self.panningButton = Qt.LeftButton
        self.zoomKey = Qt.Key_Z

        self._prevMousePos = QPoint(0, 0)
        self._doMousePanning = False
        self._doKeyZooming = False

    def pan(self, delta):

        # Move the center of the view to simulate panning.
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        x_center = self.viewport().rect().width()/2 - delta.x()
        y_center = self.viewport().rect().height()/2 - delta.y()
        center = QPoint(x_center, y_center)
        self.centerOn(self.mapToScene(center))

        # Set view anchor to zoom from the center of the view.
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

    def zoom(self, scale_factor):
        self.scale(scale_factor, scale_factor)
        self.currentScale *= scale_factor

    def zoom_in(self):
        self.zoom(1.0 + self.zoomDelta)

    def zoom_out(self):
        self.zoom(1.0 - self.zoomDelta)

    def keyPressEvent(self, event):
        super(QGraphicsView, self).keyPressEvent(event)

        # Enable zooming.
        if event.key() == self.zoomKey:
            self._doKeyZooming = True

        # Apply Zooming.
        if self._doKeyZooming:
            if event.key() == Qt.Key_Up:
                self.zoom_in()

            elif event.key() == Qt.Key_Down:
                self.zoom_out()

        # Apply Panning.
        else:
            super(InteractiveView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == self.zoomKey:
            self._doKeyZooming = False

    def mouseMoveEvent(self, event):
        super(InteractiveView, self).mouseMoveEvent(event)

        if self._doMousePanning:

            mouse_delta = self.mapToScene(event.pos()) - self.mapToScene(self._prevMousePos)
            mouse_delta *= self.panSpeed
            mouse_delta *= self.currentScale

            self.pan(mouse_delta)

        self._prevMousePos = event.pos()

    def mousePressEvent(self, event):
        super(InteractiveView, self).mousePressEvent(event)

        if event.button() == self.panningButton:
            self._prevMousePos = event.pos()
            self._doMousePanning = True

    def mouseReleaseEvent(self, event):
        super(InteractiveView, self).mouseReleaseEvent(event)

        if event.button() == self.panningButton:
            self._doMousePanning = False

    def wheelEvent(self, event):

        scroll_amount = event.delta()

        # Apply zooming base on scroll direction.
        self.zoom_in() if scroll_amount > 0 else self.zoom_out()