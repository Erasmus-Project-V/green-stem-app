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
        scrollable_column = self.ids["scrollable_activities"]

        for activity in self.activity_history_elements:
            history_card = ActivityHistoryCardWidget()
            history_card.img_path = activity["img_path"]
            history_card.activity_name = activity["activity_name"]
            history_card.activity_time = activity["activity_time"]
            history_card.activity_card_function = activity["card_function"]
            scrollable_column.add_widget(history_card)

        if len(self.activity_history_elements) <= 5:
            scroll_view = self.ids["scroll_view"]
            scroll_view.do_scroll_y = False
