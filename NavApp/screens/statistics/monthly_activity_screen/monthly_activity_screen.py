from kivymd.uix.screen import MDScreen


class MonthlyActivityScreen(MDScreen):
    def start_up_screen(self, hero_tag, activity_type):
        self.ids["hero_to"].tag = hero_tag
        self.activity = activity_type
        print(self.activity)
        self.ids["top_bar"].title = activity_type
        # self.change_labels(activity_type)