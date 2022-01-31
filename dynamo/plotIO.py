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
