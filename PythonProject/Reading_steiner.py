import cv2
import sys as s

#변수 선언
title = "homework"
key_dct = {"space bar":32, "0":48, "up":2490368,
    "down":2621440 ,"left":2424832, "right":2555904, "s":115}
flag, fps, pre_fps, val, sbar_flag, current, entire = 0, round(1000/29.97), 0, 1, False, 0, 1
capture = cv2.VideoCapture("movie.mp4")

while True:
    ret, frame = capture.read()
    key = cv2.waitKeyEx(fps)

    #현재 프레임 순서 저장
    num = capture.get(cv2.CAP_PROP_POS_FRAMES)

    #ESC를 누르거나 창이 없어졌거나 num이 마지막 프레임일 경우
    if key == 27 or not capture.isOpened() or num == 1850:
        flag = 1
        break

    #S를 누를 경우 현재 프레임을 jpg로 저장
    elif key == key_dct["s"]:
        cv2.imwrite(str(int(num))+".jpg", frame)

    #0을 누를 경우 처음으로 이동
    elif key == key_dct["0"]:
        capture.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    #fps값을 2씩 나눠 영상 속도 배속
    elif key == key_dct["up"]:
        if val <= 0.125:
            continue
        fps //= 2
        val /= 2

    #fps값을 2씩 곱해 영상 속도 감속
    elif key == key_dct["down"]:
        if val >= 8:
            continue
        fps *= 2
        val *= 2

    #현재 프레임 기준으로 5프레임씩 앞으로 이동
    elif key == key_dct["left"]:
        current = capture.get(cv2.CAP_PROP_POS_FRAMES) - 5
        if current <= 0:
            current = 0
        capture.set(cv2.CAP_PROP_POS_FRAMES, current)

    #현재 프레임 기준으로 5프레임씩 뒤로 이동
    elif key == key_dct["right"]:
        current = capture.get(cv2.CAP_PROP_POS_FRAMES) + 5
        capture.set(cv2.CAP_PROP_POS_FRAMES, current)

    #영상 정지, 재생을 토글형으로 구현
    elif key == key_dct["space bar"]:
        sbar_flag = not sbar_flag
        if sbar_flag: pre_fps = fps
        fps = 0
        if not sbar_flag and fps == 0:
            fps = pre_fps

    cv2.putText(frame, "x"+str(1/val), (210, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 180, 29), 2)
    cv2.putText(frame, "#"+str(int(num)), (210,65), cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 180, 29), 2)
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, frame)
    cv2.resizeWindow(title, 1920, 1080)

if flag == 1:
    s.exit(0)
cv2.destroyAllWindows()
capture.release()