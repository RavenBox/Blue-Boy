from Lib.interface import *
from PyQt5 import QtCore, QtWidgets
from sys import exit, argv

from Lib import lib
import random


class MiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.Wr = ""
        self.nSeed = ""
        self.clickPosition = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        self.ui.frame_top.mouseMoveEvent = self.moveWindows_Event

        self.ui.hide.clicked.connect(self._hide)
        self.ui.min.clicked.connect(self._min)
        self.ui.max.clicked.connect(self._max)
        self.ui.bye.clicked.connect(lambda: self.close())
        self.ui.pushButton.clicked.connect(lambda: self.newSeed(0))
        self.ui.pushButton_2.clicked.connect(lambda: self.newSeed(1))

        self.ui.max.show()
        self.ui.min.hide()

        self.ui.state.setText('Welcome to Blue-boy')

    def _hide(self):
        self.showMinimized()

    def _min(self):
        self.showNormal()
        self.ui.max.show()
        self.ui.min.hide()

    def _max(self):
        self.showMaximized()
        self.ui.max.hide()
        self.ui.min.show()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        if not self.isMaximized():
            self.clickPosition = event.globalPos()

    def moveWindows_Event(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                try:
                    self.move(self.pos() + event.globalPos() - self.clickPosition)
                    self.clickPosition = event.globalPos()
                    event.accept()
                except Exception as e:
                    self.ui.state.setText(e)
                    pass
        else:
            self.ui.max.show()
            self.ui.min.hide()

        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()

    def newSeed(self, S):
        try:
            if S < 1:
                self.ui.state.setText('new seed phrases generated!')
                for x in range(300):
                    for i in range(12):
                        self.nSeed = (random.choice(lib.candyLibrary))
                        self.Wr = open('SeedList.txt', 'a')
                        self.Wr.write(self.nSeed)
                    self.Wr.write('\n')
                    self.Wr.close()

            with open('SeedList.txt', 'r') as sl:
                X = sl.read()
                self.ui.output.setText(X)
                sl.close()
        except Exception as e:
            self.ui.state.setText(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    mi_app = MiApp()
    mi_app.show()
    exit(app.exec_())
