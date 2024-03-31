from kivymd.uix.relativelayout import MDRelativeLayout


class OvalDayWidget(MDRelativeLayout):
    def pressed(self, btn):
        print("The initial callback func")