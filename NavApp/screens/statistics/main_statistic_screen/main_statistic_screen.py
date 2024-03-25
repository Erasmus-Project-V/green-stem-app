from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from custom_widgets.statistics.calendar_widget.calendar_widget import CalendarWidget
from custom_widgets.statistics.activity_history_card_widget.activity_history_card_widget import ActivityHistoryCardWidget
from kivy.metrics import dp


class MainStatisticScreen(MDScreen):
    def this_clicked(self, btn):
        print(btn.tag)
        self.manager.transition.direction = "left"
        print(self.manager.current_heroes)
        self.manager.current_heroes = ["hero1"]
        self.manager.current = "was"

    def chosen_day_pressed(self, btn):
        changeable = self.ids["changeable"]
        self.clean_children()
        self.rectangle_radius = [20, 20, 0, 0]
        self.rectangle_height = dp(200)
        calendar_widget = CalendarWidget(current_month="January", current_year="2024")
        calendar_widget.pos_hint = {"center_x":0.5,"center_y":0.81}
        changeable.add_widget(calendar_widget)

        # history_widget = ActivityHistoryCardWidget()
        # history_widget.pos_hint = {"center_x":0.5,"center_y":0.7}
        # changeable.add_widget(history_widget)

    def clean_children(self):
        changeable = self.ids["changeable"]
        children = changeable.children
        for child in children:
            changeable.remove_widget(child)

    def arrow_press(self, btn):
        print("Left arrow pressed")

