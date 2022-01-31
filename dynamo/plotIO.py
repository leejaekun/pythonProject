"""
  plotMotorChar_2.py 에 종속된 프로그램
  서브 윈도우에서 그래프를 그리고, 데이타를 추출하는 부분임.

"""
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os.path
import numpy as np
from scipy import interpolate 

#
# 디버깅 시험용 임.
#
class ThailandPackage:
  def detail(self):
    print("방콕 파타야 여행. 50만원")
 
#
# 행렬을 계산하는 부분을 따로 뺴서 프로그램을 간소화.
# 인터폴레이션을 묶어서 서브 함수 콜을 간소화.
#
class intpArray:
  def __init__(self, intpLoc, file_names, maxTorque, kType, numArray):
    self.intpLoc = intpLoc  # 인터폴레이션 인덱스 번호 
    self.file_names = file_names # 파일이름 LIST 변수 
    self.maxTorque = maxTorque
    self.kType = kType
    self.numArray = numArray

  def calData(self):
    # print(self.intpLoc, self.file_names ) # for debug

    # array 개수는 신경쓰지 않음. list 로 변수를 선언하고 list 변수를 array로 바꿔주면 array 크기는 해결됨.
    # 저장할 변수들을 리스트 형식으로 선언함. 변수 초기화
    nData = list()

    # torque에 대해서 데이타 정리.
    for name in self.file_names[0]:

      fname = os.path.basename(name)
      spdChar, tr = fname.split('r')
      spdName = float(spdChar)

      try:
          # https://pythonq.com/so/python/249681 genfromtxt
          # print('>>>> ' + name)
          data = np.genfromtxt(name,  dtype='float')

      except OSError as e:
          QMessageBox.warning(self, 'intpArray() 경고', e)

      # data = np.genfromtxt('./' + str(name) + 'rpm.txt', dtype='float')
      # 1개 루프에서 속도 1개의 파일을 한번에 읽어옵니다.
      if data[len(data) - 1, 1] > float(self.maxTorque):
          tqDiv = np.linspace(data[0, 1], float(float(self.maxTorque)), \
            num=self.numArray, endpoint=True)
      else:
          tqDiv = np.linspace(data[0, 1], data[len(data) - 1, 1], \
            num=self.numArray, endpoint=True)

      # print(self.kType)
      # print(type(self.kType))
      # for col in range(0, len(data)):
        # nData.append(self.interpolateReturn(data[:, 1], data[:, col], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 0], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 1], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 2], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 3], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 4], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 5], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 6], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 7], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 8], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 9], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 10], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 11], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 12], tqDiv, self.kType))
      nData.append(self.interpolateReturn(data[:, 1], data[:, 13], tqDiv, self.kType))

  
    return nData

  def interpolateReturn(self, initX, initY, resX, type):
    function = interpolate.interp1d(initX, initY, kind=type)
    value = function(resX)
    return value

class intArrayLine(intpArray):
  def __init__(self, intpLoc, file_names, maxTorque, kType, numArray, \
            divList, VoltPer, speed, tq, po, volt, cur, eff, effS):
    intpArray.__init__(self, intpLoc, file_names, maxTorque, kType, numArray)
    self.divList = divList
    self.VoltPer = VoltPer
    self.speed = speed
    self.tq = tq
    self.po = po
    self.volt = volt
    self.cur = cur
    self.eff = eff
    self.effS = effS
  
  def calData(self):

    for row in range(0, len(self.volt)):
      # print('column = ' + str(col))
      # print((volt[:, col]), (speed[:, col]))

      MaxTorque = max(self.tq[row, :])  # 각 행에서 최대 토오크 값을 찾음
      MinTorque = min(self.tq[row, :])  # 각 행에서 최소 토오크 값을 찾음

      if max(self.volt[row, :]) > float(self.maxVoltage.text()) : # 각 행에서 최전압의 값이 제한전압보다 크면 실행.
          for div in self.divList :
              # print('div = {0:d} minTq = {1:.2f} maxTq = {2:.2f}'.format(div, MinTorque, MaxTorque))
              # print(tq[col, :], volt[col, :])

              TSet = np.linspace(MinTorque, MaxTorque, div )
              fVolt = interpolate.interp1d(self.tq[row, :], self.volt[row, :], \
                kind='linear')
              yVolt = fVolt(TSet)
              for j in range(0, len(yVolt)-1) :
                  if (yVolt[j] > float(self.maxVoltage.text())*(1-self.self.VoltPer) \
                    and (yVolt[j] < float(self.maxVoltage.text())*(1+self.VoltPer) )):
                      find = True
                      # Check Value
                      self.textBrowser.append('j={0:4d} / TSet = {1:.2f} / \
                        yVolt = {2:.2f} '.format(j, TSet[j], yVolt[j]))
                      print('j={0:4d} TSet = {1:.2f} yVolt = {2:.2f} '.\
                        format(j, TSet[j], yVolt[j]))
                      break
                  else :
                      find = False
              if find == True :
                  break
          TorqueSet = np.linspace(self.tq[row, 0], TSet[j], num=self.numArray, \
            endpoint=True)
      else :
          TorqueSet = np.linspace(self.tq[row, 0], MaxTorque, num=self.numArray, \
            endpoint=True)

      # print('row = {}'.format(row))

      # 격자를 나누는 기준으로 전압으로 합니다.
      # ‘linear’, ‘nearest’, ‘nearest-up’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, or ‘next’. ‘zero’, ‘slinear’, ‘quadratic’
      fftq =   interpolate.interp1d(self.tq[row, :], self.tq[row, :], kind='linear')
      ffPo =   interpolate.interp1d(self.tq[row, :], self.po[row, :], kind='linear')
      ffVolt = interpolate.interp1d(self.tq[row, :], self.volt[row, :], kind='linear')
      ffCur =  interpolate.interp1d(self.tq[row, :], self.cur[row, :], kind='linear')
      ffEff =  interpolate.interp1d(self.tq[row, :], self.eff[row, :], kind='linear')
      ffEffS = interpolate.interp1d(self.tq[row, :], self.effS[row, :], kind='linear')
      ffSpd =  interpolate.interp1d(self.tq[row, :], self.speed[row, :], kind='linear')

      yytq = fftq(TorqueSet)
      yySpeed = ffSpd(TorqueSet)
      yyVolt = ffVolt(TorqueSet)
      yyCur = ffCur(TorqueSet)
      yyEff = ffEff(TorqueSet)
      yyEffS = ffEffS(TorqueSet)
      yyPo = ffPo(TorqueSet)
      
      return 