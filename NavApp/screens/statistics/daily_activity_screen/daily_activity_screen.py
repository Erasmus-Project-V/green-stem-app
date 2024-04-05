from kivymd.uix.screen import MDScreen


class DailyActivityScreen(MDScreen):
    def start_up_screen(self, activity_name, activity_time):
        self.ids["activity_name"].text = activity_name
        self.ids["activity_time"].text = activity_time
        #self.change_labels(activity_type)
        pass

    def back_arrow(self):
        self.manager.transition.direction = "right"
        self.manager.goto_screen("mss")
        # not good, should be fired on complete of transition
        mss = self.manager.get_screen("mss")
        # mss.bind(on_enter=mss.reenter_hero)