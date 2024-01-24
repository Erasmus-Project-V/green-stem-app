from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout


class OvalBlueButtonWidget(MDRelativeLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("binit")
        self.md_bg_color = (1, 1, 1, 1)

    def clicked(self,button):
        print("please implement custom press command!")