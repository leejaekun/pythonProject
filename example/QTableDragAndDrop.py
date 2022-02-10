# https://stackoverflow.com/questions/10264040/how-to-drag-and-drop-into-a-qtablewidget-pyqt
# 완벽하지 않음. 일부 기능은 정상.
#
#
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui


class Button(QPushButton):

    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.RightButton:
            return

        mimeData = QtCore.QMimeData()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.start(QtCore.Qt.MoveAction)

    def mousePressEvent(self, e):

        QPushButton.mousePressEvent(self, e)
        if e.button() == QtCore.Qt.LeftButton:
            print('left-button press')
        elif e.button() == QtCore.Qt.RightButton:
            print('right-button press')


class MyTable(QTableWidget):

    def __init__(self, rows, columns, parent):
        super(MyTable, self).__init__(rows, columns, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print(e.accept())

    def dropEvent(self, e):
        print ('blah')

        position = e.pos()
        # self.button.move(position)

        e.setDropAction(QtCore.Qt.MoveAction)

        e.accept()


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.button = Button('Button', self)

        self.table = MyTable(2,2,self)
        self.table.setAcceptDrops(True)
        self.table.setDragEnabled(True)

        self.setWindowTitle('Click or Move')

        self.setGeometry(300, 300, 280, 150)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.table)
        self.setLayout(layout)


def main():

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()  


if __name__ == '__main__':

    main()