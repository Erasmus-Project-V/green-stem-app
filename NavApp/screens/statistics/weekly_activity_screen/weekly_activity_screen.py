from kivymd.uix.screen import MDScreen


class WeeklyActivityScreen(MDScreen):
    activity = None

    def back_arrow(self):
        self.manager.transition.direction = "right"
        self.manager.goto_screen("mss")
        # not good, should be fired on complete of transition
        mss = self.manager.get_screen("mss")
        mss.bind(on_enter=mss.reenter_hero)

    def start_up_screen(self,hero_tag, activity_type):
        self.ids["hero_to"].tag = hero_tag
        self.activity = activity_type
        print(self.activity)
        self.ids["top_bar"].title = activity_type
