"""
  plotMotorChar_2.py 에 종속된 프로그램
  서브 윈도우에서 그래프를 그리고, 데이타를 추출하는 부분임.

"""
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import plotMotorChar_2

class plotIO:
    def openPath(self):
        FileFolder = QFileDialog.getExistingDirectory(self, 'Find Folder')

        if not FileFolder :
            buttonReply = QMessageBox.information(self, '작업 폴더 선택', "폴더를 선택하지 않았습니다.",
                                                  QMessageBox.Ok)
        else :
            buttonReply = QMessageBox.information(self, '작업 폴더 선택', FileFolder + "가 선택되었습니다.",

                                                  QMessageBox.Ok)
            # plotMain = plotMotorChar_2()  # 이것을 왜 사용을 했는지 모르겠음.

            self.readPathInfo.setText(FileFolder)

            # 표준위치에 경로 저장
            f = open('./folderHistory.ini', 'w', encoding='utf-8', newline='')
            f.write(self.readPathInfo.text())
            f.close()