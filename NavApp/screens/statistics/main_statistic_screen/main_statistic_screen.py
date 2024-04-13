import datetime
import time

from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from custom_widgets.statistics.calendar_widget.calendar_widget import CalendarWidget
from custom_widgets.statistics.activity_history_list_widget.activity_history_list_widget import \
    ActivityHistoryListWidget
from custom_widgets.statistics.activity_history_card_widget.activity_history_card_widget import \
    ActivityHistoryCardWidget
from kivy.utils import platform
from kivy.metrics import dp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSlideTransition, MDFadeSlideTransition
from custom_widgets.activity_grid_widget.activity_grid_widget import ActivityGridWidget

from NavApp.custom_widgets.miscellaneous.dialog_widget.dialog_widget import DialogWidget


class MainStatisticScreen(MDScreen):
    image_root = "assets/images/home/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialized = False
        self.connected = False
        self.current_layout = None
        self.current_layout_name = "week"
        self.hero_activity_presets = [{"text": "Running", "img_path": f"{self.image_root}home_trcanje_1.png",
                                       "hero_tag": "running_card", "release_func": self.transit_hero},
                                      {"text": "Cycling", "img_path": f"{self.image_root}home_bicikliranje_1.png",
                                       "hero_tag": "cycling_card", "release_func": self.transit_hero},
                                      {"text": "Hiking", "img_path": f"{self.image_root}home_planinarenje_1.png",
                                       "hero_tag": "hiking_card", "release_func": self.transit_hero},
                                      {"text": "Walking", "img_path": f"{self.image_root}home_hodanje_1.png",
                                       "hero_tag": "walking_card", "release_func": self.transit_hero},
                                      {"text": "Skating", "img_path": f"{self.image_root}home_rolanje_1.png",
                                       "hero_tag": "skating_card", "release_func": self.transit_hero}]

        self.ref_nav = {"Chosen day": "day", "This week": "week_month", "This month": "week_month"}
        self.layouts = {
            "day": self.init_chosen_day(),
            "week_month": ActivityGridWidget(activity_grid_elements=self.hero_activity_presets),
        }

        self.build_references = {
            "day": self.build_chosen_day,
            "week_month": self.build_hero_panels
        }

        self.active_layout = None
        self.changeable_widget = None

        Clock.schedule_once(self.futher_build, 0.1)

    def futher_build(self, dt):
        self.daily_screen = self.manager.get_screen("das")
        self.monthly_screen = self.manager.get_screen("mas")
        self.weekly_screen = self.manager.get_screen("was")
        self.user = self.manager.active_user
        self.changeable_widget = self.ids["changeable"]

    def fetch_this_week_online(self, *args, activity_name='trcanje'):
        print("this week is being fetched online")
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        print(week_ago)
        print(activity_name)

        self.user.send_request(f"/api/collections/exercises/records?filter=(type%3D%27{activity_name}%27%20%26%26%20created%3E%27{week_ago}%27)", method="GET"
                               , success_func=self.successful_fetch, error_func=self.failed_fetch)

    def fetch_this_day_online(self,*args,current_date = None):
        if not current_date:
            current_date = str(datetime.date.today())
        next_date = datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        next_date = str(next_date).split(" ")[0]
        self.user.send_request(f"/api/collections/exercises/records?filter=(created>='{current_date}'%20%26%26%20created<='{next_date}')", method="GET"
                               , success_func=self.successful_fetch, error_func=self.failed_fetch)

    def fetch_this_month_online(self,activity_name='trcanje'):
        current_date = datetime.date.today()
        m1 = str(current_date)[:-2] + "01"
        self.user.send_request(f"/api/collections/exercises/records?filter=(type%3D'{activity_name}'%20%26%26%20created%3E%3D'{m1}')", method="GET"
                               , success_func=self.successful_fetch, error_func=self.failed_fetch)

    def fetch_this_week_offline(self):
        pass

    def fetch_this_day_offline(self):
        pass

    def fetch_this_month_offline(self):
        pass

    def successful_fetch(self, message, body):
        print(body)
        self.exercises = body['items']
        self.n_exercises = body['totalItems']
        if self.current_layout_name != "day":
            cs = self.weekly_screen
            cs.receive_activity_data(self.exercises,self.n_exercises)
        else:
            if self.n_exercises == 0:
                print("no activities for current day")
                return
            x = self.active_layout.children[0]
            x.clear_activity_cards()
            x.receive_activity_data(self.exercises,self.n_exercises,self.goto_das)

    def failed_fetch(self, a, b):
        print(b)
        self.no_connection_dialog = DialogWidget(title="No connection or server down",
                                                 text=str(b),buttons=[MDFlatButton(
            text="Dismiss",
            theme_text_color="Custom",
            text_color=self.blue_ref,
            on_release=self.close_dialog_and_retry

        ),])
        self.no_connection_dialog.open()

    def close_dialog_and_retry(self,*args):
        self.no_connection_dialog.dismiss()


    def check_for_connection(self):
        if not self.user.check_for_wifi(0):
            print("user is connected to the internet! - uploading any leftovers...")
            return True
        else:
            print("user is offline, showing limited data")
            return False

    def start_up_screen(self):
        if self.initialized:
            return
        self.destroy_old_layout()
        if platform == "android":
            self.connected = self.check_for_connection()
        else:
            self.connected = True
        self.manager.tamper_hero_data(self.layouts["week_month"])
        self.build_hero_panels()
        self.initialized = True

    def init_chosen_day(self):
        tm = datetime.date.today()
        mdict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                 9: "September", 10: "October", 11: "November", 12: "December"}
        rl = MDRelativeLayout()
        calendar_widget = CalendarWidget(current_month=mdict[tm.month], current_year=str(tm.year),
                                         current_date=str(tm.day))
        calendar_widget.fetcher_ref = self.fetch_this_day_online
        calendar_widget.pos_hint = {"center_x": 0.5, "center_y": 0.81}
        rl.add_widget(calendar_widget)

        history_widget = ActivityHistoryListWidget()
        calendar_widget.set_container_ref(history_widget)
        history_widget.pos_hint = {"center_x": 0.5, "center_y": 0.45}
        history_widget.activity_history_elements = []
        rl.add_widget(history_widget)
        return rl

    def destroy_old_layout(self):
        if self.active_layout and self.initialized:
            anim = Animation(opacity=0, duration=0.5)
            anim.bind(on_complete=self.finish_destruction)
            anim.start(self.active_layout)
        elif self.active_layout:
            self.finish_destruction()

    def finish_destruction(self, *args):
        self.changeable_widget.remove_widget(self.active_layout)
        self.active_layout = None
        if self.current_layout:
            self.build_references[self.current_layout]()
            anim = Animation(opacity=1, duration=0.5)
            anim.start(self.active_layout)

    def change_state(self, btn):
        self.current_layout_name = btn.name.split(" ")[-1]
        self.current_layout = self.ref_nav[btn.name]
        self.destroy_old_layout()

    def placeholder(self, *args):
        pass

    def _transit_hero(self, *args):
        hero_tag = self.current_hero_tag
        self.manager.transition = MDSlideTransition()
        self.manager.current_heroes = [hero_tag]
        was = self.manager.get_screen("was")
        was.start_up_screen(self.current_hero_tag, self.current_activity_type)
        # goto screen doesnt work
        self.manager.current = "was"


    def transit_hero(self, btn):
        actdict = {"Running":"trcanje","Walking":"hodanje","Cycling":"bicikliranje","Skating":"rolanje","Hiking":"planinarenje"}
        if self.connected:
            if self.current_layout_name == "week":
                self.fetch_this_week_online(activity_name=actdict[btn.activity_type])
            else:
                self.fetch_this_month_online(activity_name=actdict[btn.activity_type])
        else:
            self.fetch_this_week_offline()
        self.current_hero_tag = btn.hero_tag
        self.current_activity_type = btn.activity_type
        x = self.active_layout.nav_ref[btn.hero_tag].ids.front_box
        anim = Animation(opacity=0, duration=0.2)
        anim.bind(on_complete=self._transit_hero)
        anim.start(x)

    def reenter_hero(self, *args):
        anim = Animation(opacity=1, duration=0.2)
        anim.start(self.active_layout.nav_ref[self.current_hero_tag].ids.front_box)
        self.unbind(on_enter=self.reenter_hero)

    def build_hero_panels(self):
        self.active_layout = self.layouts["week_month"]
        self.changeable_widget.add_widget(self.active_layout)
        self.changeable_widget.manager = self.manager

    def build_chosen_day(self):
        self.fetch_this_day_online()
        changeable = self.ids["changeable"]
        self.rectangle_radius = [20, 20, 0, 0]
        self.rectangle_height = dp(200)
        self.active_layout = self.layouts["day"]
        changeable.add_widget(self.active_layout)

    def goto_das(self, activity_name="None", time=0, activity_data=None):
        das = self.manager.get_screen("das")
        das.start_up_screen(activity_name, time,activity_data)
        self.manager.current = "das"
