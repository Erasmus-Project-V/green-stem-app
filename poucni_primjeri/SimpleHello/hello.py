# file name: hello2.py
from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.widget import Widget

# KADA ŽELIMO NEKI FRAME KREIRATI NA WINDOW; MORA BITI REFERENCIRAN IMENOM
# NE ŽELIMO KORISTITI BASE KLASE: JER DCE NAM MOZA OPET TREBATI
class SvenMatic(Widget):
    pass

# AKO NE KORISTIMO BUILDER; NAZIV KV I APP INSTANCE MORA BITI JEDNAK!!!!
class main_app(App):

     def build(self):
         return SvenMatic()

if __name__=="__main__":
     main_app().run()