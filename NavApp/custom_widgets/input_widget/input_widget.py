from kivymd.uix.label import MDLabel
from kivy.uix.button import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty

class InputWidget(ButtonBehavior, MDLabel):
    place_holder_text = StringProperty("Type here")
    is_password = BooleanProperty(False)

