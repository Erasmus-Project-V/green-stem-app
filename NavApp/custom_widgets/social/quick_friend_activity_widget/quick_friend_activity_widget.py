from kivymd.uix.relativelayout import MDRelativeLayout


class QuickFriendActivityWidget(MDRelativeLayout):
    def change_heart_color(self):
        heart = self.ids["heart_icon"]
        if heart.source[22:] == "Heart_empty.png":
            heart.source = "assets/images/sprites/Heart_full.png"
        else:
            heart.source = "assets/images/sprites/Heart_empty.png"
