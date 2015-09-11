__author__ = 'unit978'

import sys
from PyQt4.QtGui import QApplication
from MainWindow import MainWindow
from Visualizer import Visualizer


def main():
    app = QApplication(sys.argv)

    w = MainWindow()
    w.setWindowTitle("Task Visualizer")
    w.resize(900, 500)

    visualizer = Visualizer(w.scene)
    visualizer.update()

    w.show()
    app.exec_()

if __name__ == '__main__':
    main()