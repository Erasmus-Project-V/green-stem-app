from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


class UtilityLoadingScreen(MDScreen):
    caller = None
    callback = None
    loader_text = "Loading"
    loading_speed = 1
    tick = 1

    def start(self, caller, callback=None, dt=0):
        anim = Animation(element_opacity=1,duration=2)
        anim.start(self)
        self.tick = 0
        self.caller = caller
        self.callback = callback
        if dt:
            Clock.schedule_once(self.close, dt)
        self.event = Clock.schedule_interval(self.loading_refresh, 1 / self.loading_speed)

    def close(self, *args):
        if self.callback:
            self.callback(0)
        self.event.cancel()
        if self.caller:
            self.manager.goto_screen(self.caller)

    def loading_refresh(self, dt):
        a = "." * (self.tick % 4)
        self.loader_text = "Loading" + a
        lw = self.ids["loader"]
        lw.text = self.loader_text
        self.tick += 1
