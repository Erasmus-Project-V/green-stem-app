from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.relativelayout import MDRelativeLayout
import webbrowser


class MailVerificationWidget(MDRelativeLayout):
    event = None
    repeatable_method = None

    def __init__(self, *args, **kwargs):

        super().__init__()
        if "repeatable_method" in kwargs:
            self.repeatable_method = kwargs["repeatable_method"]

    def start_repeatable_intervals(self, *args):
        self.event = Clock.schedule_interval(self.repeatable_method,2)

    def mail_ping(self,dt):
        pass

    def get_selected_value(self):
        return True

    def stop_repeatable_intervals(self, *args):
        self.event.cancel()

    def send_to_email(self, *args):
        webbrowser.open("mailto:")
