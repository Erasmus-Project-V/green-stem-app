from kivy.clock import Clock
from kivy.properties import ListProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from custom_widgets.statistics.friend_card_widget.friend_card_widget import \
    FriendCardWidget


class FriendStatListWidget(MDRelativeLayout):
    friend_activities = ListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.build_self, 0)

    def build_self(self, clc):
        scrollable_column = self.ids["scrollable_activities"]

        for activity in self.friend_activities:
            print("add activity", activity)
            friend_card = FriendCardWidget()
            friend_card.quantity_one = activity["quantity_one"]
            friend_card.quantity_two = activity["quantity_two"]
            friend_card.friend_name = activity["friend_name"]
            scrollable_column.add_widget(friend_card)

        if len(self.friend_activities) <= 1:
            scroll_view = self.ids["scroll_view"]
            scroll_view.do_scroll_y = False