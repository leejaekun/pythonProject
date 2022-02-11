"""
  plotMotorChar_2.py 에 종속된 프로그램
  서브 윈도우에서 그래프를 그리고, 데이타를 추출하는 부분임.

"""

import os.path
import csv
from PyQt5.QtWidgets import QAbstractItemView, QPushButton, QApplication, QDialog, \
    QMenu, QTableWidgetSelectionRange, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QHBoxLayout, QMessageBox, QLineEdit, QLabel
from PyQt5 import QtCore 
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, pyqtSlot

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VietnamPackage:
    def detail(self):
        print("베트남 다낭 60만원 ")

class subWindow(QDialog):
    def __init__(self, name, my_data):
        self.my_data = my_data  # 보낸 데이타를 이렇게 받으면 됨.
        self.name = name # 파일 이름도 같이 받음.
        super().__init__()
        self.initUI()
        self.setGeometry(200, 200, 1600, 600)
        self.setWindowTitle(name + " --> .txt Converted Window")

    def initUI(self):
        # --------
        self.signOK = QPushButton("ACCEPT", self)
        self.signOK.setGeometry(50, 550, 75, 23)
        self.signOK.clicked.connect(self.saveFile)
        # --------
        self.signNO = QPushButton("PASS", self)
        self.signNO.setGeometry(150, 550, 75, 23)
        self.signNO.clicked.connect(self.closeEvent)
        # #
        # # https://wikidocs.net/5240  QTableWidget 만들기.
        # #
        self.tableWidget = QTableWidget(self)
        # self.tableWidget.resize(1550, 500)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(self.my_data[0])-1)

        # 데이타 저장은 click event 에서 ...
        # self.tableWidget.setItem(0, 0, QTableWidgetItem("1"))
        # self.tableWidget.setItem(0, 1, QTableWidgetItem("2"))
        # self.tableWidget.setItem(1, 0, QTableWidgetItem("3"))
        # self.tableWidget.setItem(1, 1, QTableWidgetItem("4"))
        #
        # print(listValue)
        # for row in range(0, len(self.my_data[0])) :
        #     for col in range(0, len(self.my_data[0][0])) :
        #         self.tableWidget.setItem(row, col, QTableWidgetItem(str(self.my_data[0][row][col])))

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        layout = QHBoxLayout()
        layoutLeft = QVBoxLayout()
        layoutRight = QVBoxLayout()
        layoutLeftTop = QVBoxLayout()
        layoutLeftBot = QHBoxLayout()

        layout.addLayout(layoutLeft)
        layout.addLayout(layoutRight)
        layoutLeft.addLayout(layoutLeftTop)
        layoutLeft.addLayout(layoutLeftBot)

        layoutLeftTop.addWidget(self.tableWidget)
        layoutLeftBot.addWidget(self.signOK)
        layoutLeftBot.addWidget(self.signNO)
        layoutRight.addWidget(self.canvas)

        self.setLayout(layout)

        self.drawgrph()

        self.tableData = list()  # 저장할 테이블 데이타.

        # https://forum.pythonguis.com/t/remeber-last-saved-directory-with-qfiledialog/246
        #
        # 항상 고정된 위치에서 파일을 열도록 하는 방법
        # 화면에 셋팅 조건(폴더 경로)을 기록해두면 좋을 것 같음. 다음과 같은 변수를 사용.
        # self.active_folder = os.path.dirname(fileName)

    def saveFile(self):
        # rtn = startGraph()
        # rtn.saveFileOnly()
        col_count = self.tableWidget.columnCount()
        row_count = self.tableWidget.rowCount()

        rowData = list()
        for row in range(0, row_count):
            for col in range(0, col_count):
                rowData.append(float(self.tableWidget.item(row, col).text()))
            self.tableData.append(rowData)
            rowData = list()
        print(self.tableData)
        print(type(self.tableData))
        # saveFile = plotMotorChar.startGraph()  # w저장은 startGraph 에서 수행을 함.
        self.saveMdfTextFile(self.name, self.tableData)
        # self.saveTextFile(self.name, self.tableData)
