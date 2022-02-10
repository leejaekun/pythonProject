# https://forum.qt.io/topic/104363/selection-background-color-not-working-for-cell-widget-in-qtablewidget/4


from sys import exit as sysExit

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TableLine(QLineEdit):
    def __init__(self, parent):
        QLineEdit.__init__(self)
        self.setStyleSheet("padding-left: 10px")

    def IsSelected(self):
        self.On_Selected(True)

    def NotSelected(self):
        self.On_Selected(False)

    def On_Selected(self, Slctd):
        if Slctd:
            self.setStyleSheet("background-color: #353535")
        else:
            self.setStyleSheet("background-color: white")


class TableText(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self)
        self.setStyleSheet("padding-left: 10px")

    def IsSelected(self):
        self.On_Selected(True)

    def NotSelected(self):
        self.On_Selected(False)

    def On_Selected(self, Slctd):
        if Slctd:
            self.setStyleSheet("background-color: #353535")
        else:
            self.setStyleSheet("background-color: white")


class TableCheck(QCheckBox):
    def __init__(self, parent):
        QCheckBox.__init__(self)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(Qt.NoFocus)
        self.setMaximumSize(30, 30)
        self.setChecked(True)
        self.setStyleSheet("padding-left: 10px")

    def IsSelected(self):
        self.On_Selected(True)

    def NotSelected(self):
        self.On_Selected(False)

    def On_Selected(self, Slctd):
        if Slctd:
            self.setStyleSheet("background-color: #353535")
        else:
            self.setStyleSheet("background-color: white")


class TableTable(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self)

        self.setGeometry(QRect(50, 40, 310, 50))
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setShowGrid(False)
        self.PrvSlctd = -1
        self.Selected = -1

        self.insertRow(0)
        self.insertRow(1)

        self.insertColumn(0)
        self.insertColumn(1)
        self.insertColumn(2)

        self.setCellWidget(0, 0, TableLine(self))
        self.setCellWidget(0, 1, TableCheck(self))
        self.setCellWidget(0, 2, TableText(self))

        self.setCellWidget(1, 0, TableLine(self))
        self.setCellWidget(1, 1, TableCheck(self))
        self.setCellWidget(1, 2, TableText(self))

        self.itemSelectionChanged.connect(self.On_Selected)

    def On_Selected(self):
        if self.PrvSlctd > -1:
            self.cellWidget(self.PrvSlctd, 0).NotSelected()
            self.cellWidget(self.PrvSlctd, 1).NotSelected()
            self.cellWidget(self.PrvSlctd, 2).NotSelected()

        if self.Selected == 0:
            self.Selected = 1
            self.PrvSlctd = 1
        else:
            self.Selected = 0
            self.PrvSlctd = 0

        self.cellWidget(self.Selected, 0).IsSelected()
        self.cellWidget(self.Selected, 1).IsSelected()
        self.cellWidget(self.Selected, 2).IsSelected()


class UI_MainWindow(QMainWindow):
    def __init__(self):
        super(UI_MainWindow, self).__init__()
        self.setWindowTitle('Main Window')
        self.setObjectName("MainWindow")
        self.resize(400, 300)

        self.MyTable = TableTable(self)
        self.setCentralWidget(self.MyTable)


if __name__ == "__main__":
    MainApp = QApplication([])

    MainGui = UI_MainWindow()
    MainGui.show()

    sysExit(MainApp.exec_())
