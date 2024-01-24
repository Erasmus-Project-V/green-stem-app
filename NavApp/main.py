from kivy import Config


Config.set('graphics', 'width', '390')
Config.set('graphics', 'height', '780')

from scripts.imports import *

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
        self.screen_refs = {i: self.screen_names[i] for i in range(len(self.screen_names))}
        self.window_subroutines()

    def window_subroutines(self):
        Window.bind(on_key_down=self.key_pressed)

    def key_pressed(self, *args):
        key = args[-2]
        print(f"pressed {key}")
        if key in map(str, self.screen_refs.keys()):
            self.goto_screen(self.screen_refs[int(key)])

    def goto_screen(self, scrn):
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
            "green": (103 / 255, 201 / 255, 95 / 255, 1),
            "orange": (231 / 255, 100 / 255, 27 / 255, 1)
        }
        self.fonts = {
            "sans_semi_bold": "assets/fonts/OpenSans_SemiBold.ttf",
            "sans_regular": "assets/fonts/OpenSans_Regular.ttf"
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
