from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty


class QuantityDisplayWidget(MDRelativeLayout):
    title = StringProperty("NULL")
    quantity = StringProperty("NULL")


