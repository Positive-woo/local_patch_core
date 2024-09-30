# main.py
import sys
from PyQt5 import QtWidgets
from services.test2 import start, stop, onExit, set_label, print_msg

# PyQt5 어플리케이션 생성
app = QtWidgets.QApplication([])

# 윈도우 및 레이아웃 설정
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()

# 카메라 출력용 QLabel 및 버튼 설정
label = QtWidgets.QLabel()
btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")
btn_print = QtWidgets.QPushButton("print")

# services의 set_label 함수를 호출해 QLabel 설정
set_label(label)

# 레이아웃에 위젯 추가
vbox.addWidget(label)
vbox.addWidget(btn_start)
vbox.addWidget(btn_stop)
vbox.addWidget(btn_print)

win.setLayout(vbox)
win.show()
start()

# 버튼 클릭 시 실행될 함수 연결
btn_start.clicked.connect(start)
btn_stop.clicked.connect(stop)
btn_print.clicked.connect(print_msg)

# 어플리케이션 종료 시 호출될 함수 연결
app.aboutToQuit.connect(onExit)

# 어플리케이션 실행
sys.exit(app.exec_())
