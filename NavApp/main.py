from scripts.imports import *
# bilo bi najbolje ovo sve strpat u poseban import file il nes


Window.size = (720 // 2, 1560 // 2)


class MainScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.screen_names)
        self.current = "lgn"
        self.screen_refs = {i + 1: self.screen_names[i] for i in range(len(self.screen_names))}
        Window.bind(on_key_down=self.key_pressed)

    def key_pressed(self, *args):
        key = args[-2]
        print(f"pressed {key}")
        if key in map(str, self.screen_refs.keys()):
            self.current = self.screen_refs[int(key)]


class FitnessApp(MDApp):

    def build(self):
        return MainScreenManager()


load_list = ["/authentication/sign_up_screen/sign_up_screen.kv",
             "/authentication/log_in_screen/log_in_screen.kv",
             "/activity/home_screen/home_screen.kv",
             "/activity/activity_screen/activity_screen.kv"]

for fname in load_list:
    Builder.load_file(f"screens{fname}")

Builder.load_file("core.kv")

if __name__ == "__main__":
    App = FitnessApp()
    App.run()
