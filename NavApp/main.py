import os
from kivy import Config
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.screenmanager import MDScreenManager
from kivy.utils import platform
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from scripts.user_manager import UserManager
from kivy.core.window import Window

print(f"platform is: {platform}")
if not platform == "android":
    Config.set('graphics', 'width', '390')
    Config.set('graphics', 'height', '780')
    Window.size = (390, 780)

print(os.name)
from scripts.imports import *

# ovo će importati novostvoreni file!
# try:
#     from __gen__imports__ import *
# except ImportError:
#     raise ImportError("There might be a problem with import generator!")


from __gen__imports__ import *


class MainScreenManager(MDScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.screen_names)
        self.active_user = UserManager()
        self.current = "lgn"
        self.dimensions = (Config.get("graphics", "width"), Config.get("graphics", "height"))
        self.running_processes = []
        self.screen_refs = {i: self.screen_names[i] for i in range(len(self.screen_names))}
        self.window_subroutines()
        self.key_history = ["-"]

    def add_process(self, ref):
        self.running_processes.append(ref)

    def window_subroutines(self):
        ##ENABLED
        Window.bind(on_key_down=self.key_pressed)

    def key_pressed(self, *args):
        self.key_history.append(args[-2])
        if len(self.key_history) > 100:
            self.key_history = self.key_history[-3:]
        print(f"pressed {self.key_history[-1]}")
        if self.key_history[-1] in map(str, self.screen_refs.keys()) and self.key_history[-2] == "ı":
            self.goto_screen(self.screen_refs[int(self.key_history[-1])])

    def goto_screen(self, scrn):
        for event in self.running_processes:
            event.cancel()
        self.running_processes.clear()
        scrn_ref = self.get_screen(scrn)
        if hasattr(scrn_ref, "start_repeatable_intervals"):
            scrn_ref.start_repeatable_intervals()
        if hasattr(scrn_ref, "start_up_screen"):
            scrn_ref.start_up_screen()
        self.current = scrn
        self.transition = FadeTransition()


class FitnessApp(MDApp):

    def __init__(self):
        super().__init__()
        self.theme_cls.theme_style = "Dark"
        print(self.theme_cls.bg_dark)
        self.primary_colors = {
            "black": (28 / 255, 28 / 255, 28 / 255, 1),
            "white": (255 / 255, 255 / 255, 255 / 255, 1),
            "light_blue": (95 / 255, 163 / 255, 201 / 255, 1),
            "dark_blue": (22 / 255, 91 / 255, 129 / 255, 1),
            "dark_grey": (71 / 255, 71 / 255, 71 / 255, 0.5),
            "placeholder": (72 / 255, 33 / 255, 183 / 255, 1),
            "light_grey": (174 / 255, 174 / 255, 174 / 255, 1),
            "darker_grey": (44 / 255, 44 / 255, 46 / 255, 1),
            "green": (103 / 255, 201 / 255, 95 / 255, 1),
            "orange": (231 / 255, 100 / 255, 27 / 255, 1),
            "error_color": (255 / 255, 36 / 255, 36 / 255, 1)
        }
        self.fonts = {
            "sans_semi_bold": "assets/fonts/OpenSans_SemiBold.ttf",
            "sans_regular": "assets/fonts/OpenSans_Regular.ttf",
            "actor_regular": "assets/fonts/Actor_Regular.ttf",
            "advent_regular": "assets/fonts/AdventPro_Regular.ttf"
        }
        self.size = Window.size
        self.ratio = self.size[1] / self.size[0]

    def build(self):
        return MainScreenManager()


load_list = import_list_kv

for f_name in load_list:
    Builder.load_file(f_name)

Builder.load_file("core.kv")

if __name__ == "__main__":
    App = FitnessApp()
    App.run()
