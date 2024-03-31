from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout


class ActivityHistoryCardWidget(MDRelativeLayout):
    img_path = StringProperty()

    def activity_card_pressed(self):
        print("The activity card was pressed")