from kivymd.uix.label import MDLabel


class OvalBlueButtonWidget(MDLabel):
    def on_click(self):
        print("button has been clicked")