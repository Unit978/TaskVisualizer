__author__ = 'unit978'

import sys
from PyQt4.QtGui import QApplication, QBrush, QColor
from MainWindow import MainWindow
from Visualizer import Visualizer


def main():
    app = QApplication(sys.argv)

    w = MainWindow()
    w.setWindowTitle("Task Visualizer")
    w.resize(1000, 500)

    visualizer = Visualizer(w.scene)
    visualizer.update()

    # Set a dark background color
    # backColor = QColor(50, 50, 80)
    back_color = QColor(25, 20, 45)
    w.view.setBackgroundBrush(QBrush(back_color))

    w.move(10, 10)
    w.show()
    app.exec_()

if __name__ == '__main__':
    main()