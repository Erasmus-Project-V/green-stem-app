from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from custom_widgets.activity_card_widget.activity_card_widget import ActivityCardWidget
from kivymd.color_definitions import colors


class ActivityGridWidget(MDRelativeLayout):
    activity_grid_elements = ListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.build_self, 0)

    def placeholder(self,btn):
        pass
    def build_self(self, clc):
        column_num = 2
        grid = self.create_grid(column_num)
        containers = self.create_box_rows(grid)
        for container in containers:
            self.add_widget(container)

    def create_grid(self, column_num):
        grid = []
        row = []
        for i, element in enumerate(self.activity_grid_elements):
            activity_card = ActivityCardWidget()
            activity_card.hero_tag = element["hero_tag"]
            activity_card.release_func = element["release_func"]
            activity_card.img_path = element["img_path"]
            activity_card.text = element["text"]

            row.append(activity_card)

            if (i + 1) % column_num == 0:
                grid.append(row)
                row = []
            elif i == len(self.activity_grid_elements) - 1:
                grid.append(row)
        return grid

    def create_box_rows(self, grid):
        pos_hints = [{"center_x":0.54,"center_y":1.16}, {"center_x": 0.54, "center_y": 0.9}, {"center_x": 0.54, "center_y": 0.64}]
        box_list = []
        print(grid)
        for i, row in enumerate(grid):
            box = MDBoxLayout()
            box.pos_hint = pos_hints[i]
            for element in row:
                if len(row) == 1:
                    # element.pos_hint = {"center_x": 0.7,"center_y":1}
                    box.pos_hint = {'center_x': 0.8, 'center_y': box.pos_hint['center_y']}
                    box.add_widget(element)
                else:
                    box.add_widget(element)
            print(box.pos_hint, "THIS IS THE BOX POSITION")
            box_list.append(box)
        return box_list
