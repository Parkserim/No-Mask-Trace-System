import dlib
import requests
import json
import numpy as np
import cv2
import datetime

facerec = dlib.face_recognition_model_v1(
    "models/dlib_face_recognition_resnet_model_v1.dat"
)
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")


class Recognition:
    def __init__(self, url, location, sublocation):
        self.url = url + "api/recognition/"
        self.location = location
        self.sublocation = sublocation

    def loadCompareEncode(self):
        print("Data Receive Start")
        self.responses = requests.get(url=self.url).json()
        print("Data Receive Success")

    def compareEncode(self, image, roi):
        x1, y1, x2, y2 = roi
        rect = dlib.rectangle(x1, y1, x2, y2)

        shape = predictor(image, rect)
        encodeImg = facerec.compute_face_descriptor(image, shape)
        prev_dist = 1
        recognition_label = "unknown"
        recognition_detect = False

        for recognition in self.responses:
            encodeCompare = json.loads(recognition["encodeLst"])
            pk = str(recognition["pk"])
            dist = np.linalg.norm(
                np.array(encodeCompare) - np.array(encodeImg), axis=0,
            )
            if dist < 0.45 and dist < prev_dist:
                prev_dist = dist
                recognition_label = pk
                recognition_detect = True

        return [recognition_label, recognition_detect]

    def registerEncode(
        self, image, no_mask_faces,
    ):
        for roi in no_mask_faces:
            x1, y1, x2, y2 = roi

            w = x2 - x1
            h = y2 - y1
            left = x1
            right = x1 + w
            top = y1
            bottom = y1 + h

            face = image[top:bottom, left:right]

            rect = dlib.rectangle(x1, y1, x2, y2)

            shape = predictor(image, rect)
            encodeImg = facerec.compute_face_descriptor(image, shape)

            imencoded = cv2.imencode(".jpg", face)[1]
            date = datetime.datetime.today()
            date_str = date.strftime("%Y-%m-%d %H:%M:%S")
            files = {
                "image": (f"{date_str}.jpg", imencoded.tobytes(), "image/jpeg",)
            }

            response = requests.post(
                url=self.url,
                data={
                    "encodeLst": f"{list(encodeImg)}",
                    "description": f"{self.location} / {self.sublocation}",
                    "created_at": date,
                },
                files=files,
            )
            if response.status_code == 201:
                print("Encode Register Success")
            else:
                print("Encode Register Fail")

        self.loadCompareEncode()

