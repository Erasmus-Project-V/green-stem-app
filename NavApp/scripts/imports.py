from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from NavApp.screens.authentication.sign_up_screen.sign_up_screen import SignUpScreen
from NavApp.screens.authentication.log_in_screen.log_in_screen import LogInScreen
from NavApp.screens.activity.home_screen.home_screen import HomeScreen
from NavApp.screens.activity.activity_screen.activity_screen import ActivityScreen

import os

import_list_kv = []
import_list_py = []

# might be buggy
search_dir = "NavApp/screens"


def py_import_gen(py_abs_path, name):
    class_name = "".join([element[0].upper() + element[1:] for element in name.split("_")])

    import_string = "from " + py_abs_path.replace("/", ".") + " import " + class_name
    return import_string


def seek(cd):
    directories = os.listdir(cd)
    for dir in directories:
        if "_screen" in dir:
            base = cd + "\\" + dir
            if not os.listdir(base):
                return
            import_list_kv.append(base + ".kv")
            print(import_list_kv)
            import_list_py.append(py_import_gen(base, dir))

        else:
            seek(cd + "\\" + dir)


if __name__ == "__main__":
    seek(os.getcwd().removesuffix("scripts") + "screens")
else:
    search_dir = os.getcwd()
    print("Please start from main")
    print(os.getcwd() + "\\screens")
    seek(search_dir+ "\\screens")
