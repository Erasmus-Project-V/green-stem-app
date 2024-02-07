from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from NavApp.custom_widgets.authentication.gender_selector_widget.gender_selector_widget import GenderSelectorWidget
from NavApp.custom_widgets.authentication.age_selector_widget.age_selector_widget import AgeSelectorWidget
from NavApp.custom_widgets.authentication.weight_selector_widget.weight_selector_widget import WeightSelectorWidget


class SecondSignUpScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phase = 1
        self.changeable = None
        self.selector = None
        self.desc_text = None
        self.widgets = {}
        self.phase_ref = {1: self.start_up, 2: self.start_age, 3: self.start_weight, 4: self.start_height}
        self.content_data = {
            "gender":None,
            "age": None,
            "weight": None,
            "height": None,
        }

    def start_up(self, dt=0):
        self.changeable = self.ids["changeable"]
        self.changeable.add_widget(self.widgets["gsw"])
        self.selector = self.ids["selector"]
        self.desc_text = self.ids["desc_text"]
        self.selector.opacity = 0.0
        self.desc_text.opacity = 0.0

    def start_age(self):
        self.selector.opacity = 1.0
        self.desc_text.opacity = 0.0
        self.content_data["gender"] = self.widgets["gsw"].get_selected()
        self.changeable.remove_widget(self.widgets["gsw"])
        self.changeable.add_widget(self.widgets["asw"])
        self.widgets["asw"].start_repeatable_intervals()

    def return_to_signup(self, button):
        self.manager.goto_screen("sgn")

    def start_repeatable_intervals(self):
        ## ovo se jako dugo učitava!
        ## mozda raspodijeliti?
        self.widgets = \
            {"gsw": GenderSelectorWidget(),
             "asw": AgeSelectorWidget(),
             "wsw": WeightSelectorWidget(),
             "hsw": AgeSelectorWidget()}
        self.widgets["hsw"].re_argument(enumeration_min=35, button_num=90)
        self.start_up()

    def update_label(self, text):
        self.desc_text.text = str(text) + " kg"

    def start_weight(self):
        self.desc_text.opacity = 1.0
        self.desc_text.text = "Weight (kg)"
        self.selector.opacity = 0.0
        self.content_data["age"] = self.widgets["asw"].get_selected_value()
        self.changeable.remove_widget(self.widgets["asw"])
        self.changeable.add_widget(self.widgets["wsw"])
        self.widgets["asw"].stop_repeatable_intervals()
        self.widgets["wsw"].start_repeatable_intervals()
        self.widgets["wsw"].bind_to_scroll(self.update_label)

    def start_height(self):
        self.desc_text.opacity = 0.0
        self.selector.opacity = 1.0
        self.content_data["weight"] = self.widgets["wsw"].get_selected_value()
        self.changeable.remove_widget(self.widgets["wsw"])
        self.changeable.add_widget(self.widgets["hsw"])
        self.widgets["wsw"].stop_repeatable_intervals()
        self.widgets["hsw"].start_repeatable_intervals()

    def next_phase(self, btn):
        self.phase += 1
        print("rephasing")
        if self.phase in self.phase_ref:
            self.phase_ref[self.phase]()
        elif self.phase > 4:
            self.widgets["hsw"].stop_repeatable_intervals()
            self.content_data["height"] = self.widgets["hsw"].get_selected_value()
            print(self.content_data)
            for i in self.widgets.values():
                del i
