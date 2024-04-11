import json

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.screen import MDScreen
from custom_widgets.authentication.gender_selector_widget.gender_selector_widget import GenderSelectorWidget
from custom_widgets.authentication.age_selector_widget.age_selector_widget import AgeSelectorWidget
from custom_widgets.authentication.weight_selector_widget.weight_selector_widget import WeightSelectorWidget
from custom_widgets.authentication.mail_verification_widget.mail_verification_widget import \
    MailVerificationWidget


class SecondSignUpScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phase = 1
        self.changeable = None
        self.selector = None
        self.desc_text = None
        self.progress_button = None
        self.side_label = None
        self.return_button = None
        self.active = None
        self.widgets = {}
        self.loaded_widgets = 5
        self.phase_ref = {1: self.activate_mail_verification,
                          2: self.activate_gender,
                          3: self.activate_selector,
                          4: self.start_weight,
                          5: self.activate_selector,
                          }
        self.content_data_ref = {1: "verified", 2: "gender", 3: "age", 4: "weight", 5: "height"}
        self.content_data = {
            "verified": None,
            "gender": None,
            "age": None,
            "weight": None,
            "height": None,
        }


    def initialize_widgets(self,dt):
        self.widgets = \
            {1: MailVerificationWidget(repeatable_method=self.mail_ping),
             2: None,  # gender selector
             3: None,  # age selector
             4: None,  # weight selector
             5: None,  # height selector
             }
        Clock.schedule_once(self.initialize_gww, 0)
        Clock.schedule_once(self.initialize_asw, 0.5)
        Clock.schedule_once(self.initialize_asw2, 1)
        Clock.schedule_once(self.initialize_waw, 2)

    def initialize_gww(self,dt=0):
        self.widgets[2] = GenderSelectorWidget(bindable=self.enable_progression)
        self.loaded_widgets += 1

    def initialize_asw(self,dt=0):
        self.widgets[3] = AgeSelectorWidget()
        self.loaded_widgets += 1

    def initialize_asw2(self,dt=0):
        self.widgets[5] = AgeSelectorWidget()
        self.widgets[5].re_argument(enumeration_min=100, button_num=120)
        self.loaded_widgets += 1

    def initialize_waw(self,dt=0):
        self.widgets[4] = WeightSelectorWidget()
        self.loaded_widgets += 1

    def start_repeatable_intervals(self):
        ## ovo se jako dugo učitava!
        ## mozda raspodijeliti?
        self.start_up()


    def mail_ping(self, dt):

        print(f"User id: {self.manager.active_user.get_user_id()}")
        self.manager.active_user.send_request(
            path=f"/api/collections/users/records/{self.manager.active_user.get_user_id()}",
            success_func=lambda a, b: self.successful_mail_verification(a, b),
            error_func=lambda a, b: self.error_sign_up(a, b),
        )

    def successful_mail_verification(self, thread, text):
        print("pingin\n", text)
        if text["verified"]:
            print("user verified \n\n!!!!!!")
            self.progress_button.button_disabled = False
            self.next_phase(None)

    def start_up(self, dt=0):
        # treba li resetirati na novom ulasku, ili da se vrati tamo gdje se stalo?
        self.phase = 1
        self.changeable = self.ids["changeable"]
        self.selector = self.ids["selector"]
        self.side_label = self.ids["side_text"]
        self.desc_text = self.ids["desc_text"]
        self.progress_button = self.ids["progress_button"]
        self.return_button = self.ids["rtb"]
        self.disable_progression()
        self.activate_current()

    def activate_current(self):
        if self.active:
            anim1 = Animation(opacity=0,duration=0.5)
            anim1.bind(on_complete=self.ac01)
            anim1.start(self.active)
        else:
            self.ac01()


    def ac01(self,*args):
        if self.active:
            self.active.stop_repeatable_intervals()
            self.changeable.remove_widget(self.active)
        anim2 = Animation(opacity=1,duration=0.5)
        if self.phase <= len(self.widgets):
            self.active = self.widgets[self.phase]
            self.active.opacity = 0
            self.changeable.add_widget(self.active)
            self.active.start_repeatable_intervals()
        self.phase_ref[self.phase]()
        anim2 = Animation(opacity=1,duration=0.5)
        anim2.start(self.active)

    def activate_mail_verification(self):
        self.return_button.opacity = 0.0
        self.selector.opacity = 0.0
        self.desc_text.opacity = 0.0
        self.side_label.opacity = 0.0

    def activate_selector(self):
        self.selector.opacity = 1.0
        self.desc_text.opacity = 0.0
        self.side_label.opacity = 1.0
        self.side_label.text = "cm" if self.phase == 5 else "Age"
        self.return_button.opacity = 1.0

    def activate_gender(self):
        self.return_button.opacity = 0.0
        self.selector.opacity = 0.0
        self.desc_text.opacity = 0.0
        self.side_label.opacity = 0.0

    def start_weight(self):
        self.desc_text.opacity = 1.0
        self.side_label.opacity = 0.0
        self.desc_text.text = "Weight (kg)"
        self.selector.opacity = 0.0
        self.widgets[self.phase].bind_to_scroll(self.update_label)

    def finalize_sign_up(self):
        keys = list(self.widgets.keys())
        for i in keys:
            self.widgets[i].clear_widgets()
            del self.widgets[i]

    def send_second_batch(self, payload):
        print(self.manager.active_user.user_token)
        self.manager.active_user.overwrite_user_data(payload)
        self.manager.active_user.send_request(
            path=f"/api/collections/users/records/{self.manager.active_user.get_user_id()}",
            method="PATCH",
            body=json.dumps(payload),
            success_func=lambda a, b: self.successful_sign_up(a, b),
            error_func=lambda a, b: self.error_sign_up(a, b)
        )

    def successful_sign_up(self, thread, text):
        print(text)
        self.manager.active_user.save_user_data()
        self.progress_button.button_disabled = False
        self.finalize_sign_up()
        self.manager.goto_screen("hme")

    def error_sign_up(self, thread, text):
        print(text)
        self.progress_button.button_disabled = False

    def prev_phase(self, btn):
        if self.phase > 1:
            self.next_phase(btn, dp=-1)

    def next_phase(self, btn, dp=1):
        self.content_data[self.content_data_ref[self.phase]] = self.active.get_selected_value()
        if self.phase >= len(self.content_data):
            self.progress_button.button_disabled = True
            self.send_second_batch(self.content_data)
            return
        self.phase += dp
        self.activate_current()

    def return_to_signup(self, button):
        self.manager.goto_screen("sgn")

    def update_label(self, text):
        self.desc_text.text = str(text) + " kg"

    def enable_progression(self):
        self.progress_button.disabled = False

    def disable_progression(self):
        self.progress_button.disabled = True
