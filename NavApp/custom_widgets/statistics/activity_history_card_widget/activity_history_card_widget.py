from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.clock import Clock
from custom_widgets.statistics.oval_day_widget.oval_day_widget import OvalDayWidget
import calendar
from datetime import datetime


class ActivityHistoryCardWidget(MDRelativeLayout):
    img_path = StringProperty()
