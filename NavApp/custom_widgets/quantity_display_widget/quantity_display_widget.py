from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty


class QuantityDisplayWidget(MDRelativeLayout):
    title = StringProperty("STEPS")
    quantity = StringProperty("1550")
    pass
