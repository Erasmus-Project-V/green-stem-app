from kivymd.uix.screen import MDScreen


class WeeklyActivityScreen(MDScreen):
    def back_arrow(self):
        self.manager.transition.direction = "right"
        self.manager.current = "mss"
