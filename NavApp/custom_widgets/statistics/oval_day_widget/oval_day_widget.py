from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from custom_widgets.activity_card_widget.activity_card_widget import ActivityCardWidget
from kivymd.color_definitions import colors


class OvalDayWidget(MDRelativeLayout):
    def pressed(self, btn):
        print("The initial callback func")