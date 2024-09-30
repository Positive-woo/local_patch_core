import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel,
    QFrame,
    QDesktopWidget,
    QVBoxLayout,
    QComboBox,
    QSizePolicy,
)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 그리드 레이아웃 설정
        grid = QGridLayout()
        self.setLayout(grid)

        # 각 영역을 메서드로 호출하여 구성
        original = self.original_box()
        cam = self.cam_box()
        options_L, options_C, options_R = self.options_box()

        # 레이아웃에 위젯 추가 (행, 열 위치)
        grid.addWidget(original, 0, 0)  # 첫 번째 행, 첫 번째 열 (왼쪽 상단)
        grid.addWidget(
            cam, 0, 1, 1, 2
        )  # 첫 번째 행, 두 번째와 세 번째 열 병합 (오른쪽 상단)

        grid.addWidget(options_L, 1, 0)  # 두 번째 행, 첫 번째 열
        grid.addWidget(options_C, 1, 1)  # 두 번째 행, 두 번째 열
        grid.addWidget(options_R, 1, 2)  # 두 번째 행, 세 번째 열

        # 열 비율 설정
        grid.setColumnStretch(0, 2)  # 첫 번째 열 비율
        grid.setColumnStretch(1, 1)  # 두 번째 열 비율
        grid.setColumnStretch(2, 1)  # 세 번째 열 비율 (아래 행에서만 사용)

        # 첫 번째 행(위쪽 두 박스)에 높은 비율 할당, 두 번째 행(아래 박스)에 낮은 비율 할당
        grid.setRowStretch(0, 3)  # 첫 번째 행의 높이 비율을 3으로 설정
        grid.setRowStretch(1, 1)  # 두 번째 행(아래 박스)의 높이 비율을 1로 설정 (작게)

        # 윈도우 타이틀과 크기 설정
        self.setWindowTitle("Custom Grid Layout")
        self.resize(1600, 700)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()  # 창의 크기 정보 가져오기
        cp = QDesktopWidget().availableGeometry().center()  # 화면의 중심 좌표 얻기
        qr.moveCenter(cp)  # 창의 중심을 화면의 중심으로 이동
        self.move(qr.topLeft())  # 창의 좌상단 좌표를 맞춰서 창을 이동

    ### 화면 구성 ###
    def original_box(self):
        original = QLabel("정상이미지")
        original.setFrameStyle(QFrame.Box)
        return original

    def cam_box(self):
        cam = QLabel("카메라")
        cam.setFrameStyle(QFrame.Box)
        return cam

    def options_box(self):
        # options를 3열로 나눠서 각 부분 생성
        options_L = QLabel("옵션 L")
        options_L.setFrameStyle(QFrame.Box)

        options_C = QLabel("")

        options_R = QLabel("옵션 R")
        options_R.setFrameStyle(QFrame.Box)

        return options_L, options_C, options_R


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
