# file name: hello2.py
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Label
from kivy.uix.widget import Widget

# KADA ŽELIMO NEKI FRAME KREIRATI NA WINDOW; MORA BITI REFERENCIRAM IMENOM
# NE ŽELIMO KORISTITI BASE KLASE: JER DCE NAM MOZA OPET TREBATI
class EncapsulatingBoxLayout(BoxLayout):
    orientation = "vertical"

    def button_clicked(self):
        self.orientation="horizontal" if self.orientation=="vertical" else "vertical"
        print("clicked")
        self.canvas.ask_update()
        print(self.orientation)
        self.do_layout()

# AKO NE KORISTIMO BUILDER; NAZIV KV I APP INSTANCE MORA BITI JEDNAK!!!!
#PROBAJ PREBACITI U FLOAT LAYOUT SA POD HINTS i SIZE HINTS
class main_app(App):

     def build(self):
         E=  EncapsulatingBoxLayout()
         E.orientation = "horizontal" #or vertical
         return E
if __name__=="__main__":
     main_app().run()