import cv2
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 590, 350))
        self.graphicsView.setObjectName("graphicsView")

        # 'widget'을 QLabel로 변경하여 카메라 프레임을 표시할 공간으로 사용
        self.widget = QtWidgets.QLabel(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(600, 10, 590, 350))
        self.widget.setObjectName("widget")
        self.widget.setScaledContents(True)  # 이미지 크기에 맞게 자동으로 조정

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 380, 311, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 410, 311, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.setEditable(True)  # Allow editing

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1100, 360, 91, 91))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 380, 71, 21))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 410, 71, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.capture)  # Connect capture function
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 타이머와 카메라 초기화 - 프로그램 시작 시 바로 카메라 시작
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = cv2.VideoCapture(0)  # 0번 카메라 사용
        self.timer.start(30)  # 30ms마다 프레임 업데이트

    # def update_frame(self):
    #     ret, frame = self.cap.read()
    #     if ret:
    #         self.current_frame = frame.copy()  # Store current frame
    #         # 프레임을 RGB로 변환
    #         rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         # OpenCV의 이미지를 PyQt에서 사용 가능한 QImage로 변환
    #         h, w, ch = rgb_image.shape
    #         bytes_per_line = ch * w
    #         convert_to_Qt_format = QImage(
    #             rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888
    #         )
    #         # QPixmap으로 변환 후 QLabel에 설정 (widget 부분에 프레임 표시)
    #         self.widget.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

    def capture(self):
        # 타이머 멈춤
        self.timer.stop()

        # 콤보 박스에서 텍스트를 가져와 파일명에 포함
        text1 = self.comboBox.currentText()
        text2 = self.comboBox_2.currentText()

        if self.current_frame is not None:
            if not text1 or not text2:
                QMessageBox.warning(self, "Warning", "모형 이름과 위치를 입력하세요.")
                self.timer.start()  # 타이머 재시작
                return

            # 현재 시간을 기반으로 파일명 생성
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"./capture_{text1}_{text2}_{timestamp}.png"

            # 현재 프레임 저장
            cv2.imwrite(filename, self.current_frame)
            QMessageBox.information(self, "Saved", f"이미지를 저장했습니다: {filename}")
        else:
            QMessageBox.warning(self, "Warning", "저장할 프레임이 없습니다.")

        # 타이머 재시작
        self.timer.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Camera Capture"))
        self.pushButton.setText(_translate("MainWindow", "SHOT"))
        self.label.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:11pt; font-weight:600;">모형 이름</span></p></body></html>',
            )
        )
        self.label_2.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:10pt; font-weight:600;">위치</span></p></body></html>',
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
