import json
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
                        2: self.activate_mail_receipt}
        self.content_data_ref = {1: "new_password", 2: "verified"}
        self.fetcher_methods = {1: self.get_check_send_email,
                                2: lambda: 1,
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


    def successful_mail_send(self, thread, response_text):
        print(f"Mail send success: {response_text}")
        self.ids["bottom_button"].button_disabled = False
        self.phase += 1
        self.activate_phase()

    def failed_mail_send(self, thread, response_text):
        print(f"Mail send failed: {response_text}")
        self.active.enter_error_mode("mail ne postoji u bazi!")
        self.ids["bottom_button"].button_disabled = False



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
            }
        self.activate_phase()

    def activate_mail_receipt(self):
        self.hide_top_layout()
        self.active.font_size = 32
        self.ids["bottom_button"].button_text = "Odvedi me"
        self.bottom_helper.text = "Pritisni kako bi upalio E-mail:"

    def activate_mail_entry(self):
        self.show_top_layout()
        self.ids["bottom_button"].button_text = "Pošalji"
        self.top_title.text = "Zaboravili ste lozinku?"
        self.top_desc.text = "Unesite svoju email adresu."
        self.bottom_helper.text = "Pošalji kod na moju adresu:"




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
        self.phase += dp
        self.activate_phase()

    def update_label(self, text):
        self.desc_text.text = str(text) + " kg"

    def enable_progression(self):
        self.progress_button.disabled = False

    def disable_progression(self):
        self.progress_button.disabled = True
