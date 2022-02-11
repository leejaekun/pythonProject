from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QAbstractItemView, QStyleFactory, QApplication, QDialog, \
    QMenu, QTableWidgetSelectionRange, QTableWidget, QTableWidgetItem, QVBoxLayout, QAction


########################################################################################
# 2. ActionContextMenu-- actions() 사용함.
# 출처: https: // freeprog.tistory.com/334 [취미로 하는 프로그래밍 !!!]
# QTableWidget을 상속 받아 context 메뉴를 사용하는 방법
# 여기서는 사용하지 않음.
# ########################################################################################
class actionContextWidget(QDialog, QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)

        self.table_widget = QTableWidget(20, 10)

        self.table_widget.setHorizontalHeaderLabels(
            ["코드", "종목명", "코드2", "종목명2", "코드3", "종목명3", "코드4", "종목명4", "코드5", "종목명5"])

        # column 단위로 선택 가능 #
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectColumns)
        # item 단위로 선택 #
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        # row 단위로 선택 가능
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        for i in range(self.table_widget.rowCount()):
            for j in range(self.table_widget.columnCount()):
                it = QTableWidgetItem("{}-{}".format(i, j))
                self.table_widget.setItem(i, j, it)

        vlay = QVBoxLayout(self)
        vlay.addWidget(self.table_widget)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        
        selectAction = QAction("Select", self)
        unSelectAction = QAction("Unselect", self)

        self.addAction(selectAction)
        self.addAction(unSelectAction)

        selectAction.triggered.connect(self.__select)
        unSelectAction.triggered.connect(self.__unSelect)

    @pyqtSlot()
    def __select(self):
        print("Select Action Complete.")


    def __unSelect(self):
        print("unSelect Action Complete.")


    def on_customContextMenuRequested(self, pos):
        it = self.table_widget.itemAt(pos)
        if it is None:
            return
        c = it.column()
        item_range = QTableWidgetSelectionRange(
            0, c, self.table_widget.rowCount()-1, c)
        self.table_widget.setRangeSelected(item_range, True)

        menu = QMenu()
        select_column_action = menu.addAction("Select column")
        unSelect_column_action = menu.addAction("unSelect column")
        action = menu.exec_(self.mapToGlobal(pos))
        # action = menu.exec_(self.table_widget.viewport().mapToGlobal(pos))
        if action == select_column_action:
            # self.table_widget.removeColumn(c)
            colNo = self.table_widget.selectedIndexes()[0].column()
            print(colNo)
            #
            # https://freeprog.tistory.com/333
            # 헤더 배경색 설정 --> app.setStyle 설정을 해야 함
            # 헤터 설정을 해야함. 자동으로 만들어진 헤더(숫자)의 색변경은 안됨.
            item = self.table_widget.horizontalHeaderItem(colNo)
            print(item)
            if item is not None:
                item.setBackground(QBrush(Qt.cyan))
            # 아래는 셀 색상 변경.
            # for i in range(20):
                # item = self.table_widget.item(col, 0)
                # item.setBackground(QBrush(Qt.red))
                # self.table_widget.item(
                #     i, colNo).setBackground(QBrush(Qt.red))
        elif action == unSelect_column_action:
            colNo = self.table_widget.selectedIndexes()[0].column()
            print(colNo)
            item = self.table_widget.horizontalHeaderItem(colNo)
            print(item)
            if item is not None:
                item.setBackground(QBrush(Qt.white))


