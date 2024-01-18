from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.graphics import Point, Canvas, Ellipse, Color


class TopMenu(MDRelativeLayout):
    DefaultText = "Data Projector"

    def go_home(self):
        cur = self.parent
        manager = None
        while not cur.parent == cur:
            manager = cur
            cur = cur.parent
        manager.current = "startScreen"


class ColorPick(MDBoxLayout):
    current_color = StringProperty("red")
    current_ind = 0
    color_list = ["red", "orange", "brown", "blue", "yellow"]

    def change_color(self):
        if self.current_ind >= len(self.color_list) - 1:
            self.current_ind = 0
        else:
            self.current_ind += 1
        self.current_color = self.color_list[self.current_ind]


class Grapher(MDRelativeLayout):

    def on_touch_up(self, touch):
        pos = self.ids["rl"].pos
        size = self.ids["rl"].size
        if pos[0] < touch.x < pos[0]+size[0] and pos[1] < touch.y < pos[1]+size[1]:
                self.plot_dot(touch)

    def plot_dot(self, touch):
        ds: Canvas = self.ids["rl"].canvas
        pos = self.ids["rl"].pos
        clr = Color(rgba=(0.2, 0.6, 0.9, 1))
        w = 20
        h = 20
        pnt = Ellipse(size=(w, h), pos=(touch.x-pos[0] - w, touch.y-pos[1] - h), color="black")
        ds.add(clr)
        ds.add(pnt)
        ds.ask_update()
