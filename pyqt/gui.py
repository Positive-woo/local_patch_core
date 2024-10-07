import time
from PyQt5 import QtCore, QtWidgets
import cv2
from dotenv import load_dotenv
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog

import os

load_dotenv()
source_folder = os.getenv("SOURCE_FOLDER")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 560)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 정상 이미지 출력 layout (QLabel로 변경)
        self.widget = QtWidgets.QLabel(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(600, 10, 590, 370))
        self.widget.setObjectName("widget")
        self.widget.setScaledContents(True)  # 이미지 크기에 맞게 자동으로 조정

        # 현재 캠 출력 layout
        self.widget = QtWidgets.QLabel(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 590, 370))
        self.widget.setObjectName("cam_view")
        self.widget.setScaledContents(True)  # 이미지 크기에 맞게 자동으로 조정

        # 모양 콤보박스
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 440, 311, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("shape_cb")
        self.additem_combobox_1(self.comboBox)

        # 모양 라벨
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 440, 71, 21))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("shape")

        # 위치 콤보박스
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 470, 311, 22))
        self.comboBox_2.setEditable(True)
        self.comboBox.setCurrentText("")
        self.comboBox_2.setObjectName("position_cb")

        # 모양 콤보박스 선택이 변경될 때 위치 콤보박스 업데이트
        self.comboBox.currentIndexChanged.connect(self.update_position_combobox)

        # 위치 라벨
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 470, 71, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("position")

        # 캡쳐 버튼
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1100, 420, 91, 91))
        self.pushButton.setObjectName("cam_capture")

        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setGeometry(QtCore.QRect(90, 500, 311, 22))
        self.browse_button.setText("파일 브라우저로 이미지 선택")
        self.browse_button.clicked.connect(self.browse_image)  # 파일 브라우저 기능 연결

        # etc
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def browse_image(self):
        # 파일 선택 다이얼로그 열기
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "이미지 선택", "", "Image Files (*.png *.jpg *.bmp)"
        )

        if file_path:
            self.load_image_from_path(file_path)

    # def load_image_from_path(self, image_path):
    #     if not os.path.exists(image_path):
    #         QtWidgets.QMessageBox.warning(
    #             None, "Error", "파일 경로가 올바르지 않습니다."
    #         )
    #         return
    #     # QLabel에 이미지 로드 및 설정
    #     self.display_captured_image(image_path)

    # def display_captured_image(self, filepath):
    #     pixmap = QPixmap(filepath)
    #     if pixmap.isNull():
    #         QtWidgets.QMessageBox.warning(
    #             None, "Error", "이미지를 로드하는 데 실패했습니다."
    #         )
    #         return
    #     self.widget.setPixmap(pixmap)
    #     self.widget.repaint()  # 화면 갱신

    def capture(self):
        # 콤보 박스에서 텍스트를 가져와 파일명에 포함
        shape = self.comboBox.currentText()
        position = self.comboBox_2.currentText()
        if not shape or not position:
            QtWidgets.QMessageBox.warning(
                None, "Warning", "모형 이름과 위치를 입력하세요."
            )
            return

        # 현재 시간을 기반으로 파일명 생성
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(
            source_folder, shape, position, f"{timestamp}_capture.jpg"
        )

        # 현재 프레임이 저장되어 있는지 확인하고 저장
        if hasattr(self, "current_frame"):
            cv2.imwrite(filename, self.current_frame)
            QtWidgets.QMessageBox.information(
                None, "Saved", f"이미지를 저장했습니다: {filename}"
            )
            self.display_captured_image(filename)
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "저장할 프레임이 없습니다.")

    def additem_combobox_1(self, comboBox):
        path = source_folder
        result_path = os.path.join(path, "result")

        if not os.path.exists(result_path):
            os.makedirs(result_path)

        shape_list = [
            f
            for f in os.listdir(path)
            if os.path.isdir(os.path.join(path, f)) and f != "result"
        ]
        comboBox.clear()
        comboBox.addItems(shape_list)

    def update_position_combobox(self):
        # 선택된 모양에 따라 위치 콤보박스를 업데이트
        shape = self.comboBox.currentText()
        if shape:
            path = os.path.join(source_folder, shape)
            if os.path.exists(path):
                position_list = [
                    f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))
                ]
                self.comboBox_2.clear()
                self.comboBox_2.addItems(position_list)
            else:
                self.comboBox_2.clear()

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
