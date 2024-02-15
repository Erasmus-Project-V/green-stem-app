from kivymd.uix.screen import MDScreen
from custom_widgets.authentication.gender_selector_widget.gender_selector_widget import GenderSelectorWidget
from custom_widgets.authentication.age_selector_widget.age_selector_widget import AgeSelectorWidget
from custom_widgets.authentication.weight_selector_widget.weight_selector_widget import WeightSelectorWidget


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
        self.phase_ref = {1: self.activate_gender,
                          2: self.activate_selector,
                          3: self.start_weight,
                          4: self.activate_selector,
                          5: self.finalize_sign_up}
        self.content_data_ref = {1: "gender", 2: "age", 3: "weight", 4: "height"}
        self.content_data = {
            "gender": None,
            "age": None,
            "weight": None,
            "height": None,
        }

    def start_repeatable_intervals(self):
        ## ovo se jako dugo učitava!
        ## mozda raspodijeliti?
        self.widgets = \
            {1: GenderSelectorWidget(bindable=self.enable_progression),  # gender selector
             2: AgeSelectorWidget(),  # age selector
             3: WeightSelectorWidget(),  # weight selector
             4: AgeSelectorWidget()}  # height selector
        self.widgets[4].re_argument(enumeration_min=100, button_num=120)
        self.start_up()

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
            self.active.stop_repeatable_intervals()
            self.changeable.remove_widget(self.active)
        if self.phase < 5:
            self.active = self.widgets[self.phase]
            self.changeable.add_widget(self.active)
            self.active.start_repeatable_intervals()
        self.phase_ref[self.phase]()

    def activate_selector(self):
        self.selector.opacity = 1.0
        self.desc_text.opacity = 0.0
        self.side_label.opacity = 1.0
        self.side_label.text = "cm" if self.phase == 4 else "Age"
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
        print(self.content_data)
        keys = list(self.widgets.keys())
        for i in keys:
            self.widgets[i].clear_widgets()
            del self.widgets[i]
        self.manager.goto_screen("hme")


    def prev_phase(self, btn):
        if self.phase > 1:
            self.next_phase(btn, dp=-1)

    def next_phase(self, btn, dp=1):

        self.content_data[self.content_data_ref[self.phase]] = self.active.get_selected_value()
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
