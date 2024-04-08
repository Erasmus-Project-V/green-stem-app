from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout


class ActivityHistoryCardWidget(MDRelativeLayout):
    img_path = StringProperty()
    activity_data = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def activity_card_pressed(self):
        print("The activity card was pressed")