import kivymd.uix.transition
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from custom_widgets.streamlined_widgets import TopMenu
from custom_widgets.image_button import ImageButton
from kivymd.icon_definitions import md_icons

print(md_icons)

Window.size = (720 / 2, 1560 / 2)


class ScreenOne(MDScreen):
    pass


class ScreenTwo(MDScreen):
    pass


class MGAScreenManager(MDScreenManager):
    pass


Builder.load_file("streamlined_widgets.kv")


class ModernMLGraphingApp(MDApp):

    def build(self):
        return Builder.load_file("core.kv")


A = ModernMLGraphingApp()
A.run()
