import json
import os

import plyer
from kivy import platform
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from scripts.activity_manager import ActivityManager
from scripts.sql_manager import SQLManager
from plyer import wifi


DEBUG = False

class UserManager:
    MAIN_ADDRESS = "https://api.green-stem.eu"
    DEFAULT_HEADERS = {
        "Content-Type": "application/json"
    }
    SAVE_ADDRESS = "user_data.json"

    def __init__(self):
        self.active = False
        self.user_token = None
        self.user_id = None
        self.user_data = {}
        self.activity_manager = None
        self.sql_manager = None
        self.wifi_check_event = None

    def load_user_data(self):
        if DEBUG:
            self.write_user_data("NONE", {"username":"admin","email":"admin@gmail.co1",
                                                                "id":"12345","verified":True,
                                                                "weight":80,"height":180,"age":20,"gender":"male"})
            return True
        if not os.path.isfile(self.SAVE_ADDRESS):
            return False
        user_file = open(self.SAVE_ADDRESS, "r")
        user_data = json.load(user_file)
        self.write_user_data(user_data["token"], user_data["user_data"])
        return True

    def write_user_data(self, user_token, user_data):
        if self.active:
            raise RuntimeError("User already logged in!")
        self.active = True
        self.user_token = user_token
        self.user_data = user_data
        print(f"User data: {user_data}")
        self.user_id = user_data["id"]
        self.sql_manager = SQLManager(self.user_id)
        self.activity_manager = ActivityManager(self.user_id,self.sql_manager)
        if platform == "android":
            # starting to check if wifi is available
            self.wifi_check_event = Clock.schedule_once(self.check_for_wifi)
        print(self.activity_manager)
        self.save_user_data()

    def save_user_data(self):
        if not self.active:
            return "Please log user first!"
        savedata = json.dumps({
            "token": self.user_token,
            "user_data": self.user_data
        })
        with open(self.SAVE_ADDRESS, "w") as user_file:
            user_file.write(savedata)

    def overwrite_user_data(self, user_data):
        print(user_data.get("username"))
        if user_data.get("username") != self.user_data["username"] and user_data.get("username"):
            raise RuntimeError("Trying to overwrite but users do not match!")
        for key in user_data.keys():
            self.user_data[key] = user_data[key]

    def check_for_wifi(self,dt):
        if wifi.is_connected():
            print("connected to wifi, checking if upload needed")
            self.sql_manager.upload_all()

    def erase_user_data(self):
        self.user_token = None
        self.user_data = None
        self.user_id = None
        self.active = False
        if self.wifi_check_event:
            self.wifi_check_event.cancel()
        if os.path.isfile(self.SAVE_ADDRESS):
            os.remove(self.SAVE_ADDRESS)

    def get_user_token(self):
        return self.user_token

    def get_user_id(self):
        return self.user_id

    def get_user_attribute(self, key):
        return self.user_data.get(key)

    def send_request(self, path="/", method="GET", body=None, error_func=None, success_func=None, headers=None):
        if headers is None:
            headers = self.DEFAULT_HEADERS
        path.removeprefix("/")

        if self.get_user_token():
            headers["Authorization"] = self.get_user_token()

        print(f"Path: {self.MAIN_ADDRESS + path}\nHeaders: {headers}")
        UrlRequest(self.MAIN_ADDRESS + path,
                   method=method,
                   req_body=body,
                   req_headers=headers,
                   on_success=lambda a, b: success_func(a, b),
                   on_failure=lambda a, b: error_func(a, b),
                   on_error=lambda a, b: error_func(a, b))
