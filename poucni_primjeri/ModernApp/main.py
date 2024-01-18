from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from cw.image_button import ImageButton

Window.size = (720 // 2, 1560 // 2)


class OverlayScreenManager(ScreenManager):
    pass


class FirstScreen(MDScreen):

    def cookie_clicked(self):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")


class SuperModernApp(MDApp):

    def build(self):
        return Builder.load_file("core.kv")


App = SuperModernApp()
App.run()
