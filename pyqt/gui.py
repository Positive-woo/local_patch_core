import time
from PyQt5 import QtCore, QtWidgets
import cv2
from dotenv import load_dotenv
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path
import os

from patchcore import get_inferencer, infer

load_dotenv()
source_folder = os.getenv("SOURCE_FOLDER")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 560)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 정상 이미지 출력 layout (QLabel로 변경)
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(600, 10, 590, 370))
        self.image.setObjectName("image")
        self.image.setScaledContents(True)  # 이미지 크기에 맞게 자동으로 조정

        # 현재 캠 출력 layout
        self.widget = QtWidgets.QLabel(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 590, 370))
        self.widget.setObjectName("cam_view")
        self.widget.setScaledContents(True)  # 이미지 크기에 맞게 자동으로 조정

        # 모양 콤보박스
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 420, 311, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("shape_cb")
        self.additem_combobox_1(self.comboBox)

        # 모양 라벨
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 420, 71, 21))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("shape")

        # 위치 콤보박스
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 450, 311, 22))
        self.comboBox_2.setEditable(True)
        self.comboBox.setCurrentText("")
        self.comboBox_2.setObjectName("position_cb")

        # 모양 콤보박스 선택이 변경될 때 위치 콤보박스 업데이트
        self.comboBox.currentIndexChanged.connect(self.update_position_combobox)

        # 위치 라벨
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 450, 71, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("position")

        # 브라우져 버튼
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setGeometry(QtCore.QRect(90, 480, 311, 22))
        self.browse_button.setText("파일 브라우저로 이미지 선택")
        self.browse_button.clicked.connect(self.browse_image)  # 파일 브라우저 기능 연결

        # 캡쳐 버튼
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1100, 420, 91, 91))
        self.pushButton.setObjectName("cam_capture")

        # 결과 표시 QLabel
        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setGeometry(QtCore.QRect(625, 420, 450, 91))
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_label.setStyleSheet("border: 1px solid black;")
        self.result_label.setText("...")
        self.result_label.setStyleSheet(
            "background-color: grey; color: white; border: 1px solid black;"
        )

        # warning_label 초기 상태 설정 (처음엔 빈 상태)
        self.warning_label = QtWidgets.QLabel(self.centralwidget)
        self.warning_label.setGeometry(QtCore.QRect(625, 385, 450, 30))
        self.warning_label.setAlignment(QtCore.Qt.AlignCenter)
        self.warning_label.setStyleSheet("color: black; font-size: 12px; border: none;")
        self.warning_label.setText("")

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
        shape = self.comboBox.currentText()
        position = self.comboBox_2.currentText()
        if not shape or not position:
            QtWidgets.QMessageBox.warning(
                None, "Warning", "모형 이름과 위치를 입력하세요."
            )
            return
        # 파일 선택 다이얼로그 열기
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "이미지 선택", "", "Image Files (*.png *.jpg *.bmp)"
        )

        if file_path:
            ### patch core 돌린 후 경로 반환 ###
            self.display_captured_image(file_path)

    def display_captured_image(self, filepath):
        # 패치코어 다녀오기 #
        patch_core_result = self.patch_core(filepath)

        pixmap = QPixmap(patch_core_result)
        if pixmap.isNull():
            QtWidgets.QMessageBox.warning(
                None, "Error", "이미지를 로드하는 데 실패했습니다."
            )
            return

        self.image.setPixmap(pixmap)
        self.image.repaint()  # 화면 갱신

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

        directory = os.path.dirname(filename)  # 경로에서 디렉토리만 추출

        # 경로가 존재하지 않으면 디렉토리 생성
        if not os.path.exists(directory):
            os.makedirs(directory)
            QtWidgets.QMessageBox.information(
                None, "Info", "디렉토리가 없어서 생성되었습니다."
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

        shape_list = [
            f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Patchcore_Camera"))
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

    def patch_core(self, image_path):
        shape = self.comboBox.currentText()
        position = self.comboBox_2.currentText()
        path = os.path.join(source_folder, shape, position)
        weights_path = Path(path + "/model.onnx")
        metadata_path = Path(path + "/metadata.json")
        output_path = Path(path)
        time_stamp = os.path.basename(image_path)

        if not os.path.exists(weights_path):
            self.warning_label.setText(
                """훈련이 되지 않은 모델로 예상됩니다.\n선택하신 모형은 최신 촬영한 사진만 출력됩니다."""
            )
            self.result_label.setText("...")
            self.result_label.setStyleSheet(
                "background-color: grey; color: white; border: 1px solid black; font-size: 30px;"
            )
            return image_path

        self.warning_label.setText("")
        if "_capture.jpg" in time_stamp:
            time_stamp = time_stamp.replace("_capture.jpg", "")
        elif ".png" in time_stamp:
            time_stamp = time_stamp.replace(".png", "")

        inferencer = get_inferencer(weight_path=weights_path, metadata=metadata_path)

        image = cv2.imread(str(image_path))
        if image is None:
            raise FileNotFoundError(f"경로 내에 이미지를 로드할 수 없음")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        segmentations, pred_score = infer(image, inferencer)

        label_text = f"MODEL : {shape}_{position}"

        h, w, _ = segmentations.shape

        # 라벨링 위치 설정 (우측 하단)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.001 * h
        font_thickness = max(1, int(0.003 * h))
        text_size, _ = cv2.getTextSize(label_text, font, font_scale, font_thickness)
        text_w, text_h = text_size

        # 빨간색 사각형 그리기 (우측 하단)
        rectangle_bgr = (0, 0, 255)  # 빨간색 사각형
        text_x = int(0.95 * w - text_w)  # 우측에서 약간 여유
        text_y = int(0.95 * h - text_h)  # 하단에서 약간 여유
        cv2.rectangle(
            segmentations,
            (text_x, text_y),
            (int(0.95 * w), int(0.95 * h)),
            rectangle_bgr,
            -1,
        )

        # 흰색 글씨로 텍스트 적기
        text_color = (255, 255, 255)  # 흰색 텍스트
        cv2.putText(
            segmentations,
            label_text,
            (text_x, text_y + text_h),
            font,
            font_scale,
            text_color,
            font_thickness,
        )

        # return "이미지 경로"
        cv2.imwrite(str(output_path / f"{time_stamp}_result.png"), segmentations)

        result_image = os.path.join(output_path, f"{time_stamp}_result.png")

        self.pred_score = pred_score
        self.update_result()
        return result_image

    def update_result(self):
        # 위치와 숫자에 따라 결과 설정
        position = self.comboBox_2.currentText()
        value = self.pred_score

        if position:
            if value < 0.5:
                self.result_label.setText(f"PASS : {value:.2f}")
                self.result_label.setStyleSheet(
                    "background-color: green; color: white; border: 1px solid black; font-size: 30px;"
                )
            elif value >= 0.5:
                self.result_label.setText(f"NG : {value:.2f}")
                self.result_label.setStyleSheet(
                    "background-color: red; color: white; border: 1px solid black; font-size: 30px;"
                )
                if value > 0.75:
                    self.warning_label.setText(
                        "value가 너무 큽니다 ! 선택하신신 [모형 이름]과 [위치]가 맞는지 확인해주세요."
                    )
            else:
                self.result_label.setText("...")
                self.result_label.setStyleSheet(
                    "background-color: grey; color: white; border: 1px solid black; font-size: 30px;"
                )
        else:
            self.result_label.setText("...")
            self.result_label.setStyleSheet(
                "background-color: grey; color: white; border: 1px solid black; font-size: 30px;"
            )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
