import cv2

capture = cv2.VideoCapture(0)  # 0번 카메라 연결

if capture.isOpened() == False:
    print("camera open failed")
    exit()

capNum = int(0)
while True:  # 무한 반복
    ret, frame = capture.read()  # 카메라 영상 받기

    if not ret:
        print("Can't read camera")
        break

    cv2.imshow("ex01", frame)

    if cv2.waitKey(1) == ord("c"):  # c를 누르면 화면 캡쳐 후 파일경로에 저장
        img_captured = cv2.imwrite(
            "C:/Users/user/Documents/MES/patchcore/pict/captured_%03d.png" % capNum,
            frame,
        )
        capNum += 1  # 캡쳐시마다 번호증가

    if cv2.waitKey(1) == ord("q"):  # q를 누르면 while문 탈출
        break

capture.release()
