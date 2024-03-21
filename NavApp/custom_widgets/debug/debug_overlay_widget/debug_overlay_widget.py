from kivymd.uix.relativelayout import MDRelativeLayout


class DebugOverlayWidget(MDRelativeLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def bind_callback(self, instance, value):
        self.debug_text_var = self.ids["debug_text"]
        self.debug_text_var.text = value

    def get_bind_callback(self):
        return self.bind_callback
