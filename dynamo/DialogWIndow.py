"""
  plotMotorChar_2.py 에 종속된 프로그램
  서브 윈도우에서 그래프를 그리고, 데이타를 추출하는 부분임.

"""

from PyQt5.QtWidgets import *
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
        self.setLayout(self.layout)
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
        # for row in range(0, len(listValue)) :
        #     for col in range(0, len(listValue[0])) :
        #         tableWidget.setItem(row, col, QTableWidgetItem(str(listValue[row][col])))

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

        self.layout = layout

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
        saveFile = startGraph()  # w저장은 startGraph 에서 수행을 함.
        saveFile.saveTextFile(self.name, self.tableData)

        # for col in range(0, len(self.my_data)) :
        #     value = self.tableWidget.item(0,col)
        #     self.tableData.append(float(value.text()))
        # print(self.tableData)
        self.close()  # 저장이 완료되면 닫음.

    def closeEvent(self, QCloseEvent):
        rtn = startGraph()
        rtn.saveSignalFalse()
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
        y = self.my_data[:, 2]

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

