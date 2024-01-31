from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout


class TopReturnButtonWidget(MDRelativeLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def placeholder(self,button):
        print("please implement return function!")