# 
        # for col in range(0, len(self.my_data)) :
        #     value = self.tableWidget.item(0,col)
        #     self.tableData.append(float(value.text()))
        # print(self.tableData)
        self.close()  # 저장이 완료되면 닫음.

    def closeEvent(self, QCloseEvent):
        # rtn = startGraph()
        # rtn.saveSignalFalse()
        self.close()
        # re = QMessageBox.question(self, '종료확인', '종료하시겠습니까?',
        #                           QMessageBox.Yes|QMessageBox.No)
        # if re == QMessageBox.Yes:
        #     QCloseEvent.accept
        # else:
        #     QCloseEvent.ignore

    def click(self, event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        points = tuple(zip(xdata[ind], ydata[ind]))
        # print('onpick points:', points)

        print(ind)
        # Create a empty row at bottom of table
        self.numRows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(self.numRows)
        for col in range(0, len(self.my_data)):
            self.tableWidget.setItem(self.numRows, col, QTableWidgetItem(str(self.my_data[ind[0], col+1])))
            # ERROR : IndexError: index 15 is out of bounds for axis 1 with size 15 뭔지 모르겠음.
            print("{} {} index: {}".format(self.numRows, col, ind[0]))

    def drawgrph(self):
        x = self.my_data[:,0]
        y = self.my_data[:,2]

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        #
        #  mpl_connect 를 사용하는데에는 다양한 방법이 있는것 같다.
        #   - button_press_event : 마우스 클릭을 하면 좌표값만을 반환하는 것?
        #   - pick_event : 선택가능하게 그래프를 그리고, 점을 클릭하면 점의 인덱스와 값을 반환?
        ax.plot(x, y, 'o', label="torque", picker=5)  # 5 points tolerance
        self.fig.canvas.mpl_connect('pick_event', self.click)

        ax.set_xlabel("x")
        ax.set_xlabel("y")

        ax.set_title("Torque Set")
        ax.legend()
        ax.grid()

        self.canvas.draw()

    def saveTextFile(self, fileName, listData):
        pathName = os.path.dirname(fileName)
        fname = os.path.basename(fileName)  # 파일 이름만 추출함.
        speed, tr = fname.split('r')

        # Debug - 데이타 확인 ----------
        f = open(pathName + '/' + str(int(speed)) +
                 'rpm.txt', 'w', encoding='utf-8', newline='')
        print(pathName + '/' + str(int(speed)) + 'rpm.txt')
        wr = csv.writer(f, delimiter='\t')
        for line in listData:
            wr.writerow(line)
        # for line in listSecond:
        #     wr.writerow(line)
        f.close()
        # Debug - 저장 종료 ------------

    def saveMdfTextFile(self, fileName, listData):
        pathName = os.path.dirname(fileName)
        fname = os.path.basename(fileName)  # 파일 이름만 추출함.
        nameOnly, tr = fname.split('.')

        # Debug - 데이타 확인 ----------
        f = open(pathName + '/' + nameOnly +
                 '.txt', 'w', encoding='utf-8', newline='')
        print(pathName + '/' + nameOnly + '.txt')
        wr = csv.writer(f, delimiter='\t')
        for line in listData:
            wr.writerow(line)
        # for line in listSecond:
        #     wr.writerow(line)
        f.close()
        # Debug - 저장 종료 ------------


class subWinSelect(QDialog):
    def __init__(self, name, my_data):
        self.my_data = my_data  # 보낸 데이타를 이렇게 받으면 됨.
        self.name = name  # 파일 이름도 같이 받음.
        super().__init__()
        self.initUI()
        self.setGeometry(200, 200, 1600, 600)
        self.setWindowTitle(name + " --> .txt Converted Window")

    def initUI(self):
        ##############################################################################
        self.lblSpeed = QLabel("SPEED", self)
        self.editSpeed = QLineEdit(self)
        # --------
        self.lblTorque = QLabel("TORQUE", self)
        self.editTorque = QLineEdit(self)
        # --------
        self.lblPower = QLabel("POWER", self)
        self.editPower = QLineEdit(self)
        # --------
        self.lblVoltage = QLabel("VOLTAGE", self)
        self.editVoltage = QLineEdit(self)
        # --------
        self.lblCurrent = QLabel("CURRENT", self)
        self.editCurrent = QLineEdit(self)
        # --------
        self.lblEff = QLabel("EFFICIENT", self)
        self.editEff = QLineEdit(self)
        ##############################################################################
        self.signOK = QPushButton("ACCEPT", self)
        # self.signOK.setGeometry(50, 550, 75, 23)
        self.signOK.clicked.connect(self.saveFile)
        # --------
        self.signNO = QPushButton("PASS", self)
        # self.signNO.setGeometry(150, 550, 75, 23)
        self.signNO.clicked.connect(self.close)
        # --------
        self.toGraph = QPushButton("to GRAPH", self)
        # self.signNO.setGeometry(150, 550, 75, 23)
        self.toGraph.clicked.connect(self.dataToGraph)
        ##############################################################################
        self.editSelection = QLineEdit(self)
        # #
        # # https://wikidocs.net/5240  QTableWidget 만들기.
        # #
        self.tableWidget = QTableWidget(self)
        # self.tableWidget.resize(1550, 500)
        self.tableWidget.setRowCount(len(self.my_data)-1)
        self.tableWidget.setColumnCount(len(self.my_data[0]))

        # 데이타 저장은 click event 에서 ...
        # self.tableWidget.setItem(0, 0, QTableWidgetItem("1"))
        # self.tableWidget.setItem(0, 1, QTableWidgetItem("2"))
        # self.tableWidget.setItem(1, 0, QTableWidgetItem("3"))
        # self.tableWidget.setItem(1, 1, QTableWidgetItem("4"))
        #
        # print(self.my_data.shape)
        # print(type(self.my_data))

        ##############################################################################
        # column 단위로 선택 가능 #
        ##############################################################################
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectColumns)
        # item 단위로 선택 #
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        # row 단위로 선택 가능
        # self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        ##############################################################################

        ########################################################################################
        # 1. DefaultContextMenu-- contextMenuEvent() 호출함.
        # 출처: https: // freeprog.tistory.com/334 [취미로 하는 프로그래밍 !!!]
        # MAIN 프로그램에서 app.setStyle(QStyleFactory.create('Fusion')) # 헤더 색상 변경
        # 추가해야 색상이 변경됨. 꼭 알아야 두어야 함.
        ########################################################################################
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.on_customContextMenuRequested)
        # self.tableWidget.customContextMenuRequested.connect(self.on_customContextMenuRequested)

        ##############################################################################
        # QTableWidget 에서 마우스로 선택된 column 값. 초기값은 -1 #
        ##############################################################################
        self.colNo = -1

        ##############################################################################
        # QTableWidget 에서 마우스로 선택된 column 값 담는곳. #
        ##############################################################################
        self.colBank = list()

        ##############################################################################
        # HEADER 설정. 파일의 맨 앞줄 #
        ##############################################################################
        column_headers = self.my_data[0].tolist()
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 수정금지
        #################################################################################

        ##############################################################################
        # QTable Widget 에서 HEADER 선택이 되면 colume 값을 준다. QPos 값을 주지 못함.         #
        # contextMenu 를 사용하는데, 실행 위치를 계산하기 위하여 QPos 값이 필요. --> 포기          #
        #
        # self.tableWidget.horizontalHeader().sectionClicked.connect(self.horClicked)
        ##############################################################################        

        # https://blog.naver.com/PostView.naver?blogId=anakt&logNo=221834285100&parentCategoryNo=&categoryNo=12&viewDate=&isShowPopularPosts=true&from=search
        # 
        # 행과 열을 하나씩 선택
        # self.tableWidget.selectRow()
        # self.tableWidget.selectColumn()
        #
        # 행과 열을 선택하고 그 값을 가져오기.
        # self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        # 컨트롤 키를 누르고 마우스를 클릭하면, 여러 Row를 동시 선택하고, 마우스만 클릭하면 하나의 Row를 선택하는 코드
        # self.tableWidget.cellClicked.connect(self.cell_click) # cellClick 이벤트를 감지하면 cell_click 함수를 실행
        # 선택된 셀에서 행번호 열번호 가져오기
        # x = self.tableWidget.selectedIndexes() # 리스트로 선택된 행번호와 열번호가 x에 입력된다.
        # x[0].row() #첫번째 선택된 행번호를 부르는 방법
        # x[0].column() #첫번째 선택된 열번호를 부르는 방법
        #################################################################################
        
        for row in range(0, len(self.my_data)-1) :
            for col in range(0, len(self.my_data[0])) :
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(self.my_data[row+1][col])))

        ##############################################################################
        # 그래프 영역 설정 #
        ##############################################################################
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        layout = QHBoxLayout()
        layoutLeft = QVBoxLayout()
        layoutRight = QVBoxLayout()
        layoutLeftTop = QVBoxLayout()
        layoutLeftBot = QHBoxLayout()
        
        labelGroup = QHBoxLayout()
        editGroup = QHBoxLayout()

        layout.addLayout(layoutLeft)
        layout.addLayout(layoutRight)
        layoutLeft.addLayout(labelGroup)
        layoutLeft.addLayout(editGroup)
        layoutLeft.addLayout(layoutLeftTop)
        layoutLeft.addLayout(layoutLeftBot)

        labelGroup.addWidget(self.lblSpeed)
        labelGroup.addWidget(self.lblTorque)
        labelGroup.addWidget(self.lblPower)
        labelGroup.addWidget(self.lblVoltage)
        labelGroup.addWidget(self.lblCurrent)
        labelGroup.addWidget(self.lblEff)
        editGroup.addWidget(self.editSpeed)
        editGroup.addWidget(self.editTorque)
        editGroup.addWidget(self.editPower)
        editGroup.addWidget(self.editVoltage)
        editGroup.addWidget(self.editCurrent)
        editGroup.addWidget(self.editEff)

        layoutLeftTop.addWidget(self.editSelection)
        layoutLeftTop.addWidget(self.tableWidget)
        layoutLeftBot.addWidget(self.signOK)
        layoutLeftBot.addWidget(self.signNO)
        layoutLeftBot.addWidget(self.toGraph)
        layoutRight.addWidget(self.canvas)

        self.setLayout(layout)
  
    ##############################################################################
    # context MENU 연결 슬롯. #
    # 1. header를 클릭하면
    # 2. 아이템(속도, 토오크... )을 순서데로 선택을 한다.
    # 3. 선택된 아이템이 맞는지 확인
    # 4. 선택을 하지 않는 경우, 예외 만들기.
    # headerItem = ('SPEED', 'TORQUE', 'POWER', 'VOLTAGE', 'CURRENT')
    ##############################################################################
    # context MENU 연결 슬롯. #
    ##############################################################################
    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_customContextMenuRequested(self, pos):
        
        cyan = Qt.cyan
        white = Qt.white
        
        print('on_customContextMenuRequested : pos = {}'.format(pos))
        it = self.tableWidget.itemAt(pos)
        if it is None:
            return
        c = it.column()
        item_range = QTableWidgetSelectionRange(
            0, c, self.tableWidget.rowCount()-1, c)
        self.tableWidget.setRangeSelected(item_range, True)

        menu = QMenu(self)
        spdAction = menu.addAction("to SPEED")
        tqAction  = menu.addAction("to TORQUE")
        poAction  = menu.addAction("to POWER")
        volAction = menu.addAction("to VOLTAGE")
        curAction = menu.addAction("to CURRENT")
        effAction = menu.addAction("to EFFICIENCY")
        drawAction = menu.addAction("DRAW GRAPH")
        unSelAction = menu.addAction("unSelected")
        action = menu.exec_(self.mapToGlobal(pos))
        # action = menu.exec_(self.table_widget.viewport().mapToGlobal(pos))
        if action == spdAction:
            # self.table_widget.removeColumn(c)
            self.colNo = self.tableWidget.selectedIndexes()[0].column()
            #
            # https://freeprog.tistory.com/333
            # 헤더 배경색 설정 --> app.setStyle 설정을 해야 함
            # 헤터 설정을 해야함. 자동으로 만들어진 헤더(숫자)의 색변경은 안됨.
            item = self.tableWidget.horizontalHeaderItem(self.colNo)

            if item is not None:
                item.setBackground(QBrush(cyan))
            # 아래는 셀 색상 변경.
            # for i in range(20):
                # item = self.table_widget.item(col, 0)
                # item.setBackground(QBrush(Qt.red))
                # self.table_widget.item(
                #     i, colNo).setBackground(QBrush(Qt.red))
            self.editSpeed.setText(self.my_data[0][self.colNo])
            self.colBankCal(self.colNo, True)

        elif action == tqAction:
            self.colNo = self.tableWidget.selectedIndexes()[0].column()
            item = self.tableWidget.horizontalHeaderItem(self.colNo)
            if item is not None:
                item.setBackground(QBrush(cyan))
            self.editTorque.setText(self.my_data[0][self.colNo])
            self.colBankCal(self.colNo, True)

        elif action == poAction:
            self.colNo = self.tableWidget.selectedIndexes()[0].column()
            item = self.tableWidget.horizontalHeaderItem(self.colNo)
            if item is not None:
                item.setBackground(QBrush(cyan))
            self.editPower.setText(self.my_data[0][self.colNo])
            self.colBankCal(self.colNo, True)

        elif action == volAction:
            self.colNo = self.tableWidget.selectedIndexes()[0].column()
            item = self.tableWidget.horizontalHeaderItem(self.colNo)
            if item is not None:
                item.setBackground(QBrush(cyan))
            self.editVoltage.setText(self.my_data[0][self.colNo])
            self.colBankCal(self.colNo, True)

        elif action == curAction:
            self.colNo = self.tableWidget.selectedIndexes()[0].column()
            item = self.tableWidget.horizontalHeaderItem(self.colNo)
            if item is not None:
                item.setBackground(QBrush(cyan))
            self.editCurrent.setText(self.my_data[0][self.colNo])
            self.colBankCal(self.colNo, True)

        elif action == effAction:
            self.colNo = self.tableWidget.selectedIndexes()[0].column()
            item = self.tableWidget.horizontalHeaderItem(self.colNo)
            if item is not None:
                item.setBackground(QBrush(cyan))
            self.editEff.setText(self.my_data[0][self.colNo])
            self.colBankCal(self.colNo, True)

        elif action == drawAction:
            self.colNo = self.tableWidget.selectedIndexes()[0].column()
            self.dataToGraph()

        elif action == unSelAction:
            self.colNo = self.tableWidget.selectedIndexes()[0].column()
            item = self.tableWidget.horizontalHeaderItem(self.colNo)
            if item is not None:
                item.setBackground(QBrush(white))
            self.colBankCal(self.colNo, False)

            if self.my_data[0][self.colNo] == self.editSpeed.text() :
                self.editSpeed.setText("")
            elif self.my_data[0][self.colNo] == self.editTorque.text() :
                self.editTorque.setText("")
            elif self.my_data[0][self.colNo] == self.editVoltage.text() :
                self.editVoltage.setText("")
            elif self.my_data[0][self.colNo] == self.editCurrent.text() :
                self.editCurrent.setText("")
            elif self.my_data[0][self.colNo] == self.editPower.text() :
                self.editPower.setText("")
            elif self.my_data[0][self.colNo] == self.editEff.text() :
                self.editEff.setText("")

    def colBankCal(self, val, Sel):
        # Sel == True : apped
        # Sel == False : pop

        if Sel == True :
            self.colBank.append(val)
        else :
            try :
                idx = self.colBank.index(val)
                self.colBank.pop(idx)
            except :
                QMessageBox.information(self, '데이타 없음. ',\
                        "삭제하려는 행은 선택하지 않았습니다.", QMessageBox.Ok)
        self.colBank.sort()

        selCol = list()
        if len(self.colBank) < 6 and len(self.colBank) > 0 :
            if self.colBank.count(val) > 0 :
                reply = QMessageBox.question(self, '아이템 중복', '덮어 쓰겠습니까?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes :
                    for col in range(0, len(self.colBank)):
                        selCol.append(self.my_data[0][self.colBank[col]])
                    self.editSelection.setText("열 : {}개, 값은 {} 입니다.".format(
                        len(self.colBank), selCol))
                    print("선택한 행 {}개, {} 입니다.".format(len(self.colBank), selCol))



        elif len(self.colBank) < 1:
            self.editSelection.setText("")
        else:
            QMessageBox.information(self, '항목 초과 ', \
                "아이템 삭제 후, 다시 선택하세요.", QMessageBox.Ok)
            
    def saveFile(self) :
        # self.colBank
        # self.my_data

        # newArray = np.zeros((self.my_data.shape(0),len(self.colBank)))
        newList = list()
        temp = list()

        for row in range(0, self.my_data.shape[0]):
            for col in self.colBank:
                print(row, col, self.my_data[row][col])
                temp.append(self.my_data[row][col])
            newList.append(temp)
            temp = list()  # list 를 초기화 할 것. 안그러면 데이타가 계속 쌓임.
        # print(newList)

        sf = plotGraph()
        sf.saveTextFile(self.name, newList)

    def dataToGraph(self):
        x = list()
        # print(type(self.my_data))
        # 이곳에서 받는 my_data(numpy array)는 문자열로 구성이되어 있음
        # 정수형으로 바꾸어 숫자를 계산을 하고 그래프를 그리는 것이 맞음
        # 단, 0번 행은 주석문이므로 스킵할 것.

        if self.colNo > 0:
            for row in range(1 , self.my_data.shape[0]-1):
                x.append(float(self.my_data[row+1][self.colNo]))
            # print(x)

            self.fig.clear()
            ax = self.fig.add_subplot(111)
            ax.plot(x)

            ax.set_xlabel("number of data")
            # ax.set_ylabel(self.my_data[0][self.colNo]) # 공간이 모자람.

            # print("min={0:.2f} max={1:.2f}".format(min(x), max(x)))
            ax.set_yticks(np.linspace(min(x), max(x), 5))

            ax.set_title(self.my_data[0][self.colNo])
            # ax.legend()
            ax.grid()
        
            self.canvas.draw()
        else :
            QMessageBox.information(self, '데이타 선택하지 않음. ',
                                    "COLUMN 선택--> 마우스 우클릭 --> Select", QMessageBox.Ok)

    #################################################################################
    # 마우스로 셀을 선택하는 루틴. 지금은 그다지 필요가 없을 듯...
    #################################################################################
    def cell_click(self):
        modifiers = QApplication.keyboardModifiers()  # pyqt에서의 키보드 입력 확인방법
        if modifiers == QtCore.Qt.ControlModifier:  # 마우스로 셀을 클릭했을 시에 컨트롤 키가 눌려져 있던 경우
            # 여러 셀이 함께 선택되도록 한다.
            self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        else:
            # 하나의 셀만 선택되도록 한다.
            self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        x = self.tableWidget.selectedIndexes()
        print(x[0].row(), x[0].column())
    #################################################################################


     
        
class plotGraph():
    def plot2D(self):
        self.fig = plt.Figure()

        x = [1, 2, 3, 4]

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(x) 

        ax.set_xlabel("x")
        ax.set_xlabel("y")

        # ax.set_title("Torque Set")
        ax.legend()
        ax.grid()
        self.canvas.draw()
    
    def saveTextFile(self, fileName, listData):
        pathName = os.path.dirname(fileName)
        fname = os.path.basename(fileName)  # 파일 이름만 추출함.
        nameOnly, tr = fname.split('.')

        # Debug - 데이타 확인 ----------
        f = open(pathName + '/' + nameOnly +
                 '_SEL.txt', 'w', encoding='utf-8', newline='')
        print(pathName + '/' + nameOnly + '_SEL.txt')
        wr = csv.writer(f, delimiter='\t')
        for line in listData:
            wr.writerow(line)
        # for line in listSecond:
        #     wr.writerow(line)
        f.close()
        # Debug - 저장 종료 ------------
        # QMessageBox.information(self, '새로운 파일 저장 ',
        #                         '_SEL.txt 파일이 생성되었습니다.', QMessageBox.Ok)
        # 메세지 박스가 왜 에러가 나는지 모르겠음. ???


