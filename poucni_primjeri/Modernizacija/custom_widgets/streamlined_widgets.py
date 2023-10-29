from kivymd.uix.relativelayout import MDRelativeLayout


class TopMenu(MDRelativeLayout):
    DefaultText = "Data Projector"

    def go_home(self):
        cur = self.parent
        manager = None
        while not cur.parent == cur:
            manager = cur
            cur = cur.parent
        manager.current = "startScreen"


class Grapher(MDRelativeLayout):
    pass