########################################################################################
# 1. DefaultContextMenu-- contextMenuEvent() 호출함.
# 출처: https: // freeprog.tistory.com/334 [취미로 하는 프로그래밍 !!!]
# MAIN 프로그램에서 app.setStyle(QStyleFactory.create('Fusion')) # 헤더 색상 변경
# 추가해야 색상이 변경됨. 꼭 알아야 두어야 함.
########################################################################################
class contextWidget(QDialog, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(contextWidget, self).__init__(parent)

        self.table_widget = QTableWidget(20, 10)

        self.table_widget.setHorizontalHeaderLabels(
            ["코드", "종목명", "코드2", "종목명2", "코드3", "종목명3", "코드4", "종목명4", "코드5", "종목명5"])

        # column 단위로 선택 가능 #
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectColumns)
        # item 단위로 선택 #
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        # row 단위로 선택 가능
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        for i in range(self.table_widget.rowCount()):
            for j in range(self.table_widget.columnCount()):
                it = QTableWidgetItem("{}-{}".format(i, j))
                self.table_widget.setItem(i, j, it)

        vlay = QVBoxLayout(self)
        vlay.addWidget(self.table_widget)

        self.table_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(
            self.on_customContextMenuRequested)

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_customContextMenuRequested(self, pos):
        it = self.table_widget.itemAt(pos)
        if it is None:
            return
        c = it.column()
        item_range = QTableWidgetSelectionRange(
            0, c, self.table_widget.rowCount()-1, c)
        self.table_widget.setRangeSelected(item_range, True)

        menu = QMenu()
        select_column_action = menu.addAction("Select column")
        unSelect_column_action = menu.addAction("unSelect column")
        action = menu.exec_(self.mapToGlobal(pos))
        # action = menu.exec_(self.table_widget.viewport().mapToGlobal(pos))
        if action == select_column_action:
            # self.table_widget.removeColumn(c)
            colNo = self.table_widget.selectedIndexes()[0].column()
            print(colNo)
            #
            # https://freeprog.tistory.com/333
            # 헤더 배경색 설정 --> app.setStyle 설정을 해야 함
            # 헤터 설정을 해야함. 자동으로 만들어진 헤더(숫자)의 색변경은 안됨.
            item = self.table_widget.horizontalHeaderItem(colNo)
            print(item)
            if item is not None:
                item.setBackground(QBrush(Qt.cyan))
            # 아래는 셀 색상 변경.
            # for i in range(20):
                # item = self.table_widget.item(col, 0)
                # item.setBackground(QBrush(Qt.red))
                # self.table_widget.item(
                #     i, colNo).setBackground(QBrush(Qt.red))
        elif action == unSelect_column_action:
            colNo = self.table_widget.selectedIndexes()[0].column()
            print(colNo)
            item = self.table_widget.horizontalHeaderItem(colNo)
            print(item)
            if item is not None:
                item.setBackground(QBrush(Qt.white))


class Widget(QDialog, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.table_widget = QtWidgets.QTableWidget(20, 10)

        self.table_widget.setHorizontalHeaderLabels(
            ["코드", "종목명", "코드2", "종목명2", "코드3", "종목명3", "코드4", "종목명4","코드5", "종목명5"  ])

        # column 단위로 선택 가능 # 
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectColumns)
        # item 단위로 선택 # 
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectItems) 
        # row 단위로 선택 가능
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        for i in range(self.table_widget.rowCount()):
            for j in range(self.table_widget.columnCount()):
                it = QtWidgets.QTableWidgetItem("{}-{}".format(i, j))
                self.table_widget.setItem(i, j, it)

        vlay = QtWidgets.QVBoxLayout(self)
        vlay.addWidget(self.table_widget)

        self.table_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(
            self.on_customContextMenuRequested)

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_customContextMenuRequested(self, pos):
        it = self.table_widget.itemAt(pos)
        if it is None:
            return
        c = it.column()
        item_range = QtWidgets.QTableWidgetSelectionRange(
            0, c, self.table_widget.rowCount()-1, c)
        self.table_widget.setRangeSelected(item_range, True)

        menu = QtWidgets.QMenu()
        select_column_action = menu.addAction("Select column")
        unSelect_column_action = menu.addAction("unSelect column")
        action = menu.exec_(self.table_widget.viewport().mapToGlobal(pos))
        if action == select_column_action:
            # self.table_widget.removeColumn(c)
            colNo = self.table_widget.selectedIndexes()[0].column()
            print(colNo)
            #
            # https://freeprog.tistory.com/333
            # 헤더 배경색 설정 --> app.setStyle 설정을 해야 함
            # 헤터 설정을 해야함. 자동으로 만들어진 헤더(숫자)의 색변경은 안됨.
            item = self.table_widget.horizontalHeaderItem(colNo)
            if item is not None:
                item.setBackground(QBrush(Qt.cyan))
            # 아래는 셀 색상 변경.
            # for i in range(20):
                # item = self.table_widget.item(col, 0)
                # item.setBackground(QBrush(Qt.red))
                # self.table_widget.item(
                #     i, colNo).setBackground(QBrush(Qt.red))
        elif action == unSelect_column_action:
            colNo = self.table_widget.selectedIndexes()[0].column()
            print(colNo)
            item = self.table_widget.horizontalHeaderItem(colNo)
            if item is not None:
                item.setBackground(QBrush(Qt.white))
      



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion')) # 헤더 색상 변경을 위해 필수.
    w = Widget()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())
