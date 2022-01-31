"""
    2022.01.28.

    Magtrol Dynamometer Data(MDF) 데이타를 읽어서
    원하는 값을 추출하여 그래프를 그리는 프로그램

    별도의 클래스를 만들어 데이타를 연동하는 부분을 개선하였음.

"""

import os.path
import sys
import csv

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore,  QtWidgets

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

# import dynamo.DialogWIndow
# import dynamo.plotIO
# from dynamo.DialogWIndow import VietnamPackage 
# >> 클래스를 from 으로 호출하여 package 이름을 쓰지 않고 사용.

from dynamo import *
# from dynamo import plotIO 

class startGraph(QWidget):

    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self):

        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example'
        self.width = 720
        self.height = 600

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("Glory & Joy - Plot Motor Characteristic Curve")
        self.setWindowIcon(QIcon('./icon/line-chart.png'))
        # self.setFixedSize(self.width, self.height)
        self.move(50,50)

        self.textBrowser = QTextBrowser(self)  # 결과를 화면에 보여주기 위함.

        self.xAxisLabel = QLabel('X Axis : ')
        self.yAxisLabel = QLabel('Y Axis : ')
        self.zAxisLabel = QLabel('Z Axis : ')
        self.cMapLabel = QLabel('3D Color Pattern : ')

        axisList = ('torque', 'speed', 'power', 'iph', 'eff', 'effSys', 'volt')

        self.xAxisCombo = QComboBox(self)
        self.xAxisCombo.addItem('-선택하세요-')
        for item in axisList:
            self.xAxisCombo.addItem(item)
        self.xAxisCombo.setCurrentIndex(2)  # 자주쓰는 값을 지정 함.

        self.yAxisCombo = QComboBox(self)
        self.yAxisCombo.addItem('-선택하세요-')
        for item in axisList:
            self.yAxisCombo.addItem(item)
        self.yAxisCombo.setCurrentIndex(1)  # 자주쓰는 값을 지정 함.

        self.zAxisCombo = QComboBox(self)
        self.zAxisCombo.addItem('-선택하세요-')
        for item in axisList:
            self.zAxisCombo.addItem(item)
        self.zAxisCombo.setCurrentIndex(5)  # 자주쓰는 값을 지정 함.

        cmaps = ('viridis', 'plasma', 'inferno', 'magma', 'RdBu_r')
        self.cMapCombo = QComboBox(self)
        for cmap in cmaps:
            self.cMapCombo.addItem(cmap)
        # self.zAxisCombo.setCurrentIndex(5)  # 자주쓰는 값을 지정 함.

        self.rbtn1 = QRadioButton('Surface Plot', self)
        # rbtn1.move(50, 50)
        self.rbtn1.setChecked(True)
        self.rbtn1.clicked.connect(self.radioButtonClicked)

        self.rbtn2 = QRadioButton('Multi Axis', self)
        # rbtn2.move(50, 70)
        self.rbtn2.clicked.connect(self.radioButtonClicked)

        self.rbtn3 = QRadioButton('Contourf', self)
        # rbtn1.move(50, 50)
        self.rbtn3.clicked.connect(self.radioButtonClicked)

        self.rbtn4 = QRadioButton('Contour ', self)
        # rbtn1.move(50, 50)
        self.rbtn4.clicked.connect(self.radioButtonClicked)

        self.limRadio = QRadioButton('Apply to min/max of the Axis', self)

        unitMaps = ('Speed [r/min]', 'Torque [N.m]', 'Power [W]', 'Voltage [V]', 'Current [A]', 'Efficiency [%]')
        self.uMapCombo0 = QComboBox(self)
        for unitMap in unitMaps:
            self.uMapCombo0.addItem(unitMap)
        self.uMapCombo0.setCurrentIndex(0)  # 자주쓰는 값을 지정 함.

        self.uMapCombo1 = QComboBox(self)
        for unitMap in unitMaps:
            self.uMapCombo1.addItem(unitMap)
        self.uMapCombo1.setCurrentIndex(1)  # 자주쓰는 값을 지정 함.

        self.uMapCombo2 = QComboBox(self)
        for unitMap in unitMaps:
            self.uMapCombo2.addItem(unitMap)
        self.uMapCombo2.setCurrentIndex(2)  # 자주쓰는 값을 지정 함.

        self.uMapCombo3 = QComboBox(self)
        for unitMap in unitMaps:
            self.uMapCombo3.addItem(unitMap)
        self.uMapCombo3.setCurrentIndex(3)  # 자주쓰는 값을 지정 함.

        self.uMapCombo4 = QComboBox(self)
        for unitMap in unitMaps:
            self.uMapCombo4.addItem(unitMap)
        self.uMapCombo4.setCurrentIndex(4)  # 자주쓰는 값을 지정 함.

        self.uMapCombo5 = QComboBox(self)
        for unitMap in unitMaps:
            self.uMapCombo5.addItem(unitMap)
        self.uMapCombo5.setCurrentIndex(5)  # 자주쓰는 값을 지정 함.

        # min-max 값 설정
        self.min1 = QLineEdit('0')  # Speed min
        self.max1 = QLineEdit('16000')  # Speed max

        self.min2 = QLineEdit('0')
        self.max2 = QLineEdit('5')

        self.min3 = QLineEdit('0')
        self.max3 = QLineEdit('1000')

        self.min4 = QLineEdit('0')
        self.max4 = QLineEdit('300')

        self.min5 = QLineEdit('0')
        self.max5 = QLineEdit('5')

        self.min6 = QLineEdit('0')
        self.max6 = QLineEdit('100')

        self.min_max_label = QLabel('2D Graph Min-Max Set')

        #  multiAxis에서 사용할 한계치 설정을 함.
        self.checkVolt = QCheckBox('Max Voltage', self)
        self.maxVoltage = QLineEdit('300')
        # self.maxVoltage.textChanged.connect(self.reLoadData)
        self.checkCurrent = QCheckBox('Max Current', self)
        self.maxCurrent = QLineEdit('5')
        self.checkTq = QCheckBox('Max Torque', self)
        self.maxTorque = QLineEdit('5')
        self.maxTorque.textChanged.connect(self.reLoadData)

        self.openFiles = QPushButton("파일", self)
        # self.plotG.move(520, 20)
        # self.plotG.resize(80, 80)
        self.openFiles.clicked.connect(self.openDialog)
        self.openFiles.setToolTip('계산할 데이타를 선택합니다.')
        self.openFiles.setStyleSheet('background-color:#E0ECF8')
        # 색상코드보기 : https://html-color-codes.info/Korean/

        self.plotG = QPushButton("그리기", self)
        # self.plotG.move(520, 20)
        # self.plotG.resize(80, 80)
        self.plotG.clicked.connect(self.selectGraph)
        self.plotG.setToolTip("그래프를 그립니다..")
        self.plotG.setStyleSheet('background-color:#E0ECF8')
        # 색상코드보기 : https://html-color-codes.info/Korean/

        self.readMDF = QPushButton("MDF", self)
        self.readMDF.clicked.connect(self.openMdfDialog)
        self.readMDF.setToolTip("MDF 를 txt 로 변환합니다.")
        self.readMDF.setStyleSheet('background-color:#FF0000')
        # 색상코드보기 : https://html-color-codes.info/Korean/

        # ioTool = dynamo.plotIO.changeFolder()
        # ioTool.openPath()
        trip_to = plotIO.ThailandPackage()
        trip_to.detail()

        self.readPath = QPushButton("작업경로", self)
        self.readPath.clicked.connect(self.openPath)
        self.readPath.setToolTip("작업 경로를 설정합니다.")
        self.readPath.setStyleSheet('background-color:#CEECF5')
        # 색상코드보기 : https://html-color-codes.info/Korean/
        self.readPathInfo = QLineEdit('c:/')

        # 원래 그래프를 그리기 위해 만들어 놓은 것인데.
        # 당장은 필요없을 듯 함.
        # self.fig = plt.Figure()
        # self.canvas = FigureCanvas(self.fig)
        # self.fig.subplots_adjust(bottom=0.3, left=0.15)

        self.MatrixLable = QLabel('N x N')
        self.Matrix = QLineEdit('15')
        self.numArray = int(self.Matrix.text())
        self.Matrix.textChanged.connect(self.reChangeArray)

        self.divTickLabel = QLabel('division ticks')
        self.divTickEdit = QLineEdit('5')
        # self.divQline.textChanged.connect(self.reChangeArray)

        #
        # Layout Setting .........................
        #
        #배치될 위젯 변수 선언
        # [1] Group Layout 만들기
        grp_1 = QGroupBox("Graph Type")
        grp_2 = QGroupBox("Option ")
        grp_3 = QGroupBox("Parameter 1")
        grp_4 = QGroupBox("Parameter 2")
        grp_5 = QGroupBox("Parameter 3")
        grp_6 = QGroupBox("Parameter 4")
        grp_7 = QGroupBox("Parameter 5")
        grp_8 = QGroupBox("Parameter 6")
        grp_axis = QGroupBox('Select Axis')
        grp_Limits = QGroupBox('Limits - Voltage / Current / Torque')

        # [2] 레이아웃 선언 및 Form Widget 만들기
        leftTopLayout = QHBoxLayout()
        grp_1_Layout = QBoxLayout(QBoxLayout.TopToBottom)
        grp_2_Layout = QBoxLayout(QBoxLayout.TopToBottom)
        grp_3_Layout = QBoxLayout(QBoxLayout.TopToBottom)
        grp_4_Layout = QBoxLayout(QBoxLayout.TopToBottom)
        grp_5_Layout = QBoxLayout(QBoxLayout.TopToBottom)
        grp_6_Layout = QBoxLayout(QBoxLayout.TopToBottom)
        grp_7_Layout = QBoxLayout(QBoxLayout.TopToBottom)
        grp_8_Layout = QBoxLayout(QBoxLayout.TopToBottom)
        grp_axis_Layout = QBoxLayout(QBoxLayout.TopToBottom)
        limits_Layout = QBoxLayout(QBoxLayout.TopToBottom)


        # [3] Layout 을 GroupBox에 넣는다.
        grp_1.setLayout(grp_1_Layout)
        grp_2.setLayout(grp_2_Layout)
        grp_3.setLayout(grp_3_Layout)
        grp_4.setLayout(grp_4_Layout)
        grp_5.setLayout(grp_5_Layout)
        grp_6.setLayout(grp_6_Layout)
        grp_7.setLayout(grp_7_Layout)
        grp_8.setLayout(grp_8_Layout)
        grp_axis.setLayout(grp_axis_Layout)
        grp_Limits.setLayout(limits_Layout)

        # [4] GroupLayout에 Widget을 넣는다.
        grp_1_Layout.addWidget(self.rbtn1)
        grp_1_Layout.addWidget(self.rbtn2)
        grp_1_Layout.addWidget(self.rbtn3)
        grp_1_Layout.addWidget(self.rbtn4)

        grp_axis_Small_x = QHBoxLayout()
        grp_axis_Small_y = QHBoxLayout()
        grp_axis_Small_z = QHBoxLayout()

        grp_axis_Small_x.addWidget(self.xAxisLabel)
        grp_axis_Small_x.addWidget(self.xAxisCombo)
        grp_axis_Small_y.addWidget(self.yAxisLabel)
        grp_axis_Small_y.addWidget(self.yAxisCombo)
        grp_axis_Small_z.addWidget(self.zAxisLabel)
        grp_axis_Small_z.addWidget(self.zAxisCombo)

        grp_axis_Layout.addWidget(grp_axis)
        grp_axis_Layout.addLayout(grp_axis_Small_x)
        grp_axis_Layout.addLayout(grp_axis_Small_y)
        grp_axis_Layout.addLayout(grp_axis_Small_z)

        grp_2_Layout.addWidget(self.limRadio)  # 3D 그래프에서 min-max를 적용을 할껀지.
        grp_2_SmallLayout1 = QHBoxLayout()
        grp_2_SmallLayout2 = QHBoxLayout()
        grp_2_SmallLayout3 = QHBoxLayout()
        grp_2_SmallLayout1.addWidget(self.cMapLabel)
        grp_2_SmallLayout1.addWidget(self.cMapCombo) # 색상 선택
        grp_2_Layout.addLayout(grp_2_SmallLayout3)
        grp_2_Layout.addLayout(grp_2_SmallLayout1)
        grp_2_Layout.addLayout(grp_2_SmallLayout2)
        grp_2_SmallLayout2.addWidget(self.MatrixLable)
        grp_2_SmallLayout2.addWidget(self.Matrix, 10)
        grp_2_SmallLayout3.addWidget(self.divTickLabel)
        grp_2_SmallLayout3.addWidget(self.divTickEdit, 10)

        limitsVoltage = QHBoxLayout()
        limitsCurrent = QHBoxLayout()
        limitsTorque = QHBoxLayout()

        limits_Layout.addLayout(limitsVoltage)
        limits_Layout.addLayout(limitsCurrent)
        limits_Layout.addLayout(limitsTorque)

        limitsVoltage.addWidget(self.checkVolt)
        limitsVoltage.addWidget(self.maxVoltage)
        limitsCurrent.addWidget(self.checkCurrent)
        limitsCurrent.addWidget(self.maxCurrent)
        limitsTorque.addWidget(self.checkTq)
        limitsTorque.addWidget(self.maxTorque)

        # [5] GroupLayout을 마지막 Layout에 넣는다.
        leftTopLayout.addLayout(grp_1_Layout)
        leftTopLayout.addLayout(grp_axis_Layout)
        leftTopLayout.addLayout(grp_2_Layout)
        leftTopLayout.addLayout(limits_Layout)

        leftTopLayout.addWidget(grp_1)
        leftTopLayout.addWidget(grp_axis)
        leftTopLayout.addWidget(grp_2)
        leftTopLayout.addWidget(grp_Limits)
        # ========= leftTopLayout 완료 ================

        left_3Layout = QHBoxLayout()
        grp_3_Layout.addWidget(self.uMapCombo0)
        grp_3_Layout.addWidget(self.min1)
        grp_3_Layout.addWidget(self.max1)
        grp_4_Layout.addWidget(self.uMapCombo1)
        grp_4_Layout.addWidget(self.min2)
        grp_4_Layout.addWidget(self.max2)
        grp_5_Layout.addWidget(self.uMapCombo2)
        grp_5_Layout.addWidget(self.min3)
        grp_5_Layout.addWidget(self.max3)
        grp_6_Layout.addWidget(self.uMapCombo3)
        grp_6_Layout.addWidget(self.min4)
        grp_6_Layout.addWidget(self.max4)
        grp_7_Layout.addWidget(self.uMapCombo4)
        grp_7_Layout.addWidget(self.min5)
        grp_7_Layout.addWidget(self.max5)
        grp_8_Layout.addWidget(self.uMapCombo5)
        grp_8_Layout.addWidget(self.min6)
        grp_8_Layout.addWidget(self.max6)
        left_3Layout.addLayout(grp_3_Layout)
        left_3Layout.addLayout(grp_4_Layout)
        left_3Layout.addLayout(grp_5_Layout)
        left_3Layout.addLayout(grp_6_Layout)
        left_3Layout.addLayout(grp_7_Layout)
        left_3Layout.addLayout(grp_8_Layout)

        left_3Layout.addWidget(grp_3)
        left_3Layout.addWidget(grp_4)
        left_3Layout.addWidget(grp_5)
        left_3Layout.addWidget(grp_6)
        left_3Layout.addWidget(grp_7)
        left_3Layout.addWidget(grp_8)

        left_5Layout = QHBoxLayout()
        left_5Layout.addWidget(self.min_max_label) #

        leftBottomLayout = QVBoxLayout()
        # leftLayout.addWidget(self.canvas)
        leftBottomLayout.addWidget(self.readPath)
        leftBottomLayout.addWidget(self.readPathInfo)
        leftBottomLayout.addWidget(self.textBrowser)

        leftLayout = QVBoxLayout()
        leftLayout.addLayout(leftTopLayout)
        leftLayout.addLayout(left_5Layout)
        leftLayout.addLayout(left_3Layout)  # min-max input line
        leftLayout.addLayout(leftBottomLayout)

        # Right Layout
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.openFiles)
        rightLayout.addWidget(self.plotG)
        rightLayout.addStretch(1)
        rightLayout.addWidget(self.readMDF)
        rightLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        # layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)

        self.dataLogic= False
        self.fileNameSign = False

        self.setLayout(layout)

        # 사용 설명서 불러오기
        f = open('./usage.txt', 'r', encoding = 'utf-8')
        line_num = 1
        lines = f.readlines()
        for line in lines :
            self.textBrowser.append(line)
        f.close()

        # path 불러오기
        f = open('./folderHistory.ini', 'r', encoding='utf-8')
        self.readPathInfo.setText(f.read())
        f.close()

    def openPath(self):
        FileFolder = QFileDialog.getExistingDirectory(self, 'Find Folder')

        if not FileFolder :
            buttonReply = QMessageBox.information(self, '작업 폴더 선택', \
                "폴더를 선택하지 않았습니다.", QMessageBox.Ok)
        else :
            buttonReply = QMessageBox.information(self, '작업 폴더 선택', \
                FileFolder + "가 선택되었습니다.", QMessageBox.Ok)
            self.readPathInfo.setText(FileFolder)

            # 표준위치에 경로 저장
            f = open('./folderHistory.ini', 'w', encoding='utf-8', newline='')
            f.write(self.readPathInfo.text())
            f.close()

    def fileToArray(self, fileName):

        # numpy array로 데이타 읽기
        # 다이나모 데이타에서 curve 로 측정을 하면 1줄은 '주석', 2 ~ 3줄은 NaN 이 있으므로
        # header 는 3으로 하여 데이타를 넘어가도록 한다.
        # 읽는 데이타 타입은 실수형으로 한다.
        # my_data = np.genfromtxt(fileName, delimiter='\t', skip_header=3, dtype='float')
        skipHeadLines = 4
        f = open(fileName, 'r')
        data = list()
        readData = list()
        tr = csv.reader(f, delimiter='\t')
        for row in tr:
            data.append(row)

        for row in range(skipHeadLines, len(data)-1):
            # print(data[row])
            readData.append(self.listStrToFloat(data[row]))

        rtnArray = np.array(readData)

        return rtnArray

    def listStrToFloat(self, s):
        # initialization of convert a list
        new = list()

        # traverse in the string
        for x in s:
            new.append(float(x))
        return new

    def reLoadData(self):
        # 최대 토오크 값이 변경이 되면 데이타를 다시 불러옴
        if self.fileNameSign :
            self.loadFromFiles()

    def reChangeArray(self):
        try :
            self.numArray = int(self.Matrix.text())
            # array 개수가 변환되면 array를 재계산한다.0
            if self.dataLogic:
                self.dataLogic = True
                self.loadFromFiles()
            else :
                # print('file not selected!')
                QMessageBox.warning(self, '경고','계산할 파일을 선택하세요.')
        except :
            QMessageBox.warning(self, '경고','정수형으로 입력하세요.')

    def radioButtonClicked(self):
        if self.rbtn1.isChecked():
            self.textBrowser.append('3D Map is checked !')
        elif self.rbtn2.isChecked():
            self.textBrowser.append(('Multi Axis is checked !'))
        elif self.rbtn3.isChecked():
            self.textBrowser.append(('Contourf Plot is checked !'))
        elif self.rbtn4.isChecked():
            self.textBrowser.append(('Contour Plot is checked !'))

        if self.limRadio.isChecked():
            self.textBrowser.append('모든 그래프의 축에 최소/최대값을 적용합니다.')

    def selectGraph(self):
        # https://dev-guardy.tistory.com/51 입력값이 숫자인 경우만 실행.
        try: # 입력 변수가 문자로 들어오는 경우 방지함.
            float(self.min1.text())
            float(self.max1.text())
            float(self.min2.text())
            float(self.max2.text())
            float(self.min3.text())
            float(self.max2.text())
            float(self.min4.text())
            float(self.max4.text())
            float(self.min5.text())
            float(self.max3.text())
            float(self.max5.text())
            float(self.min6.text())
            float(self.max6.text())
            # float(self.fileNameSign)  # 정수
            int(self.divTickEdit.text()) # 정수
            float(self.maxVoltage.text())
            float(self.maxCurrent.text())

            self.divTick = int(self.divTickEdit.text())  # 3차원 x-thick 개수 설정

            if self.rbtn1.isChecked():
                self.map3D()
            elif self.rbtn2.isChecked():
                self.multiAxis()
            elif self.rbtn3.isChecked():
                self.contourPlot()
            elif self.rbtn4.isChecked():
                self.contourPlot()

        except:
            QMessageBox.warning(self, '경고', '입력값이 정수 또는 실수 이어야 합니다. 단, ticks 는 정수. \n'
                                            '또는 입력 데이타가 잘못되었습니다.')

    def contourPlot(self):

        self.checkCombo() # 현재 콤보 셋팅값을 가져옴

        if self.dataLogic :
            # axisList = ('torque', 'speed', 'power', 'iph', 'eff', 'effSys')
            # self.textBrowser.append('xAxis:' + self.xAxisCombo.currentText() +' ' + str(self.xAxisCombo.currentIndex()))
            # self.textBrowser.append('yAxis:' + self.yAxisCombo.currentText() +' ' + str(self.yAxisCombo.currentIndex()))
            # self.textBrowser.append('zAxis:' + self.zAxisCombo.currentText() +' ' + str(self.zAxisCombo.currentIndex()))

            # parameter Z 에 대하여 콤보값 가져오기.
            if self.zAxisCombo.currentIndex() == 1:  # Torque combp
                lvl = 15
            elif self.zAxisCombo.currentIndex() == 2:  # SPEED Combo
                lvl = 15
            elif self.zAxisCombo.currentIndex() == 3:  # Power Combo
                lvl = 15
            elif self.zAxisCombo.currentIndex() == 4:  # Current Combo
                lvl = 15
            elif self.zAxisCombo.currentIndex() == 5:  # Eff Combo
                lvl = np.linspace(10, 100, 19)
            elif self.zAxisCombo.currentIndex() == 6:  # Eff Sys Combo
                lvl = np.linspace(10, 100, 19)
            elif self.zAxisCombo.currentIndex() == 7:  # Voltage Combo
                lvl = np.linspace(10, 200, 20)
            # lvl = np.linspace(10, 200, 20)

            fig, ax = plt.subplots()  # 신규 추가
            if self.rbtn3.isChecked() :
                contour = ax.contourf(self.paraX, self.paraY, self.paraZ, levels = lvl, cmap=self.cMapCombo.currentText())
                fig.colorbar(contour)

            elif self.rbtn4.isChecked() :
                contour = ax.contour(self.paraX, self.paraY, self.paraZ, cmap=self.cMapCombo.currentText())

            # contour = plt.contour(self.paraX, self.paraY, self.paraZ, levels=15,  colors = 'k')
            # cntr = plt.contourf(self.paraX, self.paraY, self.paraZ, levels=15, cmap=self.cMapCombo.currentText())

            if self.limRadio.isChecked() :
                # parameter X 에 대하여 콤보값 가져오기.
                if self.xAxisCombo.currentIndex() == 1: # Torque combp
                    ax.set_xticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_xlim(float(self.min2.text()), float(self.max2.text()))
                elif self.xAxisCombo.currentIndex() == 2: # SPEED Combo
                    ax.set_xticks(np.linspace(float(self.min1.text()), float(self.max1.text()), self.divTick))
                    ax.set_xlim(float(self.min1.text()), float(self.max1.text()))
                elif self.xAxisCombo.currentIndex() == 3: # Power Combo
                    ax.set_xticks(np.linspace(float(self.min3.text()), float(self.max3.text()), self.divTick))
                    ax.set_xlim(float(self.min3.text()), float(self.max3.text()))
                elif self.xAxisCombo.currentIndex() == 4: # Current Combo
                    ax.set_xticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_xlim(float(self.min2.text()), float(self.max2.text()))
                elif self.xAxisCombo.currentIndex() == 5: # Eff Combo
                    ax.set_xticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_xlim(float(self.min6.text()), float(self.max6.text()))
                elif self.xAxisCombo.currentIndex() == 6: # Eff Sys Combo
                    ax.set_xticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_xlim(float(self.min6.text()), float(self.max6.text()))
                elif self.xAxisCombo.currentIndex() == 7: # Voltage Combo
                    ax.set_xticks(np.linspace(float(self.min4.text()), float(self.max4.text()), self.divTick))
                    ax.set_xlim(float(self.min4.text()), float(self.max4.text()))

                # parameter Y 에 대하여 콤보값 가져오기.
                if self.yAxisCombo.currentIndex() == 1:  # Torque combp
                    ax.set_yticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_ylim(float(self.min2.text()), float(self.max2.text()))
                elif self.yAxisCombo.currentIndex() == 2:  # SPEED Combo
                    ax.set_yticks(np.linspace(float(self.min1.text()), float(self.max1.text()), self.divTick))
                    ax.set_ylim(float(self.min1.text()), float(self.max1.text()))
                elif self.yAxisCombo.currentIndex() == 3:  # Power Combo
                    ax.set_yticks(np.linspace(float(self.min3.text()), float(self.max3.text()), self.divTick))
                    ax.set_ylim(float(self.min3.text()), float(self.max3.text()))
                elif self.yAxisCombo.currentIndex() == 4:  # Current Combo
                    ax.set_yticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_ylim(float(self.min2.text()), float(self.max2.text()))
                elif self.yAxisCombo.currentIndex() == 5:  # Eff Combo
                    ax.set_yticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_ylim(float(self.min6.text()), float(self.max6.text()))
                elif self.yAxisCombo.currentIndex() == 6:  # Eff Sys Combo
                    ax.set_yticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_ylim(float(self.min6.text()), float(self.max6.text()))
                elif self.yAxisCombo.currentIndex() == 7:  # Voltage Combo
                    ax.set_yticks(np.linspace(float(self.min4.text()), float(self.max4.text()), self.divTick))
                    ax.set_ylim(float(self.min4.text()), float(self.max4.text()))

            #     # parameter Z 에 대하여 콤보값 가져오기.
            #     if self.zAxisCombo.currentIndex() == 1:  # Torque combp
            #         lvl = 10
            #     elif self.zAxisCombo.currentIndex() == 2:  # SPEED Combo
            #         lvl = 10
            #     elif self.zAxisCombo.currentIndex() == 3:  # Power Combo
            #         lvl = 10
            #     elif self.zAxisCombo.currentIndex() == 4:  # Current Combo
            #         lvl = 10
            #     elif self.zAxisCombo.currentIndex() == 5:  # Eff Combo
            #         lvl = 10
            #     elif self.zAxisCombo.currentIndex() == 6:  # Eff Sys Combo
            #         lvl = [60, 70, 80, 90]
            #     elif self.zAxisCombo.currentIndex() == 7:  # Voltage Combo
            #         lvl = 10
            # print(lvl)


            plt.xlabel(self.xLabel)
            plt.ylabel(self.yLabel)
            plt.ylabel(self.yLabel)
            plt.title('Map is ' + self.zLabel)
            plt.grid()
            ax.clabel(contour, inline=True, fontsize=10, fmt='%3.1f', colors='black')
            # contour.levels = [ 70, 80, 90]
            # ax.clabel(contourinline=True, fontsize=10, fmt='%3.1f', colors='black')
            # https://python-course.eu/numerical-programming/contour-plots-with-matplotlib.php

            plt.tight_layout()
            plt.show()
        else :
            self.textBrowser.append('계산할 파일을 선택하세요.')
            QMessageBox.warning(self, '경고','계산할 파일을 선택하세요.')

    def map3D(self):
        self.checkCombo()  # 현재 콤보 셋팅값을 가져옴

        if self.dataLogic :
            # axisList = ('torque', 'speed', 'power', 'iph', 'eff', 'effSys')
            self.textBrowser.append('xAxis:' + self.xAxisCombo.currentText() +' ' + str(self.xAxisCombo.currentIndex()))
            self.textBrowser.append('yAxis:' + self.yAxisCombo.currentText() +' ' + str(self.yAxisCombo.currentIndex()))
            self.textBrowser.append('zAxis:' + self.zAxisCombo.currentText() +' ' + str(self.zAxisCombo.currentIndex()))

            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})  # 신규 추가
            # ax.plot_surface(speed, tq, eff, cmap='viridis')
            surf = ax.plot_surface(self.paraX, self.paraY, self.paraZ, cmap=self.cMapCombo.currentText())
            # ax.set_zlim(0, 100)
            # ax.set_xticks([500, 700, 900, 1100, 1300])
            # ax.set_yticks([0, 1, 2, 3, 4, 5])
            # ax.set_zticks([-5, 0, 5])
            ax.set_xlabel(self.xLabel)
            ax.set_ylabel(self.yLabel)
            ax.set_zlabel(self.zLabel)

            if self.limRadio.isChecked() :
                if self.xAxisCombo.currentIndex() == 1: # Torque combp
                    ax.set_xticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_xlim(float(self.min2.text()), float(self.max2.text()))
                elif self.xAxisCombo.currentIndex() == 2: # SPEED Combo
                    ax.set_xticks(np.linspace(float(self.min1.text()), float(self.max1.text()), self.divTick))
                    ax.set_xlim(float(self.min1.text()), float(self.max1.text()))
                elif self.xAxisCombo.currentIndex() == 3: # Power Combo
                    ax.set_xticks(np.linspace(float(self.min3.text()), float(self.max3.text()), self.divTick))
                    ax.set_xlim(float(self.min3.text()), float(self.max3.text()))
                elif self.xAxisCombo.currentIndex() == 4: # Current Combo
                    ax.set_xticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_xlim(float(self.min2.text()), float(self.max2.text()))
                elif self.xAxisCombo.currentIndex() == 5: # Eff Combo
                    ax.set_xticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_xlim(float(self.min6.text()), float(self.max6.text()))
                elif self.xAxisCombo.currentIndex() == 6: # Eff Sys Combo
                    ax.set_xticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_xlim(float(self.min6.text()), float(self.max6.text()))
                elif self.xAxisCombo.currentIndex() == 7: # Voltage Combo
                    ax.set_xticks(np.linspace(float(self.min4.text()), float(self.max4.text()), self.divTick))
                    ax.set_xlim(float(self.min4.text()), float(self.max4.text()))

                        # parameter Y 에 대하여 콤보값 가져오기.
                if self.yAxisCombo.currentIndex() == 1:  # Torque combp
                    ax.set_yticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_ylim(float(self.min2.text()), float(self.max2.text()))
                elif self.yAxisCombo.currentIndex() == 2:  # SPEED Combo
                    ax.set_yticks(np.linspace(float(self.min1.text()), float(self.max1.text()), self.divTick))
                    ax.set_ylim(float(self.min1.text()), float(self.max1.text()))
                elif self.yAxisCombo.currentIndex() == 3:  # Power Combo
                    ax.set_yticks(np.linspace(float(self.min3.text()), float(self.max3.text()), self.divTick))
                    ax.set_ylim(float(self.min3.text()), float(self.max3.text()))
                elif self.yAxisCombo.currentIndex() == 4:  # Current Combo
                    ax.set_yticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_ylim(float(self.min2.text()), float(self.max2.text()))
                elif self.yAxisCombo.currentIndex() == 5:  # Eff Combo
                    ax.set_yticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_ylim(float(self.min6.text()), float(self.max6.text()))
                elif self.yAxisCombo.currentIndex() == 6:  # Eff Sys Combo
                    ax.set_yticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_ylim(float(self.min6.text()), float(self.max6.text()))
                elif self.yAxisCombo.currentIndex() == 7:  # Voltage Combo
                    ax.set_yticks(np.linspace(float(self.min4.text()), float(self.max4.text()), self.divTick))
                    ax.set_ylim(float(self.min4.text()), float(self.max4.text()))

                    # parameter Z 에 대하여 콤보값 가져오기.
                if self.zAxisCombo.currentIndex() == 1:  # Torque combp
                    ax.set_zticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_zlim(float(self.min2.text()), float(self.max2.text()))
                elif self.zAxisCombo.currentIndex() == 2:  # SPEED Combo
                    ax.set_zticks(np.linspace(float(self.min1.text()), float(self.max1.text()), self.divTick))
                    ax.set_zlim(float(self.min1.text()), float(self.max1.text()))
                elif self.zAxisCombo.currentIndex() == 3:  # Power Combo
                    ax.set_zticks(np.linspace(float(self.min3.text()), float(self.max3.text()), self.divTick))
                    ax.set_zlim(float(self.min3.text()), float(self.max3.text()))
                elif self.zAxisCombo.currentIndex() == 4:  # Current Combo
                    ax.set_zticks(np.linspace(float(self.min2.text()), float(self.max2.text()), self.divTick))
                    ax.set_zlim(float(self.min2.text()), float(self.max2.text()))
                elif self.zAxisCombo.currentIndex() == 5:  # Eff Combo
                    ax.set_zticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_zlim(float(self.min6.text()), float(self.max6.text()))
                elif self.zAxisCombo.currentIndex() == 6:  # Eff Sys Combo
                    ax.set_zticks(np.linspace(float(self.min6.text()), float(self.max6.text()), self.divTick))
                    ax.set_zlim(float(self.min6.text()), float(self.max6.text()))
                elif self.zAxisCombo.currentIndex() == 7:  # Voltage Combo
                    ax.set_zticks(np.linspace(float(self.min4.text()), float(self.max4.text()), self.divTick))
                    ax.set_zlim(float(self.min4.text()), float(self.max4.text()))


            fig.colorbar(surf, shrink=0.6, aspect=8)
            surf.set_clim(self.paraZ.min(), self.paraZ.max())

            fig.tight_layout()
            plt.show()
        else :
            self.textBrowser.append('계산할 파일을 선택하세요.')
            QMessageBox.warning(self, '경고','계산할 파일을 선택하세요.')

    def multiAxis(self):

        if self.dataLogic:
            # self.fig.clf()  # 일단 화면을 깨끗이 지우기 시작. CANVAS 사용할 때 화면 지우기.
            # Create figure and subplot manually
            # fig = plt.figure()
            # host = fig.add_subplot(111)

            # More versatile wrapper
            # fig, host = plt.subplots(figsize=(10, 5))  # (width, height) in inches
            self.fig, host = plt.subplots(figsize=(10, 5))  # (width, height) in inches
            # (see https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.subplots.html)
            # https://matplotlib.org/3.3.3/gallery/ticks_and_spines/multiple_yaxis_with_spines.html#sphx-glr-gallery-ticks-and-spines-multiple-yaxis-with-spines-py

            par1 = host.twinx()  # Speed - Torque
            par2 = host.twinx()  # Speed - Power
            par3 = host.twinx()  # Speed - Voltage
            par4 = host.twinx()  # Speed - Current
            par5 = host.twinx()  # Speed - Efficiency

            host.set_xlim(float(self.min1.text()), float(self.max1.text()))  # Speed SET
            host.set_ylim()       # 빈거.
            par1.set_ylim(float(self.min2.text()), float(self.max2.text()))  # Torque SET
            par2.set_ylim(float(self.min3.text()), float(self.max3.text()))  # Power SET
            par3.set_ylim(float(self.min4.text()), float(self.max4.text()))  # Voltage SET
            par4.set_ylim(float(self.min5.text()), float(self.max5.text()))  # Current SET
            par5.set_ylim(float(self.min6.text()), float(self.max6.text()))  # Efficieny SET

            lbl0 = "Speed [r/min]"
            lbl1 = "Torque [N$\cdot$m]"
            lbl2 = "Power [W]"
            lbl3 = "Voltage [V]"
            lbl4 = "Current [A]"
            lbl5 = "Efficiency [%]"

            host.set_xlabel(lbl0)
            host.set_ylabel('')
            par1.set_ylabel(lbl1)
            par2.set_ylabel(lbl2)
            par3.set_ylabel(lbl3)
            par4.set_ylabel(lbl4)
            par5.set_ylabel(lbl5)

            color1 = '#DF0101'  # red
            color2 = '#0000FF'  # blue
            color3 = '#00FF40'  # green
            color4 = '#FF00FF'  # cyan
            color5 = '#81F7F3'  # sky blue

            # https://zephyrus1111.tistory.com/17
            # 다양한 선 종류 만들기.
            line_type = {'-': '-',
                         '--': '--',
                         '-.': '-.',
                         ':': ':'}
            yticks_label = list(line_type.keys())

            # ======= 정리된 변수 목록 =======
            # self.speed
            # self.tq
            # self.po
            # self.volt
            # self.cur
            # self.eff
            # self.effS
            # =============================
            row, col = self.speed.shape  # 행과 열의 전체 개수를 추출함. m x n Matrix.
            # print(self.speed[row-1, :])

            # line 종류, 레이블
            p1, = par1.plot(self.speed[row-1, :].tolist(), self.tq[row-1, :].tolist(), color=color1, label=lbl1, linestyle='solid')
            p2, = par2.plot(self.speed[row-1, :].tolist(), self.po[row-1, :].tolist(), color=color2, label=lbl2, linestyle='dashed')
            p3, = par3.plot(self.speed[row-1, :].tolist(), self.volt[row-1, :].tolist(), color=color3, label=lbl3, linestyle='dashdot')
            p4, = par4.plot(self.speed[row-1, :].tolist(), self.cur[row-1, :].tolist(), color=color4, label=lbl4, linestyle=line_type[yticks_label[2]], linewidth=2.0)
            p5, = par5.plot(self.speed[row-1, :].tolist(), self.eff[row-1, :].tolist(), color=color5, label=lbl5, linestyle=line_type[yticks_label[3]], linewidth=2.0)

            lns = [p1, p2, p3, p4, p5]
            host.legend(handles=lns, loc='lower left')
            # [matplot - legend - location value]
            # ---------------------------------
            # Location String | Location Code
            # ---------------------------------
            #   best                0
            #   upper right         1
            #   upper left          2
            #   lower left          3
            #   lower right         4
            #   right               5
            #   center left         6
            #   center right        7
            #   lower center        8
            #   upper center        9
            #   center             10
            # ---------------------------------
            # plt.grid('on')    # y축의 grid 만 나옴
            host.grid(True)     # x-y 축 grid 가 나옴.

            plt.title('Motor Characteristics')

            # right, left, top, bottom : 축의 위치 설정
            par1.spines['right'].set_position(('outward', 0))
            par2.spines['right'].set_position(('outward', 50))
            par3.spines['right'].set_position(('outward', 100))
            par4.spines['right'].set_position(('outward', 150))
            par5.spines['right'].set_position(('outward', 200))

            # no x-ticks
            # par2.xaxis.set_ticks([])

            # Sometimes handy, same for xaxis
            # par2.yaxis.set_ticks_position('right')

            # Move "Velocity"-axis to the left
            # par2.spines['left'].set_position(('outward', 60))
            # par2.spines['left'].set_visible(True)
            # par2.yaxis.set_label_position('left')
            # par2.yaxis.set_ticks_position('left')

            par1.yaxis.label.set_color(p1.get_color())
            par2.yaxis.label.set_color(p2.get_color())
            par3.yaxis.label.set_color(p3.get_color())
            par4.yaxis.label.set_color(p4.get_color())
            par5.yaxis.label.set_color(p5.get_color())

            # Adjust spacings w.r.t. figsize
            self.fig.tight_layout()
            # Alternatively: bbox_inches='tight' within the plt.savefig function
            #                (overwrites figsize)

            # Best for professional typesetting, e.g. LaTeX
            # plt.savefig("pyplot_multiple_y-axis.pdf")
            # For raster graphics use the dpi argument. E.g. '[...].png", dpi=200)'

            plt.show()
        else :
            print('file not selected!')
            QMessageBox.warning(self, '경고','계산할 파일을 선택하세요.')

    def checkCombo(self):
        # 공용으로 사용을 함. 동일한 클래스 내에서 self 변수는 공유함.
        # parameter X 에 대하여 콤보값 가져오기.
        if self.xAxisCombo.currentIndex() == 1:
            self.paraX = self.tq
            self.xLabel = 'torque [N$\cdot$m]'
        elif self.xAxisCombo.currentIndex() == 2:
            self.paraX = self.speed
            self.xLabel = 'speed [r/min]'
        elif self.xAxisCombo.currentIndex() == 3:
            self.paraX = self.Po
            self.xLabel = 'OutPower [W]'
        elif self.xAxisCombo.currentIndex() == 4:
            self.paraX = self.cur
            self.xLabel = 'Iph [A]'
        elif self.xAxisCombo.currentIndex() == 5:
            self.paraX = self.eff
            self.xLabel = 'efficiency [%]'
        elif self.xAxisCombo.currentIndex() == 6:
            self.paraX = self.effS
            self.xLabel = 'efficiency [%]'
        elif self.xAxisCombo.currentIndex() == 7:
            self.paraX = self.volt
            self.xLabel = 'voltage [V]'

            # parameter Y 에 대하여 콤보값 가져오기.
        if self.yAxisCombo.currentIndex() == 1:
            self.paraY = self.tq
            self.yLabel = 'torque [N$\cdot$m]'
        elif self.yAxisCombo.currentIndex() == 2:
            self.paraY = self.speed
            self.yLabel = 'speed [r/min]'
        elif self.yAxisCombo.currentIndex() == 3:
            self.paraY = self.Po
            self.yLabel = 'OutPower [W]'
        elif self.yAxisCombo.currentIndex() == 4:
            self.paraY = self.cur
            self.yLabel = 'Iph [A]'
        elif self.yAxisCombo.currentIndex() == 5:
            self.paraY = self.eff
            self.yLabel = 'efficiency [%]'
        elif self.yAxisCombo.currentIndex() == 6:
            self.paraY = self.effS
            self.yLabel = 'efficiency [%]'
        elif self.yAxisCombo.currentIndex() == 7:
            self.paraY = self.volt
            self.yLabel = 'voltage [V]'

        # parameter Z 에 대하여 콤보값 가져오기.
        if self.zAxisCombo.currentIndex() == 1:
            self.paraZ = self.tq
            self.zLabel = 'torque [N$\cdot$m]'
        elif self.zAxisCombo.currentIndex() == 2:
            self.paraZ = self.speed
            self.zLabel = 'speed [r/min]'
        elif self.zAxisCombo.currentIndex() == 3:
            self.paraZ = self.Po
            self.zLabel = 'OutPower [W]'
        elif self.zAxisCombo.currentIndex() == 4:
            self.paraZ = self.cur
            self.zLabel = 'Iph [A]'
        elif self.zAxisCombo.currentIndex() == 5:
            self.paraZ = self.eff
            self.zLabel = 'efficiency [%]'
        elif self.zAxisCombo.currentIndex() == 6:
            self.paraZ = self.effS
            self.zLabel = 'efficiency [%]'
        elif self.zAxisCombo.currentIndex() == 7:
            self.paraZ = self.volt
            self.zLabel = 'voltage [v]' 

    def loadFromFiles(self):
        #  === newData 함수에 대한 정의 ====
        # * 변수 : intpLoc, file_names, maxTorque, kType, numArray
        #   intpLoc : 인터폴레이션할 기준. 1은 토오크 위치임.
        #   file_names : 마우스로 선택된 파일들을 모아 놓음(튜플데이타)
        #   maxTorque : GUI에 있는 최대 토오크 값
        #   kType : 인터폴레이션 종류. 'cubic', 'linear', ...
        #   numArray : GUI에 있는 n x n 개수값.
        #
        newData = plotIO.intpArray(1, self.file_names, self.maxTorque.text(), \
            'cubic', self.numArray)
        datas = newData.calData()
        npData = np.array(datas)  # numpy 데이타로 변환 

        pathName = os.path.dirname(self.file_names[0][0])
        # Debug - 데이타 확인 ----------
        f = open(pathName+'/datas.csv', \
            'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        for data in datas :
            wr.writerow(data)
        f.close()
        # Debug - 저장 종료 ------------
                
        try :

            # array 개수는 신경쓰지 않음. list 로 변수를 선언하고 list 변수를 array로 바꿔주면 array 크기는 해결됨.
            # 저장할 변수들을 리스트 형식으로 선언함. 변수 초기화
            tqList = list()
            speedList = list()
            effList = list()
            voltList = list()
            curList = list()
            effSList = list()
            poList = list()

            ntqList = list()
            nspeedList = list()
            npoList = list()
            nvoltList = list()
            ncurList = list()
            neffList = list()
            neffSList = list()

            # 데이타를 분류 하여 저장을 함. 
            # 그래프를 종류별 데이타로 그리기 때문임.
            for row in range(0, len(self.file_names[0])):
                speedList.append(npData[14*row+0, :])    
                tqList.append(npData[   14*row+1, :])    # 2 - 11 - 20
                poList.append(npData[   14*row+2, :])   
                voltList.append(npData[ 14*row+3, :])   
                curList.append(npData[  14*row+6, :])    
                effList.append(npData[  14*row+11, :])    
                effSList.append(npData[ 14*row+12, :])    

            # Debug - 데이타 확인 ----------
            f = open(pathName+'/tqs.csv', \
                'w', encoding='utf-8', newline='')
            wr = csv.writer(f)
            for data in tqList :
                wr.writerow(data)
            f.close()
            # Debug - 저장 종료 ------------

            # 데이타가 완성이 되면 리스트 변수를 np array로 변경을 한다.
            speed = np.array(speedList)
            tq = np.array(tqList)
            po = np.array(poList)
            volt = np.array(voltList)
            cur = np.array(curList)
            eff = np.array(effList)
            effS = np.array(effSList)
            
            
            # 전압으로 데이타 정리 
            # max Voltage 이하 값으로 데이타 정리.
            divList = np.linspace(20, 2000, 100).astype(np.int)
            VoltPer = 0.0001
            newData = plotIO.intArrayLine(1, self.file_names, self.maxTorque.text(), \
                    'cubic', self.numArray, divList, VoltPer, \
                    speed, tq, po, volt, cur, eff, effS)
            
            find = 0

            for row in range(0, len(volt)):
                # print('column = ' + str(col))
                # print((volt[:, col]), (speed[:, col]))

                MaxTorque = max(tq[row, :])  # 각 행에서 최대 토오크 값을 찾음
                MinTorque = min(tq[row, :])  # 각 행에서 최소 토오크 값을 찾음

                if max(volt[row, :]) > float(self.maxVoltage.text()) : # 각 행에서 최전압의 값이 제한전압보다 크면 실행.
                    for div in divList :
                        # print('div = {0:d} minTq = {1:.2f} maxTq = {2:.2f}'.format(div, MinTorque, MaxTorque))
                        # print(tq[col, :], volt[col, :])

                        TSet = np.linspace(MinTorque, MaxTorque, div )
                        fVolt = interpolate.interp1d(tq[row, :], volt[row, :], kind='linear')
                        yVolt = fVolt(TSet)
                        for j in range(0, len(yVolt)-1) :
                            if (yVolt[j] > float(self.maxVoltage.text())*(1-VoltPer) and (yVolt[j] < float(self.maxVoltage.text())*(1+VoltPer) )):
                                find = True
                                # Check Value
                                self.textBrowser.append('j={0:4d} / TSet = {1:.2f} / yVolt = {2:.2f} '.format(j, TSet[j], yVolt[j]))
                                print('j={0:4d} TSet = {1:.2f} yVolt = {2:.2f} '.format(j, TSet[j], yVolt[j]))
                                break
                            else :
                                find = False
                        if find == True :
                            break
                    TorqueSet = np.linspace(tq[row, 0], TSet[j], num=self.numArray, endpoint=True)
                else :
                    TorqueSet = np.linspace(tq[row, 0], MaxTorque, num=self.numArray, endpoint=True)

                # print('row = {}'.format(row))

                # 격자를 나누는 기준으로 전압으로 합니다.
                # ‘linear’, ‘nearest’, ‘nearest-up’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, or ‘next’. ‘zero’, ‘slinear’, ‘quadratic’
                fftq =   interpolate.interp1d(tq[row, :], tq[row, :], kind='linear')
                ffPo =   interpolate.interp1d(tq[row, :], po[row, :], kind='linear')
                ffVolt = interpolate.interp1d(tq[row, :], volt[row, :], kind='linear')
                ffCur =  interpolate.interp1d(tq[row, :], cur[row, :], kind='linear')
                ffEff =  interpolate.interp1d(tq[row, :], eff[row, :], kind='linear')
                ffEffS = interpolate.interp1d(tq[row, :], effS[row, :], kind='linear')
                ffSpd =  interpolate.interp1d(tq[row, :], speed[row, :], kind='linear')

                yytq = fftq(TorqueSet)
                yySpeed = ffSpd(TorqueSet)
                yyVolt = ffVolt(TorqueSet)
                yyCur = ffCur(TorqueSet)
                yyEff = ffEff(TorqueSet)
                yyEffS = ffEffS(TorqueSet)
                yyPo = ffPo(TorqueSet)

                # 초기화 시킨 리스트 변수에 데이타를 쌓아 놓는다.
                # np.array 를 사용을 하면 마지막에 한줄이 더 발생을 함. 이유는 모르겠음.
                nspeedList.append(yySpeed)
                ntqList.append(yytq)
                npoList.append(yyPo)
                nvoltList.append(yyVolt)
                ncurList.append(yyCur)
                neffList.append(yyEff)
                neffSList.append(yyEffS)

            # 데이타가 완성이 되면 리스트 변수를 np array로 변경을 한다.
            nspeed = np.array(nspeedList)
            ntq = np.array(ntqList)
            npo = np.array(npoList)
            nvolt = np.array(nvoltList)
            ncur = np.array(ncurList)
            neff = np.array(neffList)
            neffS = np.array(neffSList)


            # list 변수 초기화하여 다시쓰기.
            tqList = list()
            speedList = list()
            effList = list()
            voltList = list()
            curList = list()
            effSList = list()
            poList = list()

            # print(nspeed.size)   # numpy array size 확인
            # print(ntq.size)      # numpy array size 확인

            # 속도에 대해서 데이타 정리.
            for col in range(0, self.numArray):
                spdDiv = np.linspace(nspeed[0, col], speed[len(nspeed) - 1, col], num=self.numArray, endpoint=True)
                # print('{0:d} {1:.2f} {2:.2f}'.format(i, nspeed[0, i], nspeed[len(nspeed)-1, i]))
                # 격자를 나누는 기준으로 속도로 하며, 준비를 하였습니다.
                # print(spdDiv)

                # ===================================================================================================
                # 오류 문제에 대한 해결.
                #
                # ValueError: A value in x_new is above the interpolation range.
                #
                # 정답은 아니지만 아래의 자료를 찾아서 해결을 함. 하지만 데이타가 이상할 수 있다는...
                # https://pythonq.com/so/python/367426

                fffnSpd = interpolate.interp1d(nspeed[:, col], nspeed[:, col], fill_value="extrapolate")
                fffntq = interpolate.interp1d(nspeed[:, col], ntq[:, col], fill_value="extrapolate")
                fffnPo = interpolate.interp1d(nspeed[:, col], npo[:, col], fill_value="extrapolate")
                fffnVolt = interpolate.interp1d(nspeed[:, col], nvolt[:, col], fill_value="extrapolate")
                fffnCur = interpolate.interp1d(nspeed[:, col], ncur[:, col], fill_value="extrapolate")
                fffnEff = interpolate.interp1d(nspeed[:, col], neff[:, col], fill_value="extrapolate")
                fffnEffS = interpolate.interp1d(nspeed[:, col], neffS[:, col], fill_value="extrapolate")
                # ===================================================================================================

                # function을 이용하여 결과값을 계산을 함.
                yyySpd = fffnSpd(spdDiv)
                yyyTq = fffntq(spdDiv)
                yyyVolt = fffnVolt(spdDiv)
                yyyCur = fffnCur(spdDiv)
                yyyEff = fffnEff(spdDiv)
                yyyEffS = fffnEffS(spdDiv)
                yyyPo = fffnPo(spdDiv)

                # 초기화 시킨 리스트 변수에 데이타를 쌓아 놓는다.
                # np.array 를 사용을 하면 마지막에 한줄이 더 발생을 함. 이유는 모르겠음.
                speedList.append(yyySpd)
                tqList.append(yyyTq)
                poList.append(yyyPo)
                voltList.append(yyyVolt)
                curList.append(yyyCur)
                effList.append(yyyEff)
                effSList.append(yyyEffS)

            # 데이타가 완성이 되면 리스트 변수를 np array로 변경을 한다.
            self.speed = np.array(speedList)
            self.tq = np.array(tqList)
            self.po = np.array(poList)
            self.volt = np.array(voltList)
            self.cur = np.array(curList)
            self.eff = np.array(effList)
            self.effS = np.array(effSList)

            # Debug - 데이타 확인 ----------
            f = open('speed.csv', 'w', encoding='utf-8', newline='')
            wr = csv.writer(f)
            for data in self.speed:
                wr.writerow(data)
            f.close()
            # Debug - 저장 종료 ------------
            # Debug - 데이타 확인 ----------
            f = open('tq.csv', 'w', encoding='utf-8', newline='')
            wr = csv.writer(f)
            for data in self.tq:
                wr.writerow(data)
            f.close()
            # Debug - 저장 종료 ------------
            # Debug - 데이타 확인 ----------
            f = open('volt.csv', 'w', encoding='utf-8', newline='')
            wr = csv.writer(f)
            for data in self.volt:
                wr.writerow(data)
            f.close()
            # Debug - 저장 종료 ------------

            self.textBrowser.append('=== 데이타를 모두 불러왔습니다. ====')
            # print('데이타를 모두 불러왔습니다.')
            #
            #
            # print(self.speed)
            # print(tq)
            # print(tq)
            # print('=======================================')
            # print(Vtq)
            # print('=======================================')
            # print(self.tq)
            # print('=======================================')

            self.dataLogic = True
        except IndexError as e:
            QMessageBox.warning(self, '경고',e)

    def openDialog(self):
        print(">>> openDialog")
        try:
            self.file_names = QFileDialog.getOpenFileNames(self, 'Open file', self.readPathInfo.text(),
                                                           "Speed files (*.txt)")
            if self.file_names[0]:
                self.dataLogic = True
                for file in self.file_names[0]:
                    self.textBrowser.append(file)
                self.textBrowser.append(str(len(self.file_names[0])) + ' 개의 파일을 선택하였습니다.')
            else :
                # print('file not selected!')
                QMessageBox.warning(self, '경고','파일을 선택하지 않았습니다.')
            # 파일 데이타를 불러옴. 1번만 불러서 계속 사용함.

            # loadData = plotIO.intpArray(1, self.file_names)
            # aaa = loadData.calData()

            # 파일 이름이 정상적으로 되어 있는지 확인을 함.s
            for name in self.file_names[0]:
                fname = os.path.basename(name)  # 파일 이름만 추출함.
                if (('rpm' in fname) == False):  # https://ponyozzang.tistory.com/532 파일이름 안에 'rpm'이 있는 경우
                    self.fileNameSign = False  # 입력된 min-max 값이 모두 숫자인지 판별 sign.
                    QMessageBox.warning(self, '경고', '선택한 파일이 형식 맞지 않습니다. \n '
                                                    '숫자 + rpm.txt. 이어야 합니다.')
                    break
                else :
                    self.fileNameSign = True  # 입력된 min-max 값이 모두 숫자인지 판별 sign.

            # 파일이 정상적으로 되었다면 실행을 한다.
            if self.fileNameSign :
                for name in self.file_names[0]:
                    fname = os.path.basename(name)
                    spdChar, tr = fname.split('r')
                    if spdChar.isdigit() :
                        self.fileNameSign = True
                    else :
                        QMessageBox.warning(self, '경고','선택한 파일({})이 형식 맞지 않습니다. \n '
                                                  '숫자 + rpm.txt. 이어야 합니다.'.format(name))

                self.loadFromFiles() # 모든게 정상적이면 데이타를 불러 옵니다.
        except FileNotFoundError as e:
            QMessageBox.warning(self, '경고',  e)

    def openMdfDialog(self):
        #
        # how to make getOpenFileName remember last opening path?
        # https://stackoom.com/en/question/1YW4v
        #
        # filename = QtGui.QFileDialog.getOpenFileName(
        #     parent, 'Open File', '', 'Images (*.png *.xpm *.jpg)',
        #     None, QtGui.QFileDialog.DontUseNativeDialog)
        #
        # dialog = QtGui.QFileDialog(parent)
        # dialog.setWindowTitle('Open File')
        # dialog.setNameFilter('Images (*.png *.xpm *.jpg)')
        # dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        # if dialog.exec_() == QtGui.QDialog.Accepted:
        #     filename = dialog.selectedFiles()[0]

        self.mdf_names = QFileDialog.getOpenFileNames(self, 'Open file', self.readPathInfo.text(),
                                                       "Magtrol File (*.mdf)")

        if self.mdf_names[0]: # 파일이 정상적으로 불러왔을 경우,
            self.dataLogic = True
            for file in self.mdf_names[0]:
                self.textBrowser.append(file)
            self.textBrowser.append(str(len(self.mdf_names[0])) + ' 개의 파일을 선택하였습니다.')
            for name in self.mdf_names[0]:
                fname = os.path.basename(name)
                spdChar, tr = fname.split('r')  # 속도 값만을 분리해 냄.
                if spdChar.isdigit():
                    self.fileNameSign = True
                    self.read_MDFtoTXT(name)  # txt 파일을 만드는 작업을 진행을 함.
                else:
                    QMessageBox.warning(self, '경고', '선택한 파일({})이 형식 맞지 않습니다. \n '
                                                    '숫자 + rpm.txt. 이어야 합니다.'.format(name))
        else:
            # print('file not selected!')
            QMessageBox.warning(self, '경고', '파일을 선택하지 않았습니다.')
        # 파일 데이타를 불러옴. 1번만 불러서 계속 사용함.

    def read_MDFtoTXT(self, fileName):

        # numpy array로 데이타 읽기
        # 다이나모 데이타에서 curve 로 측정을 하면 1줄은 '주석', 2 ~ 3줄은 NaN 이 있으므로
        # header 는 3으로 하여 데이타를 넘어가도록 한다.
        # 읽는 데이타 타입은 실수형으로 한다.
        # my_data = np.genfromtxt(fileName, delimiter='\t', skip_header=3, dtype='float')
        self.saveSignal = False
        my_data = self.fileToArray(fileName)

        """
        0. 속도값에서 기준이 되는 속도를 찾음. 가장 많은 속도값이 있는 것부터... 찾음.
           측정값이 일정한 속도로 측정은 하지만, 가끔은 그 기준이 많이 틀려질 것임.
        1. 속도값은 파일이름과 연관이 되어 있으므로 데이타의 오차범위를 +/- 3 rpm 에서 데이타만 rpm 별로 리스트에 저장을 한다.
          오차범위에 해당하는 데이타가 없으면 ---> "데이타를 다시 측정해주세요" 날리고 종료.
        2. 각 리스트의 데이타수(행의 개수)를 비교하여 가장 많은 것, 두번째 많은 것에서 토오크를  판별을 한다.
        """

        spdCheckList0 = list()
        spdCheckList1 = list()
        spdCheckList2 = list()
        spdCheckList3 = list()
        spdCheckList4 = list()
        spdCheckList5 = list()
        spdCheckList6 = list()
        spdCheckList7 = list()
        spdCheckList8 = list()
        spdCheckList9 = list()

        # print(max(my_data[:, 1]))
        # print(my_data[0, 1])
        #
        # avgSpd : 중간치 속도값을 데이타에서 판별을 함.
        #
        avgSpd = int(sum(my_data[:, 1]) / len(my_data))
        print("Aerage Speed = " + str(avgSpd))

        for row in range(0, len(my_data)):
            if ((avgSpd+4) % my_data[row, 1]) <= 0:
                spdCheckList0.append(my_data[row, 1])
            elif ((avgSpd+3) % my_data[row, 1]) <= 0:
                spdCheckList1.append(my_data[row, 1])
            elif ((avgSpd+2) % my_data[row, 1]) <= 0:
                spdCheckList2.append(my_data[row, 1])
            elif ((avgSpd+1) % my_data[row, 1]) <= 0:
                spdCheckList3.append(my_data[row, 1])
            elif (avgSpd % my_data[row, 1]) <= 0:
                spdCheckList4.append(my_data[row, 1])
            elif ((avgSpd-1) % my_data[row, 1]) <= 0:
                spdCheckList5.append(my_data[row, 1])
            elif ((avgSpd-2) % my_data[row, 1]) <= 0:
                spdCheckList6.append(my_data[row, 1])
            elif ((avgSpd-3) % my_data[row, 1]) <= 0:
                spdCheckList7.append(my_data[row, 1])
            elif ((avgSpd-4) % my_data[row, 1]) <= 0:
                spdCheckList8.append(my_data[row, 1])
            elif ((avgSpd-5) % my_data[row, 1]) <= 0:
                spdCheckList9.append(my_data[row, 1])

        listSpdNo = list()
        listSpdLable = [spdCheckList0, spdCheckList1, spdCheckList2, spdCheckList3, spdCheckList4, spdCheckList5,
                        spdCheckList6, spdCheckList7, spdCheckList8, spdCheckList9]
        # print((listSpdLable))

        for row in listSpdLable:
            listSpdNo.append(len(row))

        speedIndex = listSpdNo.index(max(listSpdNo))  # 가장 많은 인덱스를 저장
        speed = listSpdLable[speedIndex][0]   # 가장 많은 인덱스의 속도값을 speed 로 사용을 함.


        spdCase1 = float(speed -3)
        spdCase2 = float(speed -2)
        spdCase3 = float(speed -1)
        spdCase4 = float(speed -0)
        spdCase5 = float(speed +1)
        spdCase6 = float(speed +2)
        spdCase7 = float(speed +3)

        spdList1 = list()
        spdList2 = list()
        spdList3 = list()
        spdList4 = list()
        spdList5 = list()
        spdList6 = list()
        spdList7 = list()
        spdRest = list()

        spdRate = 1.001
        for row in range(0, len(my_data)):
            if (my_data[row, 1] / spdCase1) < spdRate:
                spdList1.append(my_data[row, :])
            elif (my_data[row, 1] / spdCase2) < spdRate:
                spdList2.append(my_data[row, :])
            elif (my_data[row, 1] / spdCase3) < spdRate:
                spdList3.append(my_data[row, :])
            elif (my_data[row, 1] / spdCase4) < spdRate:
                spdList4.append(my_data[row, :])
            elif (my_data[row, 1] / spdCase5) < spdRate:
                spdList5.append(my_data[row, :])
            elif (my_data[row, 1] / spdCase6) < spdRate:
                spdList6.append(my_data[row, :])
            elif (my_data[row, 1] / spdCase7) < spdRate:
                spdList7.append(my_data[row, :])
            else :
                spdRest.append(my_data[row, :])

        listNo = list()
        listLable = [spdList1, spdList2, spdList3, spdList4, spdList5, spdList6, spdList7]
        for row in listLable:
            listNo.append(len(row))

        # print(listNo) # list 값을 확인함
        idx1 = listNo.index(max(listNo))  # 가장 많은 인덱스를 저장
        listNo[idx1] = 0  # 저장을 했으니 0을 넣어서 리스트값 변경
        idx2 = listNo.index(max(listNo)) # 두번쨰 가장 많은 인덱스를 저장

        # print(idx1, idx2)

        # print(listLable[idx1])
        first = np.array(listLable[idx1])  # 가장많은 데이타를 np.array 로 변환
        second = np.array(listLable[idx2])  # 두번째 많은 데이타를 np.array 로 변환

        listFirst = list()
        for row in range(0, len(first)-1) :
            # print('{0:0.2f}'.format(first[row+1, 2]/first[row, 2]))
            if (first[row+1, 2]/first[row, 2]) > 1.12 :
                listFirst.append(first[row, 1:])

        listSecond = list()
        for row in range(0, len(second)-1) :
            # print('{0:0.2f}'.format(second[row+1, 2]/second[row, 2]))
            if (second[row+1, 2]/second[row, 2]) > 1.12 :
                listSecond.append(second[row, 1:])

        # 데이타 검색/분류가 잘못되면 데이타가 안나옴. 수동 모드로 변환을 해야 함.
        # https://jobc.tistory.com/145
        #
        # 일단 모두 수동 모드로 바꿔 사용함. 2022-01-28
        if not listFirst :
            self.checkReadedDataManual(fileName, my_data)  # 가장 많은 속도 값으로 분류된 리스트
            # print("Top")
        else :
            self.checkReadedDataManual(fileName, my_data)  # 가장 많은 속도 값으로 분류된 리스트
            # self.checkReadedData(fileName, listFirst)  # 파일 이름과 list 를 넘겨서 창을 만들어 줌.
            # print("Bottom")

        if self.saveSignal == True:
            self.saveTextFile(fileName, listFirst)

    def checkReadedDataManual(self, name, my_data):
        #
        #  sub class로 데이타 전달하는 방법 ..? 아래 싸이트에서 .... 공부 좀 합시다.
        #  https://mystyle1057.tistory.com/entry/Python-%ED%81%B4%EB%9E%98%EC%8A%A4%ED%81%B4%EB%9E%98%EC%8A%A4-%EB%B3%80%EC%88%98
        #
        dialog = DialogWIndow.subWindow(name, my_data)
        dialog.exec_()

    def checkReadedData(self, name, listValue):
        self.dialog = QDialog(self)
        self.dialog.resize(1600, 600)
        self.dialog.move(20, 70)
        # self.dialog.setFixedSize(self.width, self.height)
        self.dialog.setWindowTitle(name + " --> .txt Converted Window")
        # --------
        self.signOK = QPushButton(self.dialog)
        self.signOK.setGeometry(QtCore.QRect(50, 550, 75, 23))
        self.signOK.setObjectName("OK Button")
        self.signOK.setText("ACCEPT")
        self.signOK.clicked.connect(self.saveFile)
        # --------
        self.signNO = QPushButton(self.dialog)
        self.signNO.setGeometry(QtCore.QRect(150, 550, 75, 23))
        self.signNO.setObjectName("NO Button")
        self.signNO.setText("PASS/CLOSE")
        self.signNO.clicked.connect(self.closeEvent)
        #
        # https://wikidocs.net/5240  QTableWidget 만들기.
        #
        tableWidget = QtWidgets.QTableWidget(self.dialog)
        tableWidget.setGeometry(QtCore.QRect(10, 10, 1550, 500))
        tableWidget.setRowCount(len(listValue))
        tableWidget.setColumnCount(len(listValue[0]))

        print(listValue)
        for row in range(0, len(listValue)) :
            for col in range(0, len(listValue[0])) :
                tableWidget.setItem(row, col, QTableWidgetItem(str(listValue[row][col])))

        # print(listValue[0][0])
        # print(type(listValue))

        self.dialog.exec()  # 읽어들인 데이타를 판별하는 창을 열어줌

    def saveFile(self):
        self.saveSignal = True
        self.dialog.close()

    def saveFileOnly(self):
        self.saveSignal = True

    def closeEvent(self, event):
        self.saveSignal = False
        # self.dialog.close()

    def saveSignalFalse(self):
        self.saveSignal = False

    def saveTextFile(self, fileName, listData):
        pathName = os.path.dirname(fileName)
        fname = os.path.basename(fileName)  # 파일 이름만 추출함.
        speed, tr = fname.split('r')

        # Debug - 데이타 확인 ----------
        f = open(pathName + '/' + str(int(speed)) + 'rpm.txt', 'w', encoding='utf-8', newline='')
        print(pathName + '/' + str(int(speed)) + 'rpm.txt')
        wr = csv.writer(f, delimiter='\t')
        for line in listData:
            wr.writerow(line)
        # for line in listSecond:
        #     wr.writerow(line)
        f.close()
        # Debug - 저장 종료 ------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = startGraph()

    window.show()

    # 시방변경 불러오기/신규/수정/삭제
    # orderWindow.oW = orderWindow()
    # orderWindow.oW.show()

    # 사용자 자료 불러오기/신규/수정/삭제
    # usersManage.uM = usersManage()
    # usersManage.uM.show()

    sys.exit(app.exec_())

