import cv2

face_detect_model = cv2.dnn.readNet(
    "models/face_detect.prototxt", "models/face_detect.caffemodel"
)
nose_detect_model = cv2.dnn.readNet(
    "models/nose_detect.pb", "models/nose_detect.pbtxt",
)
mask_detect_model = cv2.dnn.readNet(
    "models/mask_detect.pb", "models/mask_detect.pbtxt",
)


class Detect:
    def __init__(self, image):
        self.image = image
        self.frame = image.copy()
        self.image_height, self.image_width, _ = image.shape
        self.face_lst = list()
        self.check_no_mask = False

    def detectFace(self):
        h, w, _ = self.frame.shape
        blob = cv2.dnn.blobFromImage(
            self.frame,
            scalefactor=1.0,
            size=(300, 300),
            mean=(104.0, 177.0, 123.0),
            swapRB=True,
        )
        face_detect_model.setInput(blob)
        face_detect = face_detect_model.forward()

        for i in range(face_detect.shape[2]):
            confidence = face_detect[0, 0, i, 2]
            if confidence < 0.5:
                continue

            x1 = int(face_detect[0, 0, i, 3] * w)
            y1 = int(face_detect[0, 0, i, 4] * h)
            x2 = int(face_detect[0, 0, i, 5] * w)
            y2 = int(face_detect[0, 0, i, 6] * h)

            face_info = {
                "roi_face": [x1, y1, x2, y2],
                "with_nose": False,
                "with_mask": False,
            }
            self.face_lst.append(face_info)

    def detectMaskNose(self):
        for index, face_info in enumerate(self.face_lst):
            x1, y1, x2, y2 = face_info["roi_face"]
            x1, y1, x2, y2 = self.validateRoi(x1, y1, x2, y2)

            w = x2 - x1
            h = y2
            left = x1
            right = x1 + w
            top = y1
            bottom = y1 + h

            face = self.frame[top:bottom, left:right]

            blob = cv2.dnn.blobFromImage(
                face, scalefactor=1.0, size=(300, 300), swapRB=True,
            )

            mask_detect_model.setInput(blob)
            mask_detect = mask_detect_model.forward()

            for i in range(mask_detect.shape[2]):
                confidence = mask_detect[0, 0, i, 2]

                if confidence < 0.5:
                    continue

                face_info["with_mask"] = True
                self.face_lst[index] = face_info
                # mask_x1 = left + int(mask_detect[0, 0, i, 3] * w)
                # mask_y1 = top + int(mask_detect[0, 0, i, 4] * h)
                # mask_x2 = left + int(mask_detect[0, 0, i, 5] * w)
                # mask_y2 = top + int(mask_detect[0, 0, i, 6] * h)
                # cv2.rectangle(
                #     self.image,
                #     pt1=(mask_x1, mask_y1),
                #     pt2=(mask_x2, mask_y2),
                #     thickness=2,
                #     color=(0, 0, 255),
                #     lineType=cv2.LINE_AA,
                # )

            w = x2 - x1
            h = y2 - y1
            left = x1
            right = x1 + w
            top = y1
            bottom = y1 + h

            face = self.frame[top:bottom, left:right]

            blob = cv2.dnn.blobFromImage(
                face, scalefactor=1.0, size=(300, 300), swapRB=True,
            )

            nose_detect_model.setInput(blob)
            nose_detect = nose_detect_model.forward()

            for i in range(nose_detect.shape[2]):
                confidence = nose_detect[0, 0, i, 2]

                if confidence < 0.5:
                    continue

                face_info["with_nose"] = True
                self.face_lst[index] = face_info
                # nose_x1 = left + int(nose_detect[0, 0, i, 3] * w)
                # nose_y1 = top + int(nose_detect[0, 0, i, 4] * h)
                # nose_x2 = left + int(nose_detect[0, 0, i, 5] * w)
                # nose_y2 = top + int(nose_detect[0, 0, i, 6] * h)
                # cv2.rectangle(
                #     self.image,
                #     pt1=(nose_x1, nose_y1),
                #     pt2=(nose_x2, nose_y2),
                #     thickness=2,
                #     color=(255, 0, 0),
                #     lineType=cv2.LINE_AA,
                # )

    def writeLabel(self, roi, color, label):
        x1, y1, x2, y2 = roi
        x1, y1, x2, y2 = self.validateRoi(x1, y1, x2, y2)

        cv2.rectangle(
            self.image, (x1, y2 - 12), (x2, y2 + 12), color, cv2.FILLED,
        )
        cv2.rectangle(self.image, (x1, y1), (x2, y2), color, 1)
        cv2.putText(
            self.image,
            f"{label}",
            (x1 + 6, y2 + 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    def showImage(self):
        cv2.imshow("image", self.image)

    def validateRoi(self, x1, y1, x2, y2):
        if x1 <= 0:
            x1 = 0
        if y1 <= 0:
            y1 = 0
        if x2 >= self.image_width:
            x2 = self.image_width
        if y2 >= self.image_height:
            y2 = self.image_height
        return x1, y1, x2, y2

