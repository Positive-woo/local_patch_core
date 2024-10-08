import sys
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from gui import Ui_MainWindow


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Ui_MainWindow 설정
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 타이머와 카메라 초기화
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.cap = cv2.VideoCapture(0)  # 0번 카메라 사용
        self.current_frame = None  # 현재 프레임 저장할 변수

        # 타이머 시작 (30ms마다 프레임 업데이트)
        self.timer.start(30)

        # Ui에 정의된 캡처 버튼과 캡처 기능 연결
        self.ui.pushButton.clicked.connect(self.ui.capture)

        self.show()

    def update_frame(self):
        # 카메라에서 프레임을 읽고 QLabel에 표시
        ret, frame = self.cap.read()
        if ret:
            self.ui.current_frame = frame.copy()  # 현재 프레임을 저장

            height, width, _ = frame.shape
            color = (0, 0, 255)
            thickness = 2

            # 프레임에 수직 및 수평 보조선 그리기
            cv2.line(frame, (width // 4, 0), (width // 4, height), color, thickness)
            cv2.line(
                frame, (0, height * 3 // 4), (width, height * 3 // 4), color, thickness
            )

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(
                rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888
            )
            self.ui.widget.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        # 윈도우 종료 시 카메라 릴리스
        if self.cap.isOpened():
            self.cap.release()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec_())
