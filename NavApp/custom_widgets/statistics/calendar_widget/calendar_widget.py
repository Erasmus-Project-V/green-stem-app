from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.clock import Clock
from custom_widgets.statistics.oval_day_widget.oval_day_widget import OvalDayWidget
import calendar
from datetime import datetime


class CalendarWidget(MDRelativeLayout):
    current_month = StringProperty()
    current_year = StringProperty()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.build_self, 0)

    def build_self(self, dt=None):
        scrollable_row = self.ids["scrollable_days"]
        month_year = self.ids["month_year"]
        month_year.text = f"{self.current_month} {self.current_year}"

        days_in_month = self.get_days_in_month(int(self.current_year), self.current_month)
        for day in days_in_month:
            day_widget = OvalDayWidget()
            day_widget.day_in_week = day[0][0]
            day_widget.date = str(day[1])
            day_widget.id = str(day[1])
            day_widget.release_func = self.date_pressed
            scrollable_row.add_widget(day_widget)

    def get_days_in_month(self, year, month_name):
        # Get the month number from its name
        month_number = self.months.index(month_name.capitalize()) +1
        # Get the number of days in the month
        num_days = calendar.monthrange(year, month_number)[1]
        # Generate the dates for each day in the month
        days = []
        for day in range(1, num_days + 1):
            date = datetime(year, month_number, day)
            day_name = date.strftime("%A")  # Get the day name (Monday, Tuesday, etc.)
            days.append((day_name, day))
        return days

    def arrow_pressed(self, btn):
        curr_month_index = self.months.index(self.current_month)
        if btn == self.ids["previous_month"]:
            if curr_month_index != 0:
                self.current_month = self.months[curr_month_index - 1]
            else:
                self.current_month = self.months[-1]
                self.current_year = str(int(self.current_year) - 1)

        if btn == self.ids["next_month"]:
            if curr_month_index != 11:
                self.current_month = self.months[curr_month_index + 1]
            else:
                self.current_month = self.months[0]
                self.current_year = str(int(self.current_year) + 1)
        self.remove_dates_of_prev_month()
        self.build_self()

    def remove_dates_of_prev_month(self):
        scrollable_row = self.ids["scrollable_days"]
        children = scrollable_row.children
        for child in reversed(children):
            scrollable_row.remove_widget(child)

    def date_pressed(self, date):
        scrollable_row = self.ids["scrollable_days"]
        children = scrollable_row.children
        for child in children:
            child.day_color = self.dark_gray_container
            if child.date == date:
                child.day_color = self.blue_container

