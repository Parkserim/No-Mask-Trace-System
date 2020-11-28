import cv2
import time

from Session import Session
from Detect import Detect
from Recognition import Recognition
from playsound import playsound

prevTime = 0
count_no_mask = 0


cap = cv2.VideoCapture(cv2.CAP_DSHOW)
while True:
    ret, image = cap.read()

    if ret:
        no_mask_faces = []

        # Cal Frame
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        fps = 1 / (sec)

        print(fps)
        Mask_Detect = Detect(image)

        # Detect Face
        Mask_Detect.detectFace()

        if len(Mask_Detect.face_lst) != 0:

            # Detect Mask & NOSE & MASK IN FACE
            Mask_Detect.detectMaskNose()

            # 조건에 맞게 결과 도출
            for face_info in Mask_Detect.face_lst:
                x1, y1, x2, y2 = face_info["roi_face"]
                mask_status = face_info["with_mask"]
                nose_status = face_info["with_nose"]
                color = (0, 0, 0)
                label = ""

                # 마스크 탐지 and 코 미 탐지
                if mask_status == True and nose_status == False:
                    color = (0, 255, 0)
                    label = "With Mask"

                # 마스크 탐지 & 코 탐지 => 반 만 착용
                if mask_status == True and nose_status == True:
                    color = (0, 182, 255)
                    label = "Half Mask"
                    Mask_Detect.check_no_mask = True

                # 마스크 미탐지 => 마스크 미착용
                elif mask_status == False:
                    color = (0, 0, 255)
                    label = "No Mask"
                    Mask_Detect.check_no_mask = True

                Mask_Detect.writeLabel([x1, y1, x2, y2], color, label)

        if Mask_Detect.check_no_mask == True:
            count_no_mask += 1

        else:
            count_no_mask = 0

        cv2.putText(
            Mask_Detect.image,
            str(count_no_mask),
            (0, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

        Mask_Detect.showImage()

        if count_no_mask == 5:
            count_no_mask = 0
            # print("마스크 미착용자 발견")
            playsound("sound.wav")
            time.sleep(3)

        if cv2.waitKey(250) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
