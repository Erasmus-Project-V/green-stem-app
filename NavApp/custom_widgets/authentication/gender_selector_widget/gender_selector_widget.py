from kivymd.uix.relativelayout import MDRelativeLayout


class GenderSelectorWidget(MDRelativeLayout):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.selected = "none"
        self.bindable = kwargs["bindable"] if "bindable" in kwargs else None

    def gender_selected(self, btn):
        btn.md_bg_color = self.blue_container
        if btn.name == "male":
            self.ids["bf"].change_color(self.grey_container)
            self.ids["icon_female"].color = "white"
            self.ids["label_female"].color = "white"
            self.ids["icon_male"].color = "black"
            self.ids["label_male"].color = "black"
        else:
            self.ids["bm"].change_color(self.grey_container)
            self.ids["icon_female"].color = "black"
            self.ids["label_female"].color = "black"
            self.ids["icon_male"].color = "white"
            self.ids["label_male"].color = "white"
        btn.selected = 1
        self.selected = btn.name
        if self.bindable:
            self.bindable()

    def get_selected_value(self):
        return self.selected

    def start_repeatable_intervals(self):
        pass

    def stop_repeatable_intervals(self):
        pass
