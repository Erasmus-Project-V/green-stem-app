import os
from kivy import Config
from kivy.clock import Clock

Config.set('graphics', 'width', '390')
Config.set('graphics', 'height', '780')

print(os.name)
if os.name == 'nt' or "linux":
    from scripts.imports import *
else:
    from scripts.mac_imports import *

# ovo će importati novostvoreni file!
try:
    from scripts.__gen__imports__ import *
except ImportError:
    raise ImportError("There might be a problem with import generator!")


# from scripts.__gen__imports__ import *

class MainScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.screen_names)
        self.current = "lgn"
        self.running_processes = []
        self.screen_refs = {i: self.screen_names[i] for i in range(len(self.screen_names))}
        self.window_subroutines()

    def add_process(self, ref):
        self.running_processes.append(ref)

    def window_subroutines(self):
        ##ENABLED
        Window.bind(on_key_down=self.key_pressed)

    def key_pressed(self, *args):
        key = args[-2]
        print(f"pressed {key}")
        if key in map(str, self.screen_refs.keys()):
            self.goto_screen(self.screen_refs[int(key)])

    def goto_screen(self, scrn):
        for event in self.running_processes:
            event.cancel()
        self.running_processes.clear()
        scrn_ref = self.get_screen(scrn)
        if hasattr(scrn_ref, "start_repeatable_intervals"):
            scrn_ref.start_repeatable_intervals()
        self.current = scrn


class FitnessApp(MDApp):

    def __init__(self):
        super().__init__()
        self.theme_cls.theme_style = "Dark"
        self.primary_colors = {
            "black": (28 / 255, 28 / 255, 30 / 255, 1),
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
            "actor_regular": "assets/fonts/Actor_Regular.ttf"
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
