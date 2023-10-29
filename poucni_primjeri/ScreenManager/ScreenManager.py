# file name: hello2.py
from kivymd.app import MDApp
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager
### IAKO JE POTAMNJEN, VAŽNO JE IMPORTATI OVAJ FILE
from screens import ComicCreator


class MetaUser:
    def __init__(self):
        self.color = (255, 255, 255, 255)

    def getColor(self):
        return self.color

    def setColor(self, color: tuple):
        assert color.__class__ == tuple
        self.color = color


# KADA ŽELIMO NEKI FRAME KREIRATI NA WINDOW; MORA BITI REFERENCIRAM IMENOM
# NE ŽELIMO KORISTITI BASE KLASE: JER DCE NAM MOZA OPET TREBATI
class ComicScreenManager(ScreenManager):
    def callup(self):
        print("called")
        screenOne = self.get_screen("comicscreen")
        screenOne.ids["textlabel"].color = self.ids["_color_picker"].color


Builder.load_file("comiccreator.kv")
Builder.load_file("colorpicker.kv")


# AKO NE KORISTIMO BUILDER; NAZIV KV I APP INSTANCE MORA BITI JEDNAK!!!!
# PROBAJ PREBACITI U FLOAT LAYOUT SA POD HINTS i SIZE HINTS
class ms_app(MDApp):

    def build(self):
        return ComicScreenManager()


if __name__ == "__main__":
    U = MetaUser()
    ms_app().run()
