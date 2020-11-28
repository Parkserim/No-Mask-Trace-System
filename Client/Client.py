import cv2
import time

from Session import Session
from Detect import Detect
from Recognition import Recognition
from playsound import playsound

prevTime = 0
count_no_mask = 0

# Const Value
# 아마존 서버 주소
URL = "http://ec2-13-209-88-225.ap-northeast-2.compute.amazonaws.com/"

# 로컬 서버 주소
# URL = "http://localhost:8000/"

LOCATION = "비즈니스센터"
SUBLOCATION = "802"

# 토큰 발행(인증)
session = Session(URL)
session.login()

recognition = Recognition(URL, LOCATION, SUBLOCATION)
recognition.loadCompareEncode()

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

                    (
                        recognition_label,
                        recognition_detect,
                    ) = recognition.compareEncode(
                        Mask_Detect.frame, [x1, y1, x2, y2]
                    )

                    label = label + " - " + recognition_label

                    if not recognition_detect:
                        no_mask_faces.append([x1, y1, x2, y2])

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
            print("마스크 미착용자 발견")

            if len(no_mask_faces) != 0:
                recognition.registerEncode(Mask_Detect.frame, no_mask_faces)

            playsound("sound.wav")
            session.postImage(Mask_Detect.image, LOCATION, SUBLOCATION)
            time.sleep(3)

        if cv2.waitKey(250) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
session.logout()
