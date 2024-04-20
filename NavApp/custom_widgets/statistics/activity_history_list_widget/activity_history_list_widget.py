from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import ListProperty
from kivy.clock import Clock
from custom_widgets.statistics.activity_history_card_widget.activity_history_card_widget import \
    ActivityHistoryCardWidget


class ActivityHistoryListWidget(MDRelativeLayout):
    activity_history_elements = ListProperty()
    img_root = "assets/images/home/home_*_1.png"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activity_cards = []
        self.filled = False


        Clock.schedule_once(self.build_self, 0)

    def build_self(self, clc):
        self.scrollable_column = self.ids["scrollable_activities"]
        self.add_activity_cards()
        self.filled = True

    def receive_activity_data(self, items, n_items,acfunc):
        if self.filled:
            return False
        widget_instructions = []
        for i in range(len(items)):
            dct = {"img_path":self.img_root.replace("*",items[i]["type"]),
                   "activity_name":items[i]["type"],
                   "activity_time":items[i]["time_started"].split(" ")[-1][:8],
                   "card_function": acfunc,
                   "other": items[i]
                   }
            widget_instructions.append(dct)
        self.activity_history_elements = widget_instructions
        self.add_activity_cards()
        self.filled =True

    def add_activity_cards(self):
        # if len(self.activity_history_elements) == 0:
        #     self.activity_cards.clear()
        #     self.scrollable_column.clear_widgets()
        #     return

        for activity in self.activity_history_elements:
            history_card = ActivityHistoryCardWidget()
            history_card.img_path = activity["img_path"]
            history_card.activity_name = activity["activity_name"]
            history_card.activity_time = activity["activity_time"]
            history_card.activity_card_function = activity["card_function"]
            history_card.activity_data = activity["other"]
            self.scrollable_column.add_widget(history_card)
            self.activity_cards.append(history_card)

        if len(self.activity_history_elements) <= 5:
            scroll_view = self.ids["scroll_view"]
            scroll_view.do_scroll_y = False

    def clear_activity_cards(self):
        for x in self.activity_cards:
            self.scrollable_column.remove_widget(x)
        self.activity_cards = []
        self.activity_history_elements = []
        scroll_view = self.ids["scroll_view"]
        scroll_view.do_scroll_y = False
        self.filled = False