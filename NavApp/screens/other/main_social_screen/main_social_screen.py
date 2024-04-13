from kivy.metrics import dp
from kivymd.uix.screen import MDScreen


class MainSocialScreen(MDScreen):
    def goto_leaderboard(self,*args):
        self.manager.goto_screen("lss")

    def add_friends_activities(self):
        pass
    def start_up_screen(self):
        self.add_friends_activities()
        self.reheight()


    def reheight(self):
        sl = self.ids["stat_scroller"].children[0]
        total = 0
        for c in sl.children:
            print(c,c.height)
            total += c.height
        print(total)
        sl.height = total + (len(sl.children)-1) * dp(10)
        if sl.height <= self.ids["stat_scroller"].height:
            self.ids["stat_scroller"].do_scroll_y = False
        else:
            self.ids["stat_scroller"].do_scroll_y = True
