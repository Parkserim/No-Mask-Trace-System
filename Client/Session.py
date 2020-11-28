import requests
import cv2
import datetime


class Session:
    def __init__(self, url):
        username = "admin"
        password = "1"
        self.username = username
        self.password = password
        self.url = url
        # url = "http://localhost:8000/"
        self.token = ""

    def login(self):
        login_url = self.url + "api/auth/login/"
        response = requests.post(
            url=login_url,
            data={"username": self.username, "password": self.password},
        )
        self.token = response.json()["token"]
        print("Login Success")

    def logout(self):
        logout_url = self.url + "api/auth/logout/"
        response = requests.post(
            url=logout_url, headers={"Authorization": "Token " + self.token}
        )
        print("Logout succes!")

    def postImage(self, image, location, sublocation):
        post_url = self.url + "api/files/"

        imencoded = cv2.imencode(".jpg", image)[1]
        date = datetime.datetime.today()
        date_str = date.strftime("%Y-%m-%d %H:%M:%S")
        files = {
            "image": (f"{date_str}.jpg", imencoded.tobytes(), "image/jpeg",)
        }
        data = {
            "name": f"{date_str}.jpg",
            "location": location,
            "sublocation": sublocation,
            "created_at": date,
        }
        response = requests.post(
            url=post_url,
            data=data,
            files=files,
            headers={"Authorization": "Token " + self.token},
        )

        print(response.status_code)
        if response.status_code == 201:
            print("Image Register Success")
        else:
            print("Image Register Fail")

