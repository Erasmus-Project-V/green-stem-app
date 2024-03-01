import re

from kivy.network.urlrequest import UrlRequest
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window

import sys

from NavApp.custom_widgets.input_widget.input_widget import InputWidget

sys.path.append('/NavApp/custom_widgets')

Window.softinput_mode = "below_target"


class ForgotPasswordScreen(MDScreen):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phase = 1
        self.widgets = {}
        self.bottom_layout = None
        self.middle_layout = None
        self.top_layout = None
        self.active = None
        self.top_title = None
        self.top_desc = None
        self.bottom_helper = None
        self.postfix = {1: self.activate_mail_entry,
                        2: self.activate_mail_receipt,
                        3: self.activate_password_changer}
        self.content_data_ref = {1: "new_password", 2: "verified"}
        self.fetcher_methods = {1: self.get_check_send_email,
                                2: lambda: 1,
                                3: self.get_passwords
                                }
        self.content_data = {
            "new_password": None,
            "mail_ver": False
        }

    def get_check_send_email(self):
        email_text = self.active.return_text()
        if not re.match(".+@.+\..+", email_text):
            self.active.enter_error_mode("Email nije ispravno napisan!")
            return 0
        else:
            self.active.exit_error_mode()
        payload = {"email": email_text}
        # bypass za debug
        return 1
        UrlRequest(url="http://localhost:8090/api/collections/users/auth-with-password", req_body=payload,
                   on_success=lambda a, b: self.successful_mail_send(a, b),
                   on_error=lambda a, b: self.failed_mail_send(a, b))
        self.ids["bottom_button"].button_disabled = True
        return 0

    def successful_mail_send(self, a, b):
        self.ids["bottom_button"].button_disabled = False
        self.phase += 1
        self.activate_phase()

    def failed_mail_send(self, a, b):
        self.active.enter_error_mode("mail ne postoji u bazi!")
        self.ids["bottom_button"].button_disabled = False

    def build_pass_change_widget(self):
        rl = MDRelativeLayout()
        input_1 = InputWidget(
            placeholder_text="Upiši novu lozinku",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            is_password=True)
        input_2 = InputWidget(
            placeholder_text="Ponovi novu lozinku",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            is_password=True)
        rl.add_widget(input_1)
        rl.add_widget(input_2)
        self.passwords_temp = [input_1, input_2]
        return rl

    def get_passwords(self):
        p1 = self.passwords_temp[0]
        p2 = self.passwords_temp[1]
        p1_t = p1.return_text()
        p2_t = p2.return_text()
        if not 4 < len(p1_t) < 24:
            p1.enter_error_mode("password too short!")
            return 0
        elif p1_t != p2_t:
            p1.enter_error_mode("passwords dont match!")
            p2.enter_error_mode("passwords dont match!")
            return 0
        else:
            p1.exit_error_mode()
            p2.exit_error_mode()
        self.content_data[self.content_data_ref[1]] = p1_t
        return 1

    def start_up_screen(self):
        self.phase = 1
        self.middle_layout = self.ids["middle_layout"]
        self.top_layout = self.ids["top_layout"]
        self.bottom_layout = self.ids["bottom_layout"]
        self.top_title = self.ids["top_title"]
        self.top_desc = self.ids["top_desc"]
        self.bottom_helper = self.ids["bottom_helper_text"]
        self.widgets = \
            {1: InputWidget(
                placeholder_text="Upiši E-mail",
                is_checkbox=True

            ),
                2: MDLabel(text="Otvorite Link poslan na vaš \n E-mail račun",
                           pos_hint={"center_x": 0.5, "center_y": 0.75},
                           halign="center",
                           font=self.actor_font),
                3: self.build_pass_change_widget()
            }
        self.activate_phase()

    def activate_mail_receipt(self):
        self.hide_top_layout()
        self.active.font_size = 32
        self.ids["bottom_button"].button_text = "Odvedi meee"
        self.bottom_helper.text = "Pritisni kako bi upalio E-mail:"

    def activate_mail_entry(self):
        self.show_top_layout()
        self.ids["bottom_button"].button_text = "Pošalji"
        self.top_title.text = "Zaboravili ste lozinku?"
        self.top_desc.text = "Unesite svoju email adresu."
        self.bottom_helper.text = "Pošalji kod na moju adresu:"
        # self.ids["bottom_button"].disabled = True
        # neka metoda koja odvede na mail il nes idk

    def activate_password_changer(self):
        self.show_top_layout()
        self.ids["bottom_button"].button_text = "Potvrdi"
        self.top_title.text = "Promijeni lozinku"
        self.top_desc.text = "Unesite novu lozinku"
        self.bottom_helper.text = "Potvrdi novu lozinku:"

    def hide_top_layout(self):
        self.top_layout.opacity = 0.0

    def show_top_layout(self):
        self.top_layout.opacity = 1.0

    def activate_phase(self):
        if self.active:
            self.middle_layout.remove_widget(self.active)
            self.active = None
        if self.phase in self.widgets:
            self.active = self.widgets[self.phase]
            self.middle_layout.add_widget(self.active)
            self.postfix[self.phase]()
        else:
            self.finalize_forget_pass()

    def finalize_forget_pass(self):
        print(self.content_data)
        keys = list(self.widgets.keys())
        for i in keys:
            self.widgets[i].clear_widgets()
            del self.widgets[i]
        self.manager.goto_screen("lgn")

    def prev_phase(self, btn):
        if self.phase > 1:
            self.phase -= 1
            self.activate_phase()
        else:
            self.phase = 0
            self.activate_phase()
            self.manager.goto_screen("lgn")

    def next_phase(self, btn, dp=1):
        if not self.fetcher_methods[self.phase]():
            return
        # self.content_data[self.content_data_ref[self.phase]] = self.active.get_selected_value()
        self.phase += dp
        self.activate_phase()

    def return_to_signup(self, button):
        self.manager.goto_screen("sgn")

    def update_label(self, text):
        self.desc_text.text = str(text) + " kg"

    def enable_progression(self):
        self.progress_button.disabled = False

    def disable_progression(self):
        self.progress_button.disabled = True
