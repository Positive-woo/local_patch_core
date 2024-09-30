# services/camera_service.py
import cv2
import threading
from PyQt5 import QtWidgets, QtCore, QtGui

# 전역 변수 설정
running = False
msg_box = None  # 메시지 박스를 전역 변수로 선언하여 제어 가능하게 함
label = None  # QLabel도 전역 변수로 설정


def run():
    global running, msg_box, label
    cap = cv2.VideoCapture(0)  # 카메라 장치 열기

    # 캡처한 프레임의 너비와 높이 가져오기
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    label.resize(width, height)  # QLabel 크기 조정

    while running:
        ret, img = cap.read()  # 프레임 읽기
        if ret:
            # 프레임을 RGB로 변환
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, c = img.shape

            # QImage로 변환 후 QLabel에 표시
            qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            label.setPixmap(pixmap)
        else:
            QtWidgets.QMessageBox.about(label, "Error", "Cannot read frame.")
            print("Cannot read frame.")
            break

    cap.release()  # 카메라 해제
    print("Thread end.")


def stop():
    global running
    running = False
    print("Stopped.")


def start():
    global running, msg_box
    running = True

    # # "잠시 기다려 달라"는 메시지를 띄움
    # msg_box = QtWidgets.QMessageBox()
    # msg_box.setWindowTitle("카메라 초기화 중")
    # msg_box.setText("카메라를 설정하는 중입니다. 잠시만 기다려 주세요...")
    # msg_box.setStandardButtons(QtWidgets.QMessageBox.NoButton)
    # msg_box.show()

    # 카메라를 실행할 스레드 생성 및 시작
    th = threading.Thread(target=run)
    th.start()
    print("Started.")


def onExit():
    print("Exit")
    stop()


def set_label(new_label):
    global label
    label = new_label  # label을 메인에서 전달받아 사용


def print_msg():
    print("Hello")
