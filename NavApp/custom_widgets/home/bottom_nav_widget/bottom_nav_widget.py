from kivymd.uix.relativelayout import MDRelativeLayout

from NavApp.scripts.utilities import find_manager


class BottomNavWidget(MDRelativeLayout):
    selected: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_map = {"home_button": "hme", "stats_button": "mss", "social_button": "mso", "account_button": "pfs"}

    def selector_pressed(self, selector):
        manager = find_manager(self, )
        manager.goto_screen(self.screen_map[selector.name])
