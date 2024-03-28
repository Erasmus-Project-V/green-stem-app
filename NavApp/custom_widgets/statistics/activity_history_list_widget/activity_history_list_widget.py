from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import ListProperty
from kivy.clock import Clock
from custom_widgets.statistics.activity_history_card_widget.activity_history_card_widget import \
    ActivityHistoryCardWidget

class ActivityHistoryListWidget(MDRelativeLayout):
    activity_history_elements = ListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.build_self, 0)

    def build_self(self, clc):
        for activity in self.activity_history_elements:
            pass