import sys
from gui import Ui_MainWindow  # 수정 부분
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import cv2
from PyQt5.QtGui import QImage, QPixmap
import time


class kinwriter(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(30)  # 30ms마다 프레임 업데이트 (카메라용)
        self.timer.timeout.connect(self.update_frame)

        # 카메라 초기화
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("카메라를 열 수 없습니다.")
            return

        self.current_frame = None  # 현재 프레임을 저장할 변수

        self.pushButton.clicked.connect(self.capture)  # 캡처 버튼과 연결

        self.timer.start()  # 타이머 시작 (카메라 업데이트)

        self.show()

    def update_frame(self):
        # 카메라에서 프레임을 읽어와서 QLabel에 표시
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame  # 현재 프레임을 저장
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(
                rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888
            )
            self.widget.setPixmap(QPixmap.fromImage(qt_image))

    # def capture(self):
    #     # 콤보 박스에서 텍스트를 가져와 파일명에 포함
    #     text1 = self.comboBox.currentText()
    #     text2 = self.comboBox_2.currentText()

    #     if self.current_frame is not None:
    #         if not text1 or not text2:
    #             QMessageBox.warning(self, "Warning", "모형 이름과 위치를 입력하세요.")
    #             return

    #         # 현재 시간을 기반으로 파일명 생성
    #         timestamp = time.strftime("%Y%m%d_%H%M%S")
    #         filename = f"./capture_{text1}_{text2}_{timestamp}.png"

    #         # 현재 프레임 저장
    #         cv2.imwrite(filename, self.current_frame)
    #         QMessageBox.information(self, "Saved", f"이미지를 저장했습니다: {filename}")
    #     else:
    #         QMessageBox.warning(self, "Warning", "저장할 프레임이 없습니다.")

    def closeEvent(self, event):
        # 윈도우 종료 시 카메라 릴리스
        if self.cap.isOpened():
            self.cap.release()
        event.accept()


app = QApplication([])
sn = kinwriter()
QApplication.processEvents()
sys.exit(app.exec_())